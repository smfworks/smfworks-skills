# Morning Commute - Setup Guide

Complete setup guide for the Morning Commute Pro skill.

---

## Prerequisites

Before starting, ensure you have:

- [ ] SMF Works Pro subscription (active)
- [ ] Python 3.7+ installed
- [ ] Home and work addresses
- [ ] Internet connection

**Estimated setup time:** 15-20 minutes

---

## Step 1: Install the Skill (2 minutes)

```bash
# Install via SMF CLI
smf install morning-commute

# Verify installation
smf list | grep morning-commute
```

---

## Step 2: Run Configuration Wizard (10 minutes)

```bash
smf run morning-commute --configure
```

### 2.1 Enter Home Address

```
Step 1: Home Location
Enter your home address (e.g., '123 Main St, Pittsboro, NC')

Home address: 123 Main St, Pittsboro, NC
Geocoding address...
✅ Found: 35.7204, -79.1772
```

**Tips:**
- Use full address with city and state
- If geocoding fails, try simpler format
- You can manually add coordinates later

### 2.2 Enter Work Address

```
Step 2: Work Location
Enter your work address

Work address: 456 Corporate Dr, Durham, NC
Geocoding address...
✅ Found: 35.9940, -78.8986
```

### 2.3 Weather API (Optional)

```
Step 3: Weather API (Optional)
Get free API key at: https://openweathermap.org/api
Adds current conditions to your briefing

OpenWeatherMap API key (press Enter to skip): YOUR_API_KEY
```

**To get weather API key:**
1. Go to https://openweathermap.org/api
2. Click "Sign Up"
3. Verify email
4. Copy API key from dashboard
5. **Wait 10-15 minutes** for key to activate

### 2.4 Departure Settings

```
Step 4: Departure Settings
Target arrival time (HH:MM, 24h) [08:00]: 09:00
Units (imperial/metric) [imperial]: imperial
```

**Options:**
- **imperial** - Miles, Fahrenheit
- **metric** - Kilometers, Celsius

### 2.5 Schedule

```
Step 5: Schedule
Recommended: Run weekday mornings at 6:30 AM
Command: openclaw cron add --name 'morning-commute' --schedule '30 6 * * 1-5' --command 'smf run morning-commute'

✅ Configuration saved to: ~/.config/smf/skills/morning-commute/config.json

Your Morning Commute briefing is ready!
Run: smf run morning-commute
```

---

## Step 3: Test (2 minutes)

### 3.1 Run Briefing

```bash
smf run morning-commute
```

Expected output:
```
🚗 Morning Commute Briefing — Monday, March 24, 2026

🌤️ 58°F, partly cloudy

🚗 Commute: 28 min (15.2 mi)
   ⚠️  Traffic delay: +8 min
   Normal time: 20 min

⏰ Departure Alert
   Target arrival: 09:00
   Leave by: 08:22

—
Powered by SMF Works Morning Commute
Configure: smf run morning-commute --configure
Subscribe: https://smf.works/subscribe
```

---

## Step 4: Schedule Daily (5 minutes)

### OpenClaw Cron

```bash
# Weekday mornings at 6:30 AM
openclaw cron add \
  --name "morning-commute" \
  --schedule "30 6 * * 1-5" \
  --command "smf run morning-commute"
```

### System Cron

```bash
# Edit crontab
crontab -e

# Add for 6:30 AM weekdays only
30 6 * * 1-5 /usr/local/bin/smf run morning-commute
```

---

## Configuration Reference

### Full Config File

```json
{
  "home_location": {
    "address": "123 Main St, Pittsboro, NC",
    "lat": 35.7204,
    "lon": -79.1772
  },
  "work_location": {
    "address": "456 Corporate Dr, Durham, NC",
    "lat": 35.9940,
    "lon": -78.8986
  },
  "weather_api_key": "your_openweathermap_api_key",
  "departure_time": "09:00",
  "units": "imperial"
}
```

### Manual Coordinate Entry

If geocoding fails:

1. Find coordinates at https://www.latlong.net
2. Edit config: `nano ~/.config/smf/skills/morning-commute/config.json`
3. Update with lat/lon values

---

## Troubleshooting

### "Could not geocode address"

- Try simpler address format
- Manually add coordinates (see above)
- Check internet connection

### "Route info unavailable"

- OSRM demo server may be down (try again later)
- Verify coordinates are set in config

### "Weather unavailable"

- Wait 10-15 minutes if key is new
- Test key: `curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY&units=imperial"`

---

## Support

- Issues: https://github.com/smfworks/smfworks-skills/issues
- OpenStreetMap: https://operations.osmfoundation.org/policies/nominatim/
- OSRM: http://project-osrm.org/
- Weather API: https://openweathermap.org/faq

---

**Setup complete! Safe travels 🚗**
