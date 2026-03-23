# Booking Engine

> Create appointment booking pages, set your availability, serve a local booking form, and manage appointments — from your terminal.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Business / Scheduling

---

## What It Does

Booking Engine is an OpenClaw Pro skill for creating appointment booking systems. Create a booking page with your service description, set your weekly availability, serve the booking form via a local HTTP server, let clients book appointments, and manage your calendar of upcoming appointments.

**Security features:** File-based locking to prevent double-booking, daily booking limits to prevent spam, and timezone support for global scheduling.

**What it does NOT do:** It does not send email confirmations automatically, sync to Google Calendar, process payments, expose the booking page to the internet (local/LAN only), or provide video call links.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/booking-engine
python3 main.py help
```

---

## Quick Start

```bash
# Create a booking page
python3 main.py create

# Set your availability
python3 main.py availability BOOK-ABC123 --add monday:09:00-17:00
python3 main.py availability BOOK-ABC123 --add tuesday:09:00-17:00

# Start the booking server
python3 main.py serve BOOK-ABC123 --port 8080
# Clients visit: http://localhost:8080/BOOK-ABC123

# View appointments
python3 main.py appointments BOOK-ABC123
```

---

## Command Reference

### `create`

Creates a new booking page. Interactive.

```bash
python3 main.py create
```

Prompts for:
- Booking page name
- Service description
- Default appointment duration
- Time zone

Output:
```
✅ Booking page created: BOOK-A1B2C3
   Name: Consultation Call
   Duration: 30 minutes
   URL: http://localhost:8080/BOOK-A1B2C3
```

---

### `list`

Lists all booking pages.

```bash
python3 main.py list
```

Output:
```
📅 Booking Pages (2 total):

1. BOOK-A1B2C3 — Consultation Call — 30 min — 3 appointments pending
2. BOOK-D4E5F6 — Strategy Session — 60 min — 1 appointment pending
```

---

### `availability BOOKING-ID`

Sets or views availability for a booking page.

**Add availability for a day:**
```bash
python3 main.py availability BOOK-A1B2C3 --add monday:09:00-17:00
python3 main.py availability BOOK-A1B2C3 --add tuesday:09:00-12:00
python3 main.py availability BOOK-A1B2C3 --add thursday:14:00-18:00
```

Output:
```
✅ Availability added: monday 09:00–17:00
```

**View current availability:**
```bash
python3 main.py availability BOOK-A1B2C3
```

Output:
```
📅 Availability: Consultation Call

Monday:    09:00 – 17:00
Tuesday:   09:00 – 12:00
Thursday:  14:00 – 18:00
```

---

### `serve BOOKING-ID`

Starts a local HTTP server serving the booking form.

```bash
python3 main.py serve BOOK-A1B2C3 --port 8080
```

Output:
```
🌐 Booking Server Started
   Page: Consultation Call (BOOK-A1B2C3)
   URL: http://localhost:8080/BOOK-A1B2C3
   Press Ctrl+C to stop

[09:42:11] GET /BOOK-A1B2C3 200 — booking page served
[09:43:55] POST /BOOK-A1B2C3/book 200 — appointment booked: 2024-03-18 10:00
```

The booking form shows a calendar with your available time slots. Clients pick a time and enter their name and email.

---

### `appointments BOOKING-ID`

Lists all upcoming appointments for a booking page.

```bash
python3 main.py appointments BOOK-A1B2C3
```

Output:
```
📅 Appointments: Consultation Call

Upcoming:
1. 2024-03-18 10:00 — Alice Smith — alice@example.com — Confirmed
2. 2024-03-19 14:00 — Bob Jones — bob@techco.io — Confirmed
3. 2024-03-21 09:30 — Carol White — carol@startup.io — Confirmed

Past:
4. 2024-03-15 11:00 — Dan Morrow — dan@company.io — Completed
```

---

### `cancel APPT-ID`

Cancels an appointment.

```bash
python3 main.py cancel APPT-20240318-A1B2C3
```

Output:
```
✅ Appointment cancelled: APPT-20240318-A1B2C3
   Note: Consider notifying the client manually.
```

---

## Use Cases

### 1. Freelance consultation booking

Create a "30-minute consultation" booking page, set your availability, and share the local URL with clients on your LAN or via screen share during a call.

### 2. Internal team meeting booking

Run on your company LAN so teammates can book time with you.

### 3. Event slot registration

Create a booking page for timed event slots (demos, presentations), set availability for each slot, and let attendees register.

---

## How Booking Works

1. Client visits `http://localhost:PORT/BOOK-ID`
2. They see a calendar showing your available slots
3. They select a slot, enter name and email, and submit
4. The slot is locked (file-based locking prevents double-booking)
5. Appointment is saved to `~/.smf/bookings/BOOK-ID/`
6. You see it in `appointments`

**No email confirmation is sent automatically.** If you want to notify clients, contact them manually using the email address they provided.

---

## Configuration

Data stored at: `~/.smf/bookings/`

| Setting | Where to set |
|---------|-------------|
| Daily booking limit | Configured during `create` |
| Appointment duration | Configured during `create` |
| Availability | Via `availability --add` command |

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### No time slots showing on booking form
**Fix:** You need to add availability first: `python3 main.py availability BOOK-ID --add monday:09:00-17:00`

### `Address already in use: port 8080`
**Fix:** Use a different port: `--port 8090`

### Double booking despite locking
**Fix:** The file-based locking prevents concurrent bookings on the same slot. If two people book the same slot nearly simultaneously, one will receive an error. This is expected behavior.

---

## FAQ

**Q: Can clients cancel their own bookings?**  
A: Not via the web form. Use `cancel APPT-ID` from the CLI to cancel.

**Q: Does it send confirmation emails?**  
A: No. You need to contact clients manually using the email address they provided when booking.

**Q: How do I share the booking page externally?**  
A: The server binds to `localhost` only. For LAN sharing, use your machine's local IP. For internet access, you'd need a reverse proxy — outside this skill's scope.

**Q: What's the daily booking limit?**  
A: Set during `create`. The limit prevents spam bookings. A reasonable default is 10–20 per day.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/booking-engine)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
