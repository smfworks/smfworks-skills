# Morning Commute

> Get traffic, weather, and route info for your daily commute before you leave

---

## What It Does

Morning Commute delivers a quick briefing about your drive to work — current traffic conditions, estimated travel time, weather along your route, and any delays to watch out for. Perfect for figuring out when to leave without checking multiple apps.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install morning-commute
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Get your morning commute briefing:

```bash
python main.py commute
```

---

## Commands

### `commute`

**What it does:** Get your complete commute briefing with traffic and weather.

**Usage:**
```bash
python main.py commute [options]
```

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--home` | ❌ No | Home location | `--home "New York"` |
| `--work` | ❌ No | Work location | `--work "Boston"` |

**Example:**
```bash
python main.py commute
python main.py commute --home "New York" --work "Boston"
```

**Output:**
```
🚗 Morning Commute — March 25, 2026
==================================================

📍 Route: New York → Boston
   Distance: 215 miles
   Current travel time: 3h 45m (heavy traffic)

🚦 Traffic Conditions:
   I-95 N: Heavy traffic, 45 min delay expected
   I-90 E: Moderate traffic, normal flow
   Alternate route: I-84 E, 15 min longer but less traffic

🌤️ Weather Along Route:
   New York: ☀️ 58°F, Clear
   Hartford: 🌤️ 55°F, Partly cloudy
   Boston: 🌧️ 52°F, Light rain

💡 Recommendation:
   Leave by 7:30 AM to avoid worst traffic.
   Rain expected in Boston — allow extra travel time.

⏰ Suggested Departure: 7:30 AM
```

---

### `traffic`

**What it does:** Get current traffic conditions for your route.

**Usage:**
```bash
python main.py traffic
```

**Example:**
```bash
python main.py traffic
```

---

### `weather`

**What it does:** Get weather forecast for your commute.

**Usage:**
```bash
python main.py weather
```

**Example:**
```bash
python main.py weather
```

---

## Use Cases

- **Leave on time:** Know exactly when to depart based on traffic
- **Weekend trips:** Check conditions before a long drive
- **Alternative routes:** See if detour would save time
- **Weather prep:** Know if you need an umbrella or snow tires

---

## Tips & Tricks

- Set `--home` and `--work` once to skip typing each time
- Check traffic the night before to plan your morning
- Use before long trips to check weather along the route

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Location not recognized" | Try a more specific address |
| "Traffic unavailable" | Check internet connection |
| "API key needed" | Some features require Google Maps API key |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- (Optional) Google Maps API key for full traffic data

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/morning-commute)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
