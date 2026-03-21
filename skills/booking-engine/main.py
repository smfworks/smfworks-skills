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

# Days of week
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


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


def parse_time(time_str: str) -> Optional[int]:
    """Parse time string (HH:MM) to minutes."""
    try:
        parts = time_str.split(":")
        hours = int(parts[0])
        minutes = int(parts[1]) if len(parts) > 1 else 0
        return hours * 60 + minutes
    except:
        return None


def format_time(minutes: int) -> str:
    """Format minutes to time string (HH:MM)."""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"


def create_booking_page(name: str, duration: int = 60, buffer_minutes: int = 15,
                       description: str = "", location: str = "") -> Dict:
    """Create a new booking page."""
    try:
        ensure_dirs()
        
        booking_id = generate_booking_id()
        
        booking = {
            "id": booking_id,
            "name": name,
            "description": description,
            "duration": duration,
            "buffer_minutes": buffer_minutes,
            "location": location,
            "availability": {},
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "timezone": "America/New_York"
        }
        
        booking_file = BOOKINGS_DIR / f"{booking_id}.json"
        booking_file.write_text(json.dumps(booking, indent=2))
        
        return {"success": True, "booking": booking}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_booking(booking_id: str) -> Optional[Dict]:
    """Load booking page by ID."""
    booking_file = BOOKINGS_DIR / f"{booking_id}.json"
    if booking_file.exists():
        try:
            return json.loads(booking_file.read_text())
        except:
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
        except:
            continue
    bookings.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return bookings


def add_availability(booking_id: str, day: str, start_time: str, end_time: str) -> Dict:
    """Add availability slot."""
    booking = load_booking(booking_id)
    if not booking:
        return {"success": False, "error": "Booking page not found"}
    
    day = day.lower()
    if day not in DAYS:
        return {"success": False, "error": f"Invalid day: {day}"}
    
    start_mins = parse_time(start_time)
    end_mins = parse_time(end_time)
    
    if start_mins is None or end_mins is None:
        return {"success": False, "error": "Invalid time format"}
    
    if "availability" not in booking:
        booking["availability"] = {}
    
    if day not in booking["availability"]:
        booking["availability"][day] = []
    
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
    """Get available time slots."""
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
    
    appointments = load_appointments(booking_id, date)
    booked_slots = {a.get("start_time", "") for a in appointments if a.get("status") not in ["cancelled", "declined"]}
    
    duration = booking.get("duration", 60)
    buffer_minutes = booking.get("buffer_minutes", 15)
    slot_length = duration + buffer_minutes
    
    available = []
    for slot in booking["availability"][day_name]:
        current = slot["start_mins"]
        while current + duration <= slot["end_mins"]:
            time_str = format_time(current)
            if time_str not in booked_slots:
                available.append(time_str)
            current += slot_length
    
    return available


def book_appointment(booking_id: str, date: str, time: str, 
                    name: str, email: str, notes: str = "") -> Dict:
    """Book an appointment."""
    booking = load_booking(booking_id)
    if not booking:
        return {"success": False, "error": "Booking page not found"}
    
    available = get_available_slots(booking_id, date)
    if time not in available:
        return {"success": False, "error": "Time slot not available"}
    
    try:
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
            "name": name,
            "email": email,
            "notes": notes,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            "location": booking.get("location", "")
        }
        
        appt_file = APPOINTMENTS_DIR / f"{appointment_id}.json"
        appt_file.write_text(json.dumps(appointment, indent=2))
        
        return {"success": True, "appointment": appointment}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


def load_appointments(booking_id: str = None, date: str = None) -> List[Dict]:
    """Load appointments."""
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
        except:
            continue
    appointments.sort(key=lambda x: (x.get("date", ""), x.get("start_time", "")))
    return appointments


def cancel_appointment(appointment_id: str) -> Dict:
    """Cancel appointment."""
    appt_file = APPOINTMENTS_DIR / f"{appointment_id}.json"
    if not appt_file.exists():
        return {"success": False, "error": "Appointment not found"}
    
    try:
        appt = json.loads(appt_file.read_text())
        appt["status"] = "cancelled"
        appt_file.write_text(json.dumps(appt, indent=2))
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


class BookingHandler(BaseHTTPRequestHandler):
    """HTTP request handler."""
    
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            bookings = load_bookings()
            html = "<html><body><h1>Booking Pages</h1><ul>"
            for b in bookings:
                html += f'<li><a href="/{b["id"]}/">{b.get("name", "Untitled")}</a></li>'
            html += "</ul></body></html>"
            self.wfile.write(html.encode())
        elif self.path.startswith("/BOOK-"):
            booking_id = self.path.strip('/').split('/')[0]
            booking = load_booking(booking_id)
            if booking:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                html = f"""
<!DOCTYPE html>
<html>
<head><title>{booking.get('name', 'Book')}</title></head>
<body>
    <h1>{booking.get('name', 'Book Appointment')}</h1>
    <form method="POST">
        Date: <input type="date" name="date" required><br>
        Time: <input type="text" name="time" placeholder="09:00" required><br>
        Name: <input type="text" name="name" required><br>
        Email: <input type="email" name="email" required><br>
        <button type="submit">Book</button>
    </form>
</body>
</html>"""
                self.wfile.write(html.encode())
            else:
                self.send_error(404, "Not found")
        else:
            self.send_error(404, "Not found")
    
    def do_POST(self):
        if self.path.startswith("/BOOK-"):
            booking_id = self.path.strip('/')
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode()
            from urllib.parse import parse_qs
            data = parse_qs(post_data)
            
            date = data.get('date', [''])[0]
            time = data.get('time', [''])[0]
            name = data.get('name', [''])[0]
            email = data.get('email', [''])[0]
            
            result = book_appointment(booking_id, date, time, name, email)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if result["success"]:
                self.wfile.write(b"<h1>Booked!</h1><p>Your appointment is confirmed.</p>")
            else:
                self.wfile.write(f"<h1>Error</h1><p>{result.get('error')}</p>".encode())
        else:
            self.send_error(404, "Not found")


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
        result = create_booking_page(name, duration)
        if result["success"]:
            print(f"✅ Created: {result['booking']['id']}")
            print(f"   Add availability: smf run booking-engine availability {result['booking']['id']} --add monday:09:00-17:00")
    
    elif command == "list":
        bookings = load_bookings()
        for b in bookings:
            print(f"{b['id']}: {b.get('name')} ({b.get('duration')} min)")
    
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
            booking = load_booking(booking_id)
            if booking:
                print(f"Availability for {booking.get('name')}:")
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
        print(f"Unknown command: {command}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
