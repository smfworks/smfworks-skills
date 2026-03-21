# Coffee Briefing - SMF Works Pro Skill

☕ **Your personal morning briefing with weather, calendar, and priorities.**

## Overview

Coffee Briefing delivers a beautifully formatted morning briefing that includes:
- 🌤️ **Weather** - Current conditions and forecast for your location
- 📅 **Calendar** - Today's events from Google Calendar (optional)
- 🎯 **Priorities** - Top 3 priorities from your Next-Actions file or auto-generated

**Schedule:** Daily at 7:00 AM (configurable)
**Tier:** Pro (requires SMF Works subscription)

---

## Requirements

- **SMF Works Subscription:** Pro tier ($19.99/mo)
- **OpenWeatherMap API Key:** Free tier (see setup below)
- **Python 3.7+** with standard library
- **Optional:** Google Calendar OAuth (for calendar integration)

---

## API Dependencies

### 1. OpenWeatherMap API (Required)

**Purpose:** Weather data

**Setup:**
1. Go to **https://openweathermap.org/api**
2. Click "Sign Up" (top right)
3. Create free account
4. Copy your API key from dashboard

**Pricing:**
- Free tier: 1,000 calls/day (plenty for daily briefings)
- Paid tiers: Available for higher volume

**Data Provided:**
- Current temperature
- Feels like temperature
- High/low for the day
- Weather conditions
- City name

### 2. Google Calendar API (Optional)

**Purpose:** Calendar events in briefing

**Setup:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project → Enable Google Calendar API
3. Configure OAuth consent screen
4. Create OAuth credentials (Desktop app)
5. Download `client_secret.json`

**Pricing:**
- Free tier: 1,000,000 requests/day
- Personal use: Free

**Note:** Calendar integration is optional. The skill works great with just weather and priorities.

---

## Installation

```bash
# Install via SMF CLI
smf install coffee-briefing
```

---

## Quick Start

### Step 1: Get Weather API Key

```bash
# Visit the registration page
open https://openweathermap.org/api
```

Or manually:
1. Go to **https://openweathermap.org/api**
2. Create free account
3. Copy your API key

**Important:** New API keys take 10-15 minutes to activate.

### Step 2: Configure

```bash
smf run coffee-briefing --configure
```

Follow the prompts:
- Enter your OpenWeatherMap API key
- Set your location (city name)
- Choose temperature units (imperial/metric)
- Configure priorities source

### Step 3: Test

```bash
smf run coffee-briefing
```

---

## Configuration

### Configuration File Location

```
~/.config/smf/skills/coffee-briefing/config.json
```

### Example Configuration

```json
{
  "weather_api_key": "your_openweathermap_api_key_here",
  "location": {
    "city": "Pittsboro",
    "lat": 35.7204,
    "lon": -79.1772,
    "units": "imperial"
  },
  "priorities": {
    "source": "auto",
    "file_path": "",
    "max_priorities": 3
  }
}
```

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `weather_api_key` | Yes | "" | OpenWeatherMap API key |
| `location.city` | Yes | "New York" | City name for display |
| `location.lat` | No | 40.7128 | Latitude (auto-detected) |
| `location.lon` | No | -74.0060 | Longitude (auto-detected) |
| `location.units` | No | "imperial" | imperial (°F) or metric (°C) |
| `priorities.source` | No | "auto" | auto or file |
| `priorities.file_path` | No | "" | Path to priorities file |

---

## Scheduling

### OpenClaw Cron (Recommended)

```bash
# Add daily at 7:00 AM
openclaw cron add \
  --name "coffee-briefing" \
  --schedule "0 7 * * *" \
  --command "smf run coffee-briefing"
```

### System Cron

```bash
# Edit crontab
crontab -e

# Add for 7:00 AM daily
0 7 * * * /usr/local/bin/smf run coffee-briefing >> ~/.config/smf/skills/coffee-briefing/briefing.log 2>&1
```

### OpenClaw Heartbeat

Add to your `HEARTBEAT.md`:

```markdown
## Morning Tasks (7:00 AM)

- [ ] Run Coffee Briefing
- [ ] Review calendar
- [ ] Check priorities
```

---

## Usage

### Run Once

```bash
# Generate today's briefing
smf run coffee-briefing

# Output as JSON
smf run coffee-briefing --output json

# Test without subscription check
smf run coffee-briefing --test-mode
```

### Reconfigure

```bash
smf run coffee-briefing --configure
```

---

## Example Output

```
☕ Good Morning! Here's your briefing for Saturday, March 22, 2026

🌤️ Weather in Pittsboro, NC
   Current: 58°F, partly cloudy
   Feels like: 56°F
   High: 72°F | Low: 45°F

📅 Calendar not configured (optional)

🎯 Top Priorities
   1. Review today's calendar and prepare
   2. Check messages and respond to urgent items
   3. Focus on your most important task

—
Powered by SMF Works Coffee Briefing ☕
Configure: smf run coffee-briefing --configure
Subscribe: https://smf.works/subscribe
```

---

## Priorities Configuration

### Automatic (Default)

The skill generates intelligent priorities based on:
- Day of the week
- Time of day
- Calendar events (if configured)

### From File

Create a priorities file:

```bash
mkdir -p ~/Documents
cat > ~/Documents/Daily-Priorities.md << 'EOF'
# Today's Priorities

1. Finish Coffee Briefing skill
2. Review Stripe implementation
3. Push updates to GitHub
EOF
```

Then configure:

```json
"priorities": {
  "source": "file",
  "file_path": "~/Documents/Daily-Priorities.md"
}
```

---

## Troubleshooting

### "Pro skill requires SMF Works subscription"

**Problem:** No active subscription

**Solution:**
1. Subscribe at [https://smf.works/subscribe](https://smf.works/subscribe)
2. Run `smf login`
3. Verify token: `ls ~/.smf/token`

### "Invalid weather API key"

**Problem:** API key not recognized

**Solution:**
1. Wait 10-15 minutes (new keys need activation)
2. Verify key at [https://home.openweathermap.org/api_keys](https://home.openweathermap.org/api_keys)
3. Test directly:
   ```bash
   curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY&units=imperial"
   ```

### "Weather data unavailable"

**Problem:** Can't fetch weather

**Solution:**
- Check internet connection
- Verify city name is valid
- Check OpenWeatherMap status

### Config file not found

```bash
# Recreate config
mkdir -p ~/.config/smf/skills/coffee-briefing
smf run coffee-briefing --configure
```

---

## Data & Privacy

- **Weather data:** Fetched from OpenWeatherMap (your API key)
- **Calendar data:** Optional, never stored by SMF Works
- **Config file:** Stored locally with 600 permissions
- **Subscription:** Validated locally via JWT token

---

## Support

- **Documentation:** https://smfworks.com/skills/coffee-briefing
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **OpenWeatherMap:** https://openweathermap.org/faq
- **Google Calendar:** https://developers.google.com/calendar

---

## Related Skills

- **Daily News Digest** - Get curated news headlines
- **Morning Commute** - Traffic and transit updates
- **Meeting Prep** - Research attendees and generate talking points

---

*Powered by SMF Works | Pro Skill | Local-First*
