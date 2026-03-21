# Booking Engine

Create booking pages, manage your availability, and accept appointments. Perfect for consultants, coaches, service providers, and anyone who needs to schedule time with clients.

## Features

- ✅ **Booking Pages** — Create multiple service types
- ✅ **Availability Management** — Set weekly schedules
- ✅ **Duration & Buffer** — Configure appointment length and gaps
- ✅ **HTTP Server** — Built-in booking website
- ✅ **Appointment Management** — View, cancel, complete
- ✅ **Conflict Prevention** — Automatic slot blocking
- ✅ **Local Storage** — All data stays on your machine

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install booking-engine
```

## Quick Start

### 1. Create a Booking Page

```bash
smf run booking-engine create
# Service name: Initial Consultation
# Duration: 60
# Buffer: 15
```

### 2. Set Your Availability

```bash
smf run booking-engine availability BOOK-ABC123 --add "monday,tuesday,wednesday:09:00-17:00"
smf run booking-engine availability BOOK-ABC123 --add "thursday,friday:10:00-16:00"
```

### 3. Start the Server

```bash
smf run booking-engine serve --port 8080
```

### 4. Share the Link

`http://localhost:8080/BOOK-ABC123`

Clients can book directly. Appointments are saved automatically.

### 5. View Appointments

```bash
smf run booking-engine appointments BOOK-ABC123
```

## Usage

### Creating Booking Pages

**Interactive:**
```bash
smf run booking-engine create
```

**Quick mode:**
```bash
smf run booking-engine create --name "Consultation" --duration 60 --buffer 15 --location "Video Call"
```

**Parameters:**
- `name` — Service name (required)
- `duration` — Length in minutes (default: 60)
- `buffer` — Gap between appointments (default: 15)
- `location` — Where it happens (optional)
- `description` — Service description (optional)

### Setting Availability

**Add availability:**
```bash
# Single day
smf run booking-engine availability BOOK-ABC --add "monday:09:00-17:00"

# Multiple days
smf run booking-engine availability BOOK-ABC --add "monday,wednesday,friday:09:00-17:00"

# Different times
smf run booking-engine availability BOOK-ABC --add "monday:09:00-12:00"
smf run booking-engine availability BOOK-ABC --add "monday:14:00-17:00"
```

**View availability:**
```bash
smf run booking-engine availability BOOK-ABC
```

**Remove slot:**
```bash
smf run booking-engine availability BOOK-ABC --remove monday --index 0
```

### Serving Booking Pages

**Start server:**
```bash
smf run booking-engine serve
# Serves on http://localhost:8080/
```

**Custom port:**
```bash
smf run booking-engine serve --port 3000
```

**Access:**
- Main page: `http://localhost:8080/` (lists all booking pages)
- Specific page: `http://localhost:8080/BOOK-ABC123`

**Stop server:**
- Press `Ctrl+C`

### Managing Appointments

**List appointments:**
```bash
# All appointments
smf run booking-engine appointments

# For specific booking page
smf run booking-engine appointments BOOK-ABC123

# For specific date
smf run booking-engine appointments BOOK-ABC123 --date 2026-03-25
```

**Cancel appointment:**
```bash
smf run booking-engine cancel APPT-XYZ789
```

**Mark completed:**
```bash
smf run booking-engine complete APPT-XYZ789
```

### Viewing Booking Pages

**List all:**
```bash
smf run booking-engine list
```

**Show details:**
```bash
smf run booking-engine show BOOK-ABC123
```

## Booking Page Examples

### Consultation Call

```bash
smf run booking-engine create --name "Free Consultation" --duration 30 --buffer 10 --location "Zoom"
smf run booking-engine availability BOOK-XXX --add "monday,friday:09:00-12:00"
```

### Coaching Session

```bash
smf run booking-engine create --name "Coaching Session" --duration 60 --buffer 15 --location "Office"
smf run booking-engine availability BOOK-XXX --add "tuesday,thursday:14:00-18:00"
```

### Office Hours

```bash
smf run booking-engine create --name "Office Hours" --duration 30 --buffer 5 --location "Room 301"
smf run booking-engine availability BOOK-XXX --add "wednesday:13:00-17:00"
```

## Storage Structure

```
~/.smf/
├── bookings/
│   ├── BOOK-ABC123.json       # Booking page definition
│   └── BOOK-DEF456.json
└── appointments/
    ├── APPT-XYZ789.json       # Individual appointment
    └── ...
```

### Booking JSON Format

```json
{
  "id": "BOOK-ABC123",
  "name": "Consultation",
  "description": "Initial meeting",
  "duration": 60,
  "buffer_minutes": 15,
  "location": "Zoom",
  "availability": {
    "monday": [
      {"start": "09:00", "end": "17:00", "start_mins": 540, "end_mins": 1020}
    ]
  },
  "created_at": "2026-03-20T14:30:00",
  "status": "active",
  "timezone": "America/New_York"
}
```

### Appointment JSON Format

```json
{
  "id": "APPT-XYZ789",
  "booking_id": "BOOK-ABC123",
  "booking_name": "Consultation",
  "date": "2026-03-25",
  "start_time": "14:00",
  "end_time": "15:00",
  "duration": 60,
  "name": "John Smith",
  "email": "john@example.com",
  "notes": "First time client",
  "status": "confirmed",
  "created_at": "2026-03-20T10:00:00",
  "location": "Zoom"
}
```

## How It Works

### Slot Generation

1. **Set availability** — "Monday 9 AM - 5 PM"
2. **Define duration** — 60 minute appointments
3. **Add buffer** — 15 minutes between appointments
4. **Generate slots** — System creates 75-minute blocks
5. **Check conflicts** — Booked slots are automatically hidden

### Booking Flow

1. **Client visits** booking page URL
2. **Selects date** from calendar
3. **Sees available slots** for that date
4. **Chooses time** and enters details
5. **Submits** — Appointment saved
6. **Confirmation** shown to client

### Conflict Prevention

The system automatically:
- ✅ Blocks booked slots
- ✅ Respects buffer time
- ✅ Prevents double-booking
- ✅ Handles cancellations

## Workflows

### Consultant Schedule

```bash
# Create booking page
smf run booking-engine create --name "Strategy Session" --duration 90 --buffer 30

# Set availability (Tues/Thurs afternoons)
smf run booking-engine availability BOOK-XXX --add "tuesday,thursday:13:00-17:00"

# Start server
smf run booking-engine serve

# Check morning appointments
smf run booking-engine appointments BOOK-XXX --date $(date +%Y-%m-%d)
```

### Team Office Hours

```bash
# Create multiple booking pages
smf run booking-engine create --name "CEO Office Hours" --duration 30 --buffer 10
smf run booking-engine create --name "CTO Office Hours" --duration 30 --buffer 10

# Different availability
smf run booking-engine availability BOOK-CEO --add "friday:14:00-16:00"
smf run booking-engine availability BOOK-CTO --add "wednesday:10:00-12:00"

# Serve all on one port
smf run booking-engine serve --port 8080
```

### Class Booking

```bash
# Yoga class
smf run booking-engine create --name "Yoga Class" --duration 60 --buffer 15 --location "Studio A"
smf run booking-engine availability BOOK-XXX --add "monday,wednesday,friday:07:00-08:00"

# 10 spots per class (manual limit tracking)
```

## Best Practices

### 1. Set Realistic Availability

**Don't:**
- Overbook your calendar
- Set 24/7 availability
- Forget lunch breaks

**Do:**
- Leave buffer time
- Block focus time
- Set realistic limits

### 2. Clear Service Names

**Good:**
- "Free 30-Minute Consultation"
- "1-Hour Strategy Session"
- "Quick Check-in Call"

**Bad:**
- "Meeting"
- "Call"

### 3. Include Buffer Time

**Recommended:**
- Back-to-back meetings: 15 min buffer
- Client calls: 5-10 min buffer
- Travel time: Add to buffer

### 4. Set Expectations

**In description:**
- What's included
- Preparation needed
- Cancellation policy

### 5. Regular Reviews

**Weekly:**
```bash
# Check upcoming appointments
smf run booking-engine appointments

# Review cancellations
smf run booking-engine appointments BOOK-XXX --status cancelled
```

### 6. Backup Appointments

```bash
# Weekly backup
tar -czf ~/backups/bookings-$(date +%Y%m%d).tar.gz ~/.smf/bookings/ ~/.smf/appointments/
```

## Integration Ideas

### With Email Notifications

```bash
#!/bin/bash
# check-appointments.sh

export PATH="$HOME/.local/bin:$PATH"

TODAY=$(date +%Y-%m-%d)
APPOINTMENTS=$(smf run booking-engine appointments --date $TODAY 2>/dev/null)

if [ -n "$APPOINTMENTS" ]; then
    echo "Today's appointments:" | mail -s "Daily Schedule" you@example.com
fi
```

### With Calendar Sync

```bash
# Export appointments to CSV
# Import to Google Calendar
smf run booking-engine appointments BOOK-XXX > appointments.txt
```

### With CRM

```bash
# When client books, add to CRM
# (Webhook or script integration)
```

## Pricing

**Booking Engine is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use Calendly, Acuity, or Google Calendar

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
