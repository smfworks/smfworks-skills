# Coffee Briefing

> Your personalized morning briefing — news, weather, tasks, and insights while your coffee brews

---

## What It Does

Coffee Briefing delivers a customized morning summary right when you need it — while your coffee is brewing. It gathers your calendar, weather, top news headlines, task reminders, and any custom notes you've added, presenting them in a clean digest you can read in under a minute.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install coffee-briefing
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Get your personalized morning briefing:

```bash
python main.py briefing
```

---

## Commands

### `briefing`

**What it does:** Generate your complete morning briefing with weather, news, calendar, and tasks.

**Usage:**
```bash
python main.py briefing [date]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `date` | ❌ No | Date for briefing (YYYY-MM-DD, default: today) | `2026-03-25` |

**Example:**
```bash
python main.py briefing
python main.py briefing 2026-03-25
```

**Output:**
```
☕ Good morning! Here's your briefing for March 25, 2026:

📅 TODAY'S SCHEDULE
------------------------------------------------------------
9:00 AM  - Team standup meeting
11:00 AM - Client call: Smith Industries
2:00 PM  - Project review

🌤️ WEATHER (New York)
------------------------------------------------------------
Currently: 58°F, Partly Cloudy
High: 65°F | Low: 52°F
Perfect day for a walk!

📰 TOP NEWS
------------------------------------------------------------
1. Tech stocks rally on AI demand (Bloomberg)
2. New renewable energy breakthrough (Reuters)
3. Local events this weekend (Local News)

✅ YOUR TASKS
------------------------------------------------------------
• Review Q1 sales report
• Send follow-up emails
• Schedule team 1:1s

💡 INSIGHTS
------------------------------------------------------------
"Focus on progress, not perfection." — Your daily reminder

Have a great day! ☕
```

---

### `config`

**What it does:** Configure your briefing preferences, location, and API keys.

**Usage:**
```bash
python main.py config
```

**Example:**
```bash
python main.py config
```

**Output:**
```
⚙️  Briefing Configuration
==================================================

Location for weather [New York]:
News categories [technology, business, local]:
API Keys:
  OpenWeatherMap: ✅ Set
  News API: ✅ Set
  Calendar: ✅ Set

✅ Configuration saved!
```

---

### `add`

**What it does:** Add a custom item to your daily briefing.

**Usage:**
```bash
python main.py add "Your reminder text"
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `text` | ✅ Yes | The reminder or note to add | `Review contracts` |

**Example:**
```bash
python main.py add "Review Q1 sales report"
python main.py add "Call mom on her birthday"
python main.py add "Pick up dry cleaning"
```

**Output:**
```
✅ Added to briefing: "Review Q1 sales report"
```

---

### `list`

**What it does:** View all items queued for your briefing.

**Usage:**
```bash
python main.py list
```

**Example:**
```bash
python main.py list
```

**Output:**
```
📋 Your Briefing Items:
------------------------------------------------------------
1. Review Q1 sales report
2. Send follow-up emails
3. Schedule team 1:1s
4. Pick up dry cleaning
```

---

### `weather`

**What it does:** Get just the weather forecast without full briefing.

**Usage:**
```bash
python main.py weather
```

**Example:**
```bash
python main.py weather
```

**Output:**
```
🌤️ Weather for New York:
   Currently: 58°F, Partly Cloudy
   Feels like: 56°F
   High: 65°F | Low: 52°F
   Wind: 8 mph NW
   Humidity: 65%
```

---

### `news`

**What it does:** Get just the news headlines without full briefing.

**Usage:**
```bash
python main.py news
```

**Example:**
```bash
python main.py news
```

**Output:**
```
📰 Top News Headlines:
------------------------------------------------------------
1. Tech stocks rally on AI demand - Bloomberg
2. New renewable energy breakthrough - Reuters
3. Fed signals rate decision - WSJ
4. Weekend forecast looks great - Weather.com
```

---

## Use Cases

- **Morning routine:** Start your day informed and organized
- **Productivity boost:** See all your tasks and appointments at a glance
- **Weather check:** Know if you need an umbrella or sunglasses
- **News catchup:** Stay informed without doom-scrolling
- **Meeting prep:** See your day's schedule before heading out

---

## Tips & Tricks

- Add items the night before: `python main.py add "Prepare slides"`
- Use cron to auto-generate at 7 AM daily: `0 7 * * * python main.py briefing`
- Configure multiple locations if you travel frequently
- Set preferred news categories to filter out noise

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not set" | Run `python main.py config` to enter your keys |
| "Weather unavailable" | Check your internet connection or API quota |
| Empty briefing | Add items with `python main.py add "Your task"` |
| Wrong location | Re-run `python main.py config` to update |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- (Optional) OpenWeatherMap API key for weather
- (Optional) News API key for headlines

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/coffee-briefing)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
