# Morning Commute - SMF Works Pro Skill

🚗 **Your daily commute briefing with traffic, transit, and weather.**

## Overview

Morning Commute delivers a complete commute briefing that includes:
- 🌤️ **Weather** - Current conditions at your home location
- 🚗 **Traffic** - Route time with estimated delays
- ⏰ **Departure Alert** - When to leave to arrive on time
- 🚌 **Transit** - Public transit options (optional)

**Schedule:** Weekday mornings at 6:30 AM (configurable)
**Tier:** Pro (requires SMF Works subscription)

---

## Requirements

- **SMF Works Subscription:** Pro tier ($19.99/mo)
- **Home & Work Addresses** - For route calculation
- **OpenWeatherMap API Key** - Free tier (optional but recommended)
- **Optional:** Google Maps API key for accurate traffic

---

## API Dependencies

### 1. OpenStreetMap Nominatim (Required)

**Purpose:** Address geocoding (convert addresses to coordinates)

**Source:** https://nominatim.openstreetmap.org

**Pricing:**
- Free (no API key required)
- Usage policy: Be respectful, cache results
- Rate limit: 1 request/second

**Data Provided:**
- Latitude/longitude for addresses
- Used for routing calculations

### 2. OSRM - Open Source Routing Machine (Required)

**Purpose:** Route calculation and drive time estimates

**Source:** http://project-osrm.org

**Pricing:**
- Free demo server available
- For production: Self-host or use paid routing service

**Data Provided:**
- Drive time between two points
- Distance in miles/km
- Basic route geometry

**Note:** Traffic estimates are approximate. For accurate real-time traffic, see Google Maps API option below.

### 3. OpenWeatherMap API (Optional)

**Purpose:** Current weather at your location

**Setup:**
1. Go to **https://openweathermap.org/api**
2. Sign up for free account
3. Copy API key

**Pricing:**
- Free tier: 1,000 calls/day
- Sufficient for daily briefings

**Data Provided:**
- Current temperature
- Weather conditions
- Feels-like temperature

### 4. Google Maps Directions API (Optional)

**Purpose:** Accurate real-time traffic data

**Setup:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Directions API
3. Create API key

**Pricing:**
- Free tier: $200 credit/month (~40,000 requests)
- Typical usage: 1 request/day
- Cost: Free for personal use

**Note:** This is optional. Without it, the skill uses OSRM with heuristic traffic estimates.

---

## Installation

```bash
# Install via SMF CLI
smf install morning-commute
```

---

## Quick Start

### Step 1: Configure the Skill

```bash
smf run morning-commute --configure
```

The wizard will ask for:
- Home address
- Work address
- OpenWeatherMap API key (optional)
- Departure/arrival time
- Units (imperial/metric)

### Step 2: Test

```bash
smf run morning-commute
```

---

## Configuration

### Configuration File Location

```
~/.config/smf/skills/morning-commute/config.json
```

### Example Configuration

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
  "departure_time": "08:00",
  "mode": "driving",
  "units": "imperial",
  "alert_threshold_minutes": 10
}
```

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `home_location.address` | Yes | "" | Your home address |
| `home_location.lat` | Auto | 0.0 | Home latitude (auto-geocoded) |
| `home_location.lon` | Auto | 0.0 | Home longitude (auto-geocoded) |
| `work_location.address` | Yes | "" | Your work address |
| `work_location.lat` | Auto | 0.0 | Work latitude (auto-geocoded) |
| `work_location.lon` | Auto | 0.0 | Work longitude (auto-geocoded) |
| `weather_api_key` | No | "" | OpenWeatherMap API key |
| `departure_time` | No | "08:00" | Target arrival time (24h) |
| `mode` | No | "driving" | driving, transit, walking |
| `units` | No | "imperial" | imperial (mi) or metric (km) |
| `alert_threshold_minutes` | No | 10 | Alert if delay exceeds this |

---

## Scheduling

### OpenClaw Cron (Recommended)

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

### OpenClaw Heartbeat

Add to your `HEARTBEAT.md`:

```markdown
## Weekday Morning (6:30 AM)

- [ ] Run Morning Commute briefing
- [ ] Check traffic and leave on time
```

---

## Usage

### Run Once

```bash
# Generate commute briefing
smf run morning-commute

# Output as JSON
smf run morning-commute --output json

# Test without subscription check
smf run morning-commute --test-mode
```

### Reconfigure

```bash
smf run morning-commute --configure
```

---

## Example Output

```
🚗 Morning Commute Briefing — Monday, March 24, 2026

🌤️ 58°F, partly cloudy

🚗 Commute: 28 min (15.2 mi)
   ⚠️  Traffic delay: +8 min
   Normal time: 20 min

⏰ Departure Alert
   Target arrival: 08:00
   Leave by: 07:22

—
Powered by SMF Works Morning Commute
Configure: smf run morning-commute --configure
Subscribe: https://smf.works/subscribe
```

---

## Troubleshooting

### "Pro skill requires SMF Works subscription"

**Problem:** No active subscription

**Solution:**
1. Subscribe at [https://smf.works/subscribe](https://smf.works/subscribe)
2. Run `smf login`
3. Verify token: `ls ~/.smf/token`

### "Could not geocode address"

**Problem:** Address lookup failed

**Solution:**
1. Try simpler address ("123 Main St, City, State")
2. Check internet connection
3. Manually add coordinates to config:
   ```json
   "home_location": {
     "address": "Your Address",
     "lat": 35.7204,
     "lon": -79.1772
   }
   ```

### "Route info unavailable"

**Problem:** OSRM routing failed

**Solution:**
- Check that home/work coordinates are set
- OSRM demo server may be down (try again later)
- Consider self-hosting OSRM for reliability

### "Weather unavailable"

**Problem:** Can't fetch weather

**Solution:**
- Check OpenWeatherMap API key
- Wait 10-15 min if key is new
- Verify key at [home.openweathermap.org](https://home.openweathermap.org/api_keys)

---

## Data & Privacy

- **Addresses:** Stored locally in config file
- **Coordinates:** Used for routing only, not sent to SMF Works
- **Weather:** Fetched from OpenWeatherMap (your API key)
- **Routing:** Uses OSRM (open source, no tracking)
- **Subscription:** Validated locally via JWT token

---

## Support

- **Documentation:** https://smfworks.com/skills/morning-commute
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **OpenStreetMap:** https://operations.osmfoundation.org/policies/nominatim/
- **OSRM:** http://project-osrm.org/docs/

---

## Related Skills

- **Coffee Briefing** - Weather and priorities
- **Daily News Digest** - Curated news headlines
- **Meeting Prep** - Research and talking points

---

*Powered by SMF Works | Pro Skill | Local-First*
