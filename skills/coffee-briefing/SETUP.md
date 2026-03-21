# Coffee Briefing - Setup Guide

Complete setup guide for the Coffee Briefing Pro skill.

---

## Prerequisites

Before starting, ensure you have:

- [ ] SMF Works Pro subscription (active)
- [ ] Python 3.7+ installed
- [ ] OpenClaw installed and configured
- [ ] Internet connection

**Estimated setup time:** 15-20 minutes

---

## Step 1: Get OpenWeatherMap API Key (5 minutes)

### 1.1 Create Account

1. Go to **https://openweathermap.org/api**
2. Click "Sign Up" (top right)
3. Fill in:
   - Username
   - Email address
   - Password
4. Verify your email (check spam folder)

### 1.2 Get API Key

1. Log in to [https://home.openweathermap.org](https://home.openweathermap.org)
2. Go to **API Keys** tab
3. Copy the default key (long hex string)

**Important:** New API keys can take **10-15 minutes** to activate.

### 1.3 Test API Key

```bash
# Replace YOUR_API_KEY with your actual key
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY&units=imperial"
```

You should see JSON weather data.

---

## Step 2: Install the Skill (2 minutes)

```bash
# Install the skill
smf install coffee-briefing

# Verify installation
smf list | grep coffee-briefing
```

---

## Step 3: Run Configuration Wizard (5 minutes)

```bash
smf run coffee-briefing --configure
```

### 3.1 Enter Weather API Key

```
Step 1: OpenWeatherMap API Key
Get your free API key at: https://openweathermap.org/api
Free tier: 1,000 calls/day (sufficient for daily briefings)

Enter your OpenWeatherMap API key: YOUR_API_KEY_HERE
```

### 3.2 Set Your Location

```
Step 2: Your Location
City name [New York]: Pittsboro, NC
Units (imperial/metric) [imperial]: imperial
```

**For precise coordinates:**

1. Go to [https://www.latlong.net](https://www.latlong.net)
2. Enter your address
3. Note the latitude and longitude
4. Edit config directly:

```bash
nano ~/.config/smf/skills/coffee-briefing/config.json
```

Add coordinates:
```json
"location": {
  "city": "Pittsboro",
  "lat": 35.7204,
  "lon": -79.1772,
  "units": "imperial"
}
```

### 3.3 Configure Priorities

```
Step 3: Priorities Source
Options: auto (default), file

Source [auto]: auto
```

**Options:**
- `auto` - Generate priorities automatically
- `file` - Read from a text file

For file-based priorities:
```
Source: file
Path to priorities file: ~/Documents/Daily-Priorities.md
```

### 3.4 Complete Setup

```
Step 4: Schedule
Recommended: Run daily at 7:00 AM via OpenClaw cron

✅ Configuration saved to: ~/.config/smf/skills/coffee-briefing/config.json

Your Coffee Briefing is ready!
Run: smf run coffee-briefing
```

---

## Step 4: Test (2 minutes)

### 4.1 Run Briefing

```bash
smf run coffee-briefing
```

Expected output:
```
☕ Good Morning! Here's your briefing for Saturday, March 22, 2026

🌤️ Weather in Pittsboro, NC
   Current: 58°F, partly cloudy
   Feels like: 56°F
   High: 72°F | Low: 45°F

🎯 Top Priorities
   1. Review today's calendar and prepare
   2. Check messages and respond to urgent items
   3. Focus on your most important task

—
Powered by SMF Works Coffee Briefing ☕
Subscribe: https://smf.works/subscribe
```

---

## Step 5: Schedule Daily (5 minutes)

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

# Add this line for 7:00 AM daily
0 7 * * * /usr/local/bin/smf run coffee-briefing >> ~/.config/smf/skills/coffee-briefing/briefing.log 2>&1
```

---

## Configuration Reference

### Full Config File

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

---

## Troubleshooting

### "Pro skill requires SMF Works subscription"

**Problem:** No active subscription or token not found

**Solution:**
1. Subscribe at https://smf.works/subscribe
2. Run `smf login`
3. Check token exists: `ls -la ~/.smf/token`

### "Invalid weather API key"

**Problem:** API key not recognized

**Solution:**
1. Wait 10-15 minutes (new keys need activation)
2. Verify key in config
3. Test key directly with curl

### "Weather data unavailable"

**Problem:** Can't fetch weather

**Solution:**
- Check internet: `ping google.com`
- Verify coordinates are valid
- Try different city name

---

## Support

- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Weather API Help:** https://openweathermap.org/faq

---

**Setup complete! Enjoy your morning briefings ☕**
