# Coffee Briefing — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. OpenWeatherMap key configured. Google Calendar connected. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Get Your Morning Briefing](#1-how-to-get-your-morning-briefing)
2. [How to Customize Your Briefing](#2-how-to-customize-your-briefing)
3. [How to Save Your Briefing to a File](#3-how-to-save-your-briefing-to-a-file)
4. [How to Get JSON Output for Scripts](#4-how-to-get-json-output-for-scripts)
5. [Automating with Cron](#5-automating-with-cron)
6. [Combining with Other Skills](#6-combining-with-other-skills)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)
8. [Tips & Best Practices](#8-tips--best-practices)

---

## 1. How to Get Your Morning Briefing

**What this does:** Fetches current weather, today's calendar events, and top news headlines and prints them in a clean, readable format.

**When to use it:** Every morning as the first thing you run.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/coffee-briefing
```

**Step 2 — Run the briefing.**

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
   Tomorrow: Rain expected ☂️

📅 Today's Calendar
   09:00 AM — Team Standup (30 min)
   11:00 AM — Client Demo — Acme Corp (1 hr)
   02:00 PM — Budget Review (1 hr)
   06:30 PM — Dinner with Sarah

📰 Morning Headlines
   1. Fed Holds Rates Steady
   2. Apple Announces Developer Tools at WWDC
   3. Climate Summit Reaches Agreement

Configure: smf run coffee-briefing --configure
```

**Step 3 — Use the information.**

- Weather helps you decide what to wear and whether to commute differently
- Calendar gives you your day's agenda at a glance
- Headlines keep you informed before your first meeting

**Result:** Everything you need for the morning in one 10-second command.

---

## 2. How to Customize Your Briefing

**What this does:** Re-runs the configuration wizard to update any setting.

**When to use it:** You've moved cities, changed calendars, or want different news categories.

### Steps

```bash
python3 main.py --configure
```

Follow the prompts to update:
- City/location
- Temperature unit (F vs C)
- Google Calendar credentials
- News categories

After saving, run `python3 main.py` to see the updated briefing.

---

## 3. How to Save Your Briefing to a File

**When to use it:** You want to review the briefing later, archive it, or read it offline.

```bash
python3 main.py > ~/Briefings/briefing-$(date +%Y-%m-%d).txt
```

View it later:
```bash
cat ~/Briefings/briefing-2024-03-15.txt
```

---

## 4. How to Get JSON Output for Scripts

**When to use it:** You want to process the briefing programmatically or pipe it to another tool.

```bash
python3 main.py --output json
```

Output:
```json
{
  "success": true,
  "timestamp": "2024-03-15T07:00:12",
  "content": "☕ Good Morning!...",
  "weather": {...},
  "calendar": [...],
  "news": [...]
}
```

---

## 5. Automating with Cron

Schedule your briefing to be generated and saved every morning automatically.

### Open crontab

```bash
crontab -e
```

### Example: Generate briefing every weekday at 7 AM

```bash
0 7 * * 1-5 cd /home/yourname/smfworks-skills/skills/coffee-briefing && python3 main.py > /home/yourname/Briefings/briefing-$(date +\%Y-\%m-\%d).txt 2>&1
```

### Example: Print briefing to terminal at login

Add to your `~/.bashrc` or `~/.zshrc`:
```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 7 * * 1-5` | Weekdays at 7 AM |
| `0 6 * * *` | Every day at 6 AM |
| `30 7 * * *` | Every day at 7:30 AM |

---

## 6. Combining with Other Skills

**Coffee Briefing + Morning Commute:** Get weather and calendar from Coffee Briefing, plus commute times from Morning Commute:

```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

**Coffee Briefing + Daily News Digest:** Coffee Briefing gives a short headline summary; Daily News Digest gives more depth. Run both for comprehensive coverage.

**Coffee Briefing + Task Manager:** See your calendar events from Coffee Briefing, then check your task board:

```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
python3 ~/smfworks-skills/skills/task-manager/main.py board
```

---

## 7. Troubleshooting Common Issues

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe) and re-authenticate OpenClaw.

### `Error: OpenWeatherMap API key not configured`
**Fix:** Run `python3 main.py --configure`.

### Weather section shows but Calendar is blank
**Fix:** 1) Verify today's calendar has events. 2) Check the Google Calendar credentials are still valid. 3) Re-run `--configure` if the OAuth token has expired.

### `401 Unauthorized` from weather API
**Fix:** New OWM keys take up to 2 hours to activate. Also check the key is correctly saved in config.

### Google Calendar authorization expired
**Fix:** Delete the stored OAuth token (usually in `~/.config/smf/skills/coffee-briefing/`) and re-run `python3 main.py` to trigger re-authorization.

---

## 8. Tips & Best Practices

**Run it before you open your email.** Starting your day with weather, calendar, and headlines before hitting your inbox sets a clearer frame for your priorities.

**Add it to your shell startup.** Adding `python3 ~/smfworks-skills/skills/coffee-briefing/main.py` to `~/.bashrc` or `~/.zshrc` means you get your briefing the moment you open a terminal.

**Use the JSON output with jq for filtering.** If you only want the calendar section: `python3 main.py --output json | python3 -c "import json,sys; [print(e) for e in json.load(sys.stdin).get('calendar',[])]"`

**Check weather before long commutes or outdoor meetings.** The "Tomorrow" forecast in the weather section is especially useful for planning the next day's attire or commute method.
