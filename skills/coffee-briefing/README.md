# Coffee Briefing

> Get your personalized morning briefing — weather, calendar events, and news — delivered in one clean terminal output while you brew your coffee.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Requires:** OpenWeatherMap API key (free) + Google Calendar access  
**Version:** 1.0  
**Category:** Productivity / Daily Briefing

---

## What It Does

Coffee Briefing is an OpenClaw Pro skill that combines three data sources into a single morning brief: current weather and forecast (via OpenWeatherMap), today's calendar events (via Google Calendar), and curated news headlines. Run it each morning and get everything you need in under 30 seconds.

**What it does NOT do:** It does not send email, push notifications, read emails, check tasks, or provide sports scores.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **OpenWeatherMap API key** — free at [openweathermap.org/api](https://openweathermap.org/api)
- [ ] **Google Calendar API** configured (see SETUP.md)

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/coffee-briefing
python3 main.py --configure
```

---

## Quick Start

After configuration:

```bash
python3 main.py
```

Output:
```
☕ Good Morning! — Wednesday, March 15, 2024
═══════════════════════════════════════════

🌤️ Weather — New York, NY
   Currently: 54°F, Partly Cloudy
   Today: High 61°F / Low 48°F
   Tomorrow: Rain expected — bring an umbrella ☂️

📅 Today's Calendar
   09:00 AM — Team Standup (30 min)
   11:00 AM — Client Demo — Acme Corp (1 hr)
   02:00 PM — Budget Review (1 hr)
   06:30 PM — Dinner with Sarah

📰 Morning Headlines
   1. Fed Holds Rates Steady Amid Mixed Economic Data
   2. Apple Announces New Developer Tools at WWDC
   3. Climate Summit Reaches Landmark Agreement

Configure: smf run coffee-briefing --configure
```

---

## Command Reference

### Default (no arguments)

Generates and prints your morning briefing using saved configuration.

**Usage:**
```bash
python3 main.py
```

---

### `--configure` / `-c`

Interactive setup wizard. Prompts for your location, OpenWeatherMap API key, Google Calendar credentials, and preferred briefing settings.

**Usage:**
```bash
python3 main.py --configure
```

---

### `--output json` / `-o json`

Outputs the briefing as JSON instead of formatted text.

**Usage:**
```bash
python3 main.py --output json
```

---

## Use Cases

### 1. Daily morning routine

Schedule via cron at 7 AM — see HOWTO.md for setup.

### 2. Briefing before an important day

```bash
python3 main.py
```

Quickly see: what's the weather (do I need a coat?), what meetings are coming up, and what's in the news.

### 3. Save to file for offline reading

```bash
python3 main.py > ~/briefing-$(date +%Y-%m-%d).txt
```

---

## Configuration

Config file: `~/.config/smf/skills/coffee-briefing/config.json`

| Setting | Description |
|---------|-------------|
| `openweathermap_api_key` | Your free OWM API key |
| `location` | City name or coordinates |
| `temperature_unit` | `imperial` (°F) or `metric` (°C) |
| `google_calendar_credentials` | Path to OAuth credentials file |
| `news_categories` | Categories to include in headlines |

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Error: OpenWeatherMap API key not configured`
**Fix:** Run `python3 main.py --configure` and enter your free OWM key.

### `Error: Google Calendar not configured`
**Fix:** See SETUP.md for Google Calendar OAuth setup.

### `City not found` (weather error)
**Fix:** Try a major nearby city name, or use `City,CountryCode` format: `London,GB`

### Weather shows but Calendar is empty
**Fix:** Verify your Google Calendar has events for today. Check the calendar name in config matches exactly.

---

## FAQ

**Q: Does this cost extra beyond the Pro subscription?**  
A: No. OpenWeatherMap's free tier (60 calls/minute) is more than sufficient. Google Calendar API has a free quota that covers personal use.

**Q: Can I add my own news source?**  
A: News categories are configurable via `--configure`. Custom sources require editing the config file directly.

**Q: Can I see tomorrow's weather?**  
A: Yes — the briefing includes tomorrow's forecast in the weather section.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| OpenWeatherMap API | Free tier |
| Google Calendar | OAuth credentials required |
| Internet | Required |

---

---

## Automation

Schedule your briefing to run automatically every morning:

```bash
# Add to crontab (crontab -e)
0 7 * * 1-5 cd /home/yourname/smfworks-skills/skills/coffee-briefing && python3 main.py > /home/yourname/Briefings/briefing-$(date +\%Y-\%m-\%d).txt 2>&1
```

Or add it to your shell startup for a briefing every time you open a terminal:

```bash
# Add to ~/.bashrc or ~/.zshrc
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
```

---

## Combining with Other Skills

**Coffee Briefing + Morning Commute:** Full morning picture — weather, calendar, and commute times:

```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

**Coffee Briefing + Task Manager:** See your day's meetings and your task board together:

```bash
python3 main.py
python3 ~/smfworks-skills/skills/task-manager/main.py board
```

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/coffee-briefing)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
