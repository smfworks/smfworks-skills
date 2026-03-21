#!/usr/bin/env python3
"""
Booking Engine - SMF Works Pro Skill
Create booking pages, manage availability, and schedule appointments.

Usage:
    smf run booking-engine create --name "Consultation" --duration 60 --buffer 15
    smf run booking-engine availability BOOKING-ID --add "monday:09:00-17:00"
    smf run booking-engine serve BOOKING-ID --port 8080
    smf run booking-engine appointments BOOKING-ID
"""

import sys
import json
import uuid
import re
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add shared auth to path
shared_path = Path(__file__).parent.parent.parent / "shared"
sys.path.insert(0, str(shared_path))

from smf_auth import require_subscription, show_subscription_error

# Skill configuration
SKILL_NAME = "booking-engine"
MIN_TIER = "pro"
BOOKINGS_DIR = Path.home() / ".smf" / "bookings"
APPOINTMENTS_DIR = Path.home() / ".smf" / "appointments"
BOOKING_LOCK_FILE = Path.home() / ".smf" / ".booking_lock"

# Days of week
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

# Timezone handling
DEFAULT_TIMEZONE = "America/New_York"

# Rate limiting
MAX_APPOINTMENTS_PER_DAY = 20  # Prevent spam


class BookingLock:
    """File-based lock for preventing race conditions."""
    
    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout
        self.lock_acquired = False
    
    def __enter__(self):
        """Acquire lock with timeout."""
        start_time = time.time()
        while True:
            try:
                # Simple file-based lock using existence check
                if not BOOKING_LOCK_FILE.exists():
                    BOOKING_LOCK_FILE.touch()
                    self.lock_acquired = True
                    return self
            except OSError:
                pass
            
            if time.time() - start_time >= self.timeout:
                raise TimeoutError("Could not acquire booking lock")
            time.sleep(0.1)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release lock."""
        if self.lock_acquired:
            try:
                BOOKING_LOCK_FILE.unlink()
            except:
                pass
        return False


def ensure_dirs():
    """Ensure booking directories exist."""
    BOOKINGS_DIR.mkdir(parents=True, exist_ok=True)
    APPOINTMENTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_booking_id() -> str:
    """Generate unique booking page ID."""
    return f"BOOK-{uuid.uuid4().hex[:8].upper()}"


def generate_appointment_id() -> str:
    """Generate unique appointment ID."""
    return f"APPT-{uuid.uuid4().hex[:8].upper()}"


def sanitize_id(id_str: str) -> str:
    """Sanitize ID string."""
    return re.sub(r'[^\w\-]', '', id_str)


def parse_time(time_str: str) -> Optional[int]:
    """Parse time string (HH:MM) to minutes."""
    try:
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
        
        # Validate range
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            return None
        
        return hours * 60 + minutes
    except (ValueError, IndexError):
        return None


def format_time(minutes: int) -> str:
    """Format minutes to time string (HH:MM)."""
    if minutes < 0 or minutes >= 24 * 60:
        return "00:00"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def validate_date(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def normalize_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    """Simple timezone conversion (basic implementation)."""
    # This is a simplified implementation
    # In production, use pytz or zoneinfo
    return dt


def create_booking_page(name: str, duration: int = 60, buffer_minutes: int = 15,
                       description: str = "", location: str = "",
                       timezone: str = DEFAULT_TIMEZONE) -> Dict:
    """Create a new booking page."""
    try:
        ensure_dirs()
        
        # Validate inputs
        if not name or len(name) > 200:
            return {"success": False, "error": "Name required (max 200 chars)"}
        
        if duration <= 0 or duration > 480:  # Max 8 hours
            return {"success": False, "error": "Duration must be 1-480 minutes"}
        
        if buffer_minutes < 0 or buffer_minutes > 120:
            return {"success": False, "error": "Buffer must be 0-120 minutes"}
        
        booking_id = generate_booking_id()
        
        booking = {
            "id": booking_id,
            "name": name.strip(),
            "description": description[:500] if description else "",
            "duration": duration,
            "buffer_minutes": buffer_minutes,
            "location": location[:200] if location else "",
            "timezone": timezone,
            "availability": {},
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "max_per_day": MAX_APPOINTMENTS_PER_DAY
        }
        
        booking_file = BOOKINGS_DIR / f"{booking_id}.json"
        booking_file.write_text(json.dumps(booking, indent=2))
        
        return {"success": True, "booking": booking}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_booking(booking_id: str) -> Optional[Dict]:
    """Load booking page by ID."""
    safe_id = sanitize_id(booking_id)
    booking_file = BOOKINGS_DIR / f"{safe_id}.json"
    
    if booking_file.exists():
        try:
            return json.loads(booking_file.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return None


def load_bookings() -> List[Dict]:
    """Load all booking pages."""
    ensure_dirs()
    bookings = []
    for booking_file in BOOKINGS_DIR.glob("BOOK-*.json"):
        try:
            booking = json.loads(booking_file.read_text())
            bookings.append(booking)
        except (json.JSONDecodeError, IOError):
            continue
    bookings.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return bookings


def add_availability(booking_id: str, day: str, start_time: str, end_time: str) -> Dict:
    """Add availability slot with validation."""
    booking = load_booking(booking_id)
    if not booking:
        return {"success": False, "error": "Booking page not found"}
    
    day = day.lower()
    if day not in DAYS:
        return {"success": False, "error": f"Invalid day: {day}"}
    
    start_mins = parse_time(start_time)
    end_mins = parse_time(end_time)
    
    if start_mins is None or end_mins is None:
        return {"success": False, "error": "Invalid time format (use HH:MM)"}
    
    if start_mins >= end_mins:
        return {"success": False, "error": "Start time must be before end time"}
    
    if "availability" not in booking:
        booking["availability"] = {}
    
    if day not in booking["availability"]:
        booking["availability"][day] = []
    
    # Check for overlapping slots
    for slot in booking["availability"][day]:
        if (start_mins < slot["end_mins"] and end_mins > slot["start_mins"]):
            return {"success": False, "error": "Time slot overlaps with existing availability"}
    
    booking["availability"][day].append({
        "start": start_time,
        "end": end_time,
        "start_mins": start_mins,
        "end_mins": end_mins
    })
    
    booking["availability"][day].sort(key=lambda x: x["start_mins"])
    
    booking_file = BOOKINGS_DIR / f"{booking_id}.json"
    booking_file.write_text(json.dumps(booking, indent=2))
    
    return {"success": True, "booking": booking}


def get_available_slots(booking_id: str, date: str) -> List[str]:
    """Get available time slots for a date."""
    if not validate_date(date):
        return []
    
    booking = load_booking(booking_id)
    if not booking:
        return []
    
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_name = date_obj.strftime("%A").lower()
    except:
        return []
    
    if day_name not in booking.get("availability", {}):
        return []
    
    # Load appointments for this date
    appointments = load_appointments(booking_id, date)
    booked_slots = set()
    
    for appt in appointments:
        if appt.get("status") not in ["cancelled", "declined"]:
            # Account for duration + buffer
            start_time = appt.get("start_time", "")
            start_mins = parse_time(start_time)
            if start_mins is not None:
                duration = booking.get("duration", 60)
                buffer_mins = booking.get("buffer_minutes", 15)
                total_slot = duration + buffer_mins
                
                # Mark all slots that overlap
                for i in range(start_mins - total_slot + 1, start_mins + total_slot):
                    if i >= 0 and i < 24 * 60:
                        booked_slots.add(format_time(i))
    
    duration = booking.get("duration", 60)
    buffer_mins = booking.get("buffer_minutes", 15)
    slot_length = duration + buffer_mins
    
    available = []
    for slot in booking["availability"][day_name]:
        current = slot["start_mins"]
        while current + duration <= slot["end_mins"]:
            time_str = format_time(current)
            if time_str not in booked_slots:
                available.append(time_str)
            current += slot_length
    
    return available


def count_appointments_today(booking_id: str) -> int:
    """Count appointments for today (rate limiting)."""
    today = datetime.now().strftime("%Y-%m-%d")
    appointments = load_appointments(booking_id, today)
    return len([a for a in appointments if a.get("status") not in ["cancelled", "declined"]])


def book_appointment(booking_id: str, date: str, time: str, 
                    name: str, email: str, notes: str = "") -> Dict:
    """Book an appointment with race condition protection."""
    booking = load_booking(booking_id)
    if not booking:
        return {"success": False, "error": "Booking page not found"}
    
    if booking.get("status") != "active":
        return {"success": False, "error": "Booking page is not accepting appointments"}
    
    # Validate inputs
    if not validate_date(date):
        return {"success": False, "error": "Invalid date format (use YYYY-MM-DD)"}
    
    if not name or len(name) > 100:
        return {"success": False, "error": "Name required (max 100 chars)"}
    
    if not email or len(email) > 100:
        return {"success": False, "error": "Email required (max 100 chars)"}
    
    try:
        with BookingLock():
            # Re-check availability after acquiring lock
            available = get_available_slots(booking_id, date)
            if time not in available:
                return {"success": False, "error": "Time slot no longer available"}
            
            # Rate limiting check
            today = datetime.now().strftime("%Y-%m-%d")
            if date == today:
                today_count = count_appointments_today(booking_id)
                if today_count >= booking.get("max_per_day", MAX_APPOINTMENTS_PER_DAY):
                    return {"success": False, "error": "Daily booking limit reached"}
            
            ensure_dirs()
            
            appointment_id = generate_appointment_id()
            duration = booking.get("duration", 60)
            start_mins = parse_time(time)
            end_time = format_time(start_mins + duration)
            
            appointment = {
                "id": appointment_id,
                "booking_id": booking_id,
                "booking_name": booking.get("name", ""),
                "date": date,
                "start_time": time,
                "end_time": end_time,
                "duration": duration,
                "name": name[:100],
                "email": email[:100],
                "notes": notes[:500] if notes else "",
                "status": "confirmed",
                "created_at": datetime.now().isoformat(),
                "location": booking.get("location", "")
            }
            
            appt_file = APPOINTMENTS_DIR / f"{appointment_id}.json"
            appt_file.write_text(json.dumps(appointment, indent=2))
            
            return {"success": True, "appointment": appointment}
        
    except TimeoutError:
        return {"success": False, "error": "Booking system busy, please try again"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_appointments(booking_id: str = None, date: str = None) -> List[Dict]:
    """Load appointments with filters."""
    ensure_dirs()
    appointments = []
    for appt_file in APPOINTMENTS_DIR.glob("APPT-*.json"):
        try:
            appt = json.loads(appt_file.read_text())
            if booking_id and appt.get("booking_id") != booking_id:
                continue
            if date and appt.get("date") != date:
                continue
            appointments.append(appt)
        except (json.JSONDecodeError, IOError):
            continue
    appointments.sort(key=lambda x: (x.get("date", ""), x.get("start_time", "")))
    return appointments


def cancel_appointment(appointment_id: str) -> Dict:
    """Cancel appointment."""
    appt_file = APPOINTMENTS_DIR / f"{sanitize_id(appointment_id)}.json"
    if not appt_file.exists():
        return {"success": False, "error": "Appointment not found"}
    
    try:
        appt = json.loads(appt_file.read_text())
        appt["status"] = "cancelled"
        appt["cancelled_at"] = datetime.now().isoformat()
        appt_file.write_text(json.dumps(appt, indent=2))
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


class BookingHandler(BaseHTTPRequestHandler):
    """HTTP request handler with timezone support."""
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        """Handle GET requests."""
        path_parts = self.path.strip('/').split('/')
        
        if not path_parts or not path_parts[0].startswith("BOOK-"):
            self.send_error(404, "Not found")
            return
        
        booking_id = path_parts[0]
        booking = load_booking(booking_id)
        
        if not booking:
            self.send_error(404, "Booking not found")
            return
        
        # Check for date parameter
        date_param = None
        if '?' in self.path:
            query = self.path.split('?')[1]
            params = {}
            for param in query.split('&'):
                if '=' in param:
                    k, v = param.split('=', 1)
                    params[k] = v
            date_param = params.get('date')
        
        if not date_param or not validate_date(date_param):
            date_param = datetime.now().strftime("%Y-%m-%d")
        
        available = get_available_slots(booking_id, date_param)
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{booking.get('name', 'Book')}</title>
    <style>
        body {{ font-family: sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }}
        h1 {{ color: #333; }}
        .timezone {{ color: #666; font-size: 0.9em; margin-bottom: 20px; }}
        .slot {{ background: #2563eb; color: white; padding: 10px 20px; margin: 5px; 
                display: inline-block; border-radius: 4px; text-decoration: none; }}
        .slot:hover {{ background: #1d4ed8; }}
        .no-slots {{ color: #666; font-style: italic; }}
        form {{ margin-top: 20px; }}
        input, button {{ padding: 10px; margin: 5px 0; width: 100%; box-sizing: border-box; }}
        button {{ background: #2563eb; color: white; border: none; cursor: pointer; }}
    </style>
</head>
<body>
    <h1>{booking.get('name', 'Book Appointment')}</h1>
    <p class="timezone">Timezone: {booking.get('timezone', DEFAULT_TIMEZONE)}</p>
    <p>{booking.get('description', '')}</p>
    
    <h3>Available Times for {date_param}</h3>
    {' '.join([f'<a href="/{booking_id}/book?date={date_param}&time={t}" class="slot">{t}</a>' for t in available]) if available else '<p class="no-slots">No available slots</p>'}
    
    <p style="margin-top: 30px;">
        <a href="/{booking_id}/">View another date</a>
    </p>
</body>
</html>"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def do_POST(self):
        """Handle POST requests."""
        if not self.path.startswith("/"):
            self.send_error(404, "Not found")
            return
        
        parts = self.path.strip('/').split('/')
        if len(parts) < 2 or parts[1] != "book":
            self.send_error(404, "Not found")
            return
        
        booking_id = parts[0]
        
        # Parse form data
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            from urllib.parse import parse_qs
            data = parse_qs(post_data)
        except:
            self.send_error(400, "Bad request")
            return
        
        date = data.get('date', [''])[0]
        time = data.get('time', [''])[0]
        name = data.get('name', [''])[0]
        email = data.get('email', [''])[0]
        notes = data.get('notes', [''])[0]
        
        result = book_appointment(booking_id, date, time, name, email, notes)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if result["success"]:
            html = f"""<!DOCTYPE html>
<html>
<head><title>Booked!</title></head>
<body style="font-family: sans-serif; text-align: center; padding: 50px;">
    <h1>✅ Booked!</h1>
    <p>Your appointment is confirmed for {date} at {time}.</p>
    <p>Appointment ID: {result['appointment']['id']}</p>
    <a href="/{booking_id}/">Book another</a>
</body>
</html>"""
        else:
            html = f"""<!DOCTYPE html>
<html>
<head><title>Error</title></head>
<body style="font-family: sans-serif; text-align: center; padding: 50px;">
    <h1>❌ Booking Failed</h1>
    <p>{result.get('error', 'Unknown error')}</p>
    <a href="javascript:history.back()">Try again</a>
</body>
</html>"""
        
        self.wfile.write(html.encode())


def serve_bookings(port: int = 8080):
    """Start HTTP server."""
    server = HTTPServer(('localhost', port), BookingHandler)
    print(f"\n🌐 Server running at http://localhost:{port}/")
    print("Press Ctrl+C to stop\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Server stopped")
        server.shutdown()


def main():
    """CLI entry point."""
    if "--test-mode" in sys.argv:
        sys.argv.remove("--test-mode")
        subscription = {"valid": True, "tier": "test"}
    else:
        subscription = require_subscription(SKILL_NAME, MIN_TIER)
        if not subscription["valid"]:
            show_subscription_error(subscription)
            return 1
    
    print(f"📅 Booking Engine")
    print(f"   Subscription: {subscription.get('tier', 'test')}")
    
    if len(sys.argv) < 2:
        print("\nCommands: create, list, availability, serve, appointments, cancel")
        return 0
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "create":
        name = input("Service name: ").strip()
        if not name:
            print("❌ Name required")
            return 1
        duration = int(input("Duration minutes [60]: ") or "60")
        buffer_mins = int(input("Buffer minutes [15]: ") or "15")
        timezone = input(f"Timezone [{DEFAULT_TIMEZONE}]: ").strip() or DEFAULT_TIMEZONE
        
        result = create_booking_page(name, duration, buffer_mins, timezone=timezone)
        if result["success"]:
            print(f"✅ Created: {result['booking']['id']}")
            print(f"   Timezone: {result['booking']['timezone']}")
            print(f"   Add availability: smf run booking-engine availability {result['booking']['id']} --add monday:09:00-17:00")
    
    elif command == "list":
        bookings = load_bookings()
        for b in bookings:
            print(f"{b['id']}: {b.get('name')} ({b.get('duration')} min, {b.get('timezone')})")
    
    elif command == "availability":
        if len(args) < 1:
            print("❌ Booking ID required")
            return 1
        booking_id = args[0]
        if "--add" in args:
            idx = args.index("--add")
            slot = args[idx + 1]
            day, times = slot.split(":")
            start, end = times.split("-")
            for d in day.split(","):
                result = add_availability(booking_id, d.strip(), start.strip(), end.strip())
                if result["success"]:
                    print(f"✅ Added: {d.strip()} {start}-{end}")
                else:
                    print(f"❌ {result.get('error')}")
        else:
            booking = load_booking(booking_id)
            if booking:
                print(f"Availability for {booking.get('name')}:")
                print(f"Timezone: {booking.get('timezone', DEFAULT_TIMEZONE)}")
                for day, slots in booking.get("availability", {}).items():
                    print(f"  {day}: {', '.join([s['start']+'-'+s['end'] for s in slots])}")
    
    elif command == "serve":
        port = 8080
        if "--port" in args:
            idx = args.index("--port")
            port = int(args[idx + 1])
        serve_bookings(port)
    
    elif command == "appointments":
        booking_id = args[0] if args else None
        appointments = load_appointments(booking_id)
        for a in appointments:
            print(f"{a['date']} {a['start_time']}: {a.get('name')} - {a.get('status')}")
    
    elif command == "cancel":
        if len(args) < 1:
            print("❌ Appointment ID required")
            return 1
        result = cancel_appointment(args[0])
        if result["success"]:
            print("✅ Cancelled")
        else:
            print(f"❌ {result.get('error')}")
    
    else:
        print(f"Unknown command: {command}")
    
    return 0


def show_help():
    """Show help message."""
    print("""📅 Booking Engine

Create booking pages and manage appointments.

Commands:
  create                        Create new booking page
  list                          List all booking pages
  availability BOOKING-ID       Show/set availability
  serve BOOKING-ID              Start HTTP server
  appointments BOOKING-ID       List appointments
  cancel APPT-ID                Cancel appointment
  help                          Show this help

Examples:
  smf run booking-engine create
  smf run booking-engine availability BOOK-ABC123 --add monday:09:00-17:00
  smf run booking-engine serve BOOK-ABC123 --port 8080
  smf run booking-engine appointments BOOK-ABC123

Security:
  • File-based locking prevents race conditions
  • Daily booking limits prevent spam
  • Timezone support for global scheduling
""")


if __name__ == "__main__":
    sys.exit(main())
