# Booking Engine — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |
| Web browser | For accessing the booking form | Free |

---

## Step 1 — Subscribe and Authenticate

```bash
openclaw auth status
```

If not subscribed: [smfworks.com/subscribe](https://smfworks.com/subscribe)

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate and Verify

```bash
cd ~/smfworks-skills/skills/booking-engine
python3 main.py help
```

---

## Verify Your Setup

**Step 1 — Create a booking page:**

```bash
python3 main.py create
```

Follow the prompts (enter a name, duration, etc.).

Note the BOOK-ID in the output (e.g., `BOOK-A1B2C3`).

**Step 2 — Add some availability:**

```bash
python3 main.py availability BOOK-A1B2C3 --add monday:09:00-17:00
python3 main.py availability BOOK-A1B2C3 --add tuesday:09:00-17:00
```

**Step 3 — Start the server:**

```bash
python3 main.py serve BOOK-A1B2C3 --port 8080
```

**Step 4 — Open in browser:**

Go to `http://localhost:8080/BOOK-A1B2C3`

You should see a booking page with a calendar showing available Monday and Tuesday slots.

**Step 5 — Test a booking (optional):**

Select a time slot, enter a name and email, submit.

**Step 6 — Stop the server (Ctrl+C) and verify:**

```bash
python3 main.py appointments BOOK-A1B2C3
```

Your test appointment should appear.

---

## Availability Format

Availability is added per-day:

```bash
python3 main.py availability BOOK-ID --add WEEKDAY:START-END
```

| Day | Format |
|-----|--------|
| Monday | `monday:09:00-17:00` |
| Tuesday | `tuesday:10:00-15:00` |
| Wednesday | `wednesday:09:00-12:00` |
| Thursday | `thursday:14:00-18:00` |
| Friday | `friday:09:00-16:00` |

Use 24-hour format for times.

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**No time slots on booking page** — Add availability first with `availability --add`.

**`Address already in use`** — Use a different port: `--port 8090`.

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on creating booking pages, managing availability, and handling appointments.
