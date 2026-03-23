# Booking Engine — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Set Up a Booking Page](#1-how-to-set-up-a-booking-page)
2. [How to Configure Your Availability](#2-how-to-configure-your-availability)
3. [How to Serve Your Booking Page](#3-how-to-serve-your-booking-page)
4. [How to View and Manage Appointments](#4-how-to-view-and-manage-appointments)
5. [How to Cancel an Appointment](#5-how-to-cancel-an-appointment)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Set Up a Booking Page

**What this does:** Creates a booking page with a name, service description, and duration.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/booking-engine
```

**Step 2 — Create a booking page.**

```bash
python3 main.py create
```

Interactive prompts:
```
Booking page name: 30-Minute Consultation
Service description: A focused 30-minute call to discuss your project
Appointment duration (minutes) [30]: 30
Timezone [UTC]: America/New_York
Daily booking limit [10]: 5

✅ Booking page created: BOOK-A1B2C3
   Name: 30-Minute Consultation
   URL: http://localhost:8080/BOOK-A1B2C3
```

**Step 3 — Note your BOOK-ID.**

You'll use this ID for all subsequent commands. Run `python3 main.py list` at any time to see your IDs.

**Result:** Booking page created. Next step: set availability.

---

## 2. How to Configure Your Availability

**What this does:** Sets which days and times you're available for bookings.

### Steps

**Step 1 — Add availability for each day you're available.**

```bash
python3 main.py availability BOOK-A1B2C3 --add monday:09:00-17:00
python3 main.py availability BOOK-A1B2C3 --add tuesday:09:00-17:00
python3 main.py availability BOOK-A1B2C3 --add wednesday:13:00-17:00
python3 main.py availability BOOK-A1B2C3 --add thursday:09:00-12:00
```

Each command outputs:
```
✅ Availability added: monday 09:00–17:00
```

**Step 2 — Verify your availability.**

```bash
python3 main.py availability BOOK-A1B2C3
```

Output:
```
📅 Availability: 30-Minute Consultation

Monday:     09:00 – 17:00
Tuesday:    09:00 – 17:00
Wednesday:  13:00 – 17:00
Thursday:   09:00 – 12:00
```

**Result:** Clients will see these days and times as available on the booking form.

---

## 3. How to Serve Your Booking Page

**What this does:** Starts a local HTTP server that shows the booking form and accepts bookings.

### Steps

**Step 1 — Start the server.**

```bash
python3 main.py serve BOOK-A1B2C3 --port 8080
```

Output:
```
🌐 Booking Server Started
   Page: 30-Minute Consultation (BOOK-A1B2C3)
   URL: http://localhost:8080/BOOK-A1B2C3
   Press Ctrl+C to stop
```

**Step 2 — Open the booking page.**

Go to `http://localhost:8080/BOOK-A1B2C3` in your browser.

The page shows:
- Your service name and description
- A calendar with available time slots
- Name and email fields

**Step 3 — Share the URL with clients.**

For clients on your LAN, share your machine's local IP:
```bash
# Find your local IP:
ip addr | grep "inet 192"
# Share: http://192.168.1.100:8080/BOOK-A1B2C3
```

For local demos, share your screen and let clients select a time slot while on a call.

**Step 4 — Monitor incoming bookings.**

The terminal shows each request:
```
[10:15:22] GET /BOOK-A1B2C3 200 — booking page served
[10:15:45] POST /BOOK-A1B2C3/book 200 — booked: 2024-03-18 10:00 — Alice Smith
```

**Step 5 — Stop the server when done.**

Press `Ctrl+C`.

**Result:** Your booking page is live and accepting appointments.

---

## 4. How to View and Manage Appointments

**When to use it:** Before starting your day or week to see who you have calls with.

```bash
python3 main.py appointments BOOK-A1B2C3
```

Output:
```
📅 Appointments: 30-Minute Consultation

Upcoming:
1. APPT-20240318-A1B — 2024-03-18 10:00 — Alice Smith — alice@example.com
2. APPT-20240319-B2C — 2024-03-19 14:00 — Bob Jones — bob@techco.io
3. APPT-20240321-C3D — 2024-03-21 09:30 — Carol White — carol@startup.io

Past:
4. APPT-20240315-D4E — 2024-03-15 11:00 — Dan Morrow — dan@co.io — Completed
```

Use the client email to reach out with a confirmation or calendar invite.

---

## 5. How to Cancel an Appointment

**When to use it:** A client needs to reschedule, or you need to clear a slot.

```bash
python3 main.py cancel APPT-20240318-A1B
```

Output:
```
✅ Appointment cancelled: APPT-20240318-A1B
   Note: Consider notifying the client manually.
```

After cancelling, notify the client using the email address from `appointments`.

---

## 6. Automating with Cron

### Example: Daily morning appointment reminder

```bash
0 8 * * * python3 /home/yourname/smfworks-skills/skills/booking-engine/main.py appointments BOOK-A1B2C3 >> /home/yourname/logs/appointments.log 2>&1
```

---

## 7. Combining with Other Skills

**Booking Engine + Task Manager:** After each appointment, create a follow-up task:

```bash
python3 ~/smfworks-skills/skills/task-manager/main.py task add "Follow up with Alice Smith" --project client-work --priority high --due 2024-03-20
```

**Booking Engine + Coffee Briefing:** See your calendar events in your morning briefing (Coffee Briefing reads Google Calendar, Booking Engine manages its own storage — for manual cross-referencing).

---

## 8. Troubleshooting Common Issues

### No time slots showing on the booking form

**Fix:** Add availability for at least one day: `python3 main.py availability BOOK-ID --add monday:09:00-17:00`

### `Address already in use: port 8080`

**Fix:** Use a different port: `--port 9090`. Or kill the occupying process: `lsof -ti :8080 | xargs kill`

### Client gets "slot unavailable" error

**Fix:** The slot was already booked or the daily limit was reached. Check appointments and daily limit settings.

### Booking doesn't appear in appointments list

**Fix:** Ensure the server was running when the client booked. Submissions are only saved while the server is active.

---

## 9. Tips & Best Practices

**Set a realistic daily limit.** If your limit is 10 appointments per day but you only have 4 hours of availability with 30-minute slots, the effective limit is 8. Set the limit slightly higher than your actual slot count.

**Keep the server running only during booking windows.** Don't leave the server running indefinitely — stop it when you're not accepting new bookings to prevent unexpected appointments.

**Always contact clients to confirm.** The system doesn't send confirmation emails. After each booking, reach out to the client using their email address to confirm and send calendar details.

**Use separate booking pages for different service types.** Create one for "30-min intro call" and another for "60-min strategy session" — each with its own availability and duration settings.

**Review appointments each morning.** Run `appointments BOOK-ID` daily so you're never surprised by a booking you forgot about.
