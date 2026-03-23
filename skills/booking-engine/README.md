# Booking Engine

> Appointment booking system for service-based businesses

---

## What It Does

Booking Engine is a complete appointment scheduling system that lets small businesses manage bookings, services, and availability without third-party platforms or commissions. It runs entirely on your machine with a simple JSON-based backend — no internet required after setup.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install booking-engine
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Book your first appointment in seconds:

```bash
python main.py book "Haircut" "John Smith" "2026-03-25" "10:00"
```

---

## Commands

### `book`

**What it does:** Create a new appointment booking.

**Usage:**
```bash
python main.py book [service] [client] [date] [time]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `service` | ✅ Yes | Name of the service | `Haircut` |
| `client` | ✅ Yes | Client's name | `Jane Doe` |
| `date` | ✅ Yes | Date in YYYY-MM-DD format | `2026-03-25` |
| `time` | ✅ Yes | Time in HH:MM format | `14:00` |

**Example:**
```bash
python main.py book "Haircut" "Jane Doe" "2026-03-25" "10:00"
python main.py book "Massage" "John Smith" "2026-03-26" "15:30"
```

**Output:**
```
✅ Booked: Jane Doe for Haircut on 2026-03-25 at 10:00
   Booking ID: BOOK-20260325-001
```

---

### `list`

**What it does:** Display all bookings, optionally filtered.

**Usage:**
```bash
python main.py list [date]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `date` | ❌ No | Filter by date (YYYY-MM-DD) | `2026-03-25` |

**Example:**
```bash
python main.py list
python main.py list 2026-03-25
```

**Output:**
```
📅 Bookings for 2026-03-25:
------------------------------------------------------------
1. BOOK-20260325-001 | 10:00 | Jane Doe | Haircut | confirmed
2. BOOK-20260325-002 | 14:00 | John Smith | Massage | confirmed
```

---

### `cancel`

**What it does:** Cancel an existing booking.

**Usage:**
```bash
python main.py cancel [booking-id]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `booking-id` | ✅ Yes | The booking ID to cancel | `BOOK-20260325-001` |

**Example:**
```bash
python main.py cancel BOOK-20260325-001
```

**Output:**
```
✅ Cancelled: BOOK-20260325-001
```

---

### `services`

**What it does:** List all available services.

**Usage:**
```bash
python main.py services
```

**Example:**
```bash
python main.py services
```

**Output:**
```
✂️ Available Services:
------------------------------------------------------------
1. Haircut        | 30 min  | $35
2. Massage        | 60 min  | $65
3. Consultation   | 15 min  | Free
```

---

### `availability`

**What it does:** Check available time slots for a given date.

**Usage:**
```bash
python main.py availability [date]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `date` | ✅ Yes | Date to check (YYYY-MM-DD) | `2026-03-25` |

**Example:**
```bash
python main.py availability 2026-03-25
```

**Output:**
```
🗓️ Available slots for 2026-03-25:
09:00, 09:30, 10:30, 11:00, 13:00, 14:30...
```

---

### `configure`

**What it does:** Run the interactive setup wizard to configure business settings.

**Usage:**
```bash
python main.py configure
```

**Example:**
```bash
python main.py configure
```

**Output:**
```
💼 Booking Engine Configuration
==================================================

Business Name: Your Business Name
Working Hours: 09:00 - 17:00
Buffer Between Bookings: 15 minutes

✅ Configuration saved!
```

---

## Use Cases

- **Hair salon:** Let clients book haircut, color, or styling appointments
- **Consulting:** Schedule client consultations with time blocks
- **Coaching:** Manage one-on-one coaching session bookings
- **Personal training:** Book gym sessions with availability tracking
- **Tutoring:** Schedule tutoring appointments with students

---

## Tips & Tricks

- Use `--date` flag to pre-fill common booking dates in scripts
- Combine with cron jobs to send daily booking reminders
- Export bookings to CSV for reporting: `python main.py list > bookings.csv`
- Set up a shared calendar file for household scheduling

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Service not found" | Check your services config or use exact service name |
| "Time slot not available" | Try a different time or check existing bookings |
| "Invalid date format" | Use exactly YYYY-MM-DD (e.g., 2026-03-25) |
| No bookings showing | Run `python main.py list` without a date argument |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies (uses built-in `json` module)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/booking-engine)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
