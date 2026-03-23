# Morning Commute

> Get real-time traffic conditions, transit times, and commute alerts for your daily route — before you leave the house.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Requires:** Google Maps API key (free tier available)  
**Version:** 1.0  
**Category:** Productivity / Daily Briefing

---

## What It Does

Morning Commute is an OpenClaw Pro skill that checks your commute route using the Google Maps Directions API and delivers a clear commute briefing: estimated travel time, traffic conditions, transit options, and any alerts for your saved route. Configure your home and work addresses once, set your departure time, and get a personalized daily commute report.

**What it does NOT do:** It does not track live vehicle positions, provide turn-by-turn navigation, monitor specific transit lines for delays, or send push notifications.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **Google Maps API key** — see SETUP.md for instructions

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/morning-commute
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
🚗 Morning Commute Briefing — Wednesday, March 15, 2024
Departure: 8:00 AM
═══════════════════════════════════════════════════════

📍 Route: Home → Acme Corp HQ
   Distance: 12.3 miles

🚗 Driving
   Typical time: 28 min
   Current time: 42 min ⚠️ (heavy traffic on I-95 N)
   Estimated arrival: 8:42 AM
   Recommendation: Leave now or delay 30 min

🚇 Transit
   Next departure: 8:07 AM (Bus #42)
   Estimated arrival: 8:51 AM (via Downtown station)

Configure: smf run morning-commute --configure
```

---

## Command Reference

### Default (no arguments)

Generates and prints your commute briefing using saved configuration.

```bash
python3 main.py
```

---

### `--configure` / `-c`

Interactive setup wizard for home address, work address, departure time, and Google Maps API key.

```bash
python3 main.py --configure
```

Configuration prompts:
- Home address
- Work/destination address
- Preferred departure time
- Google Maps API key
- Travel mode preference (driving, transit, walking, bicycling)

---

## Use Cases

### 1. Daily check before leaving

```bash
python3 main.py
```

Know before you leave whether traffic is light or heavy — and whether to take an alternate route or public transit.

---

### 2. Schedule automated morning alert

Via cron, generate the briefing at 7 AM so it's ready when you wake up:

```bash
0 7 * * 1-5 python3 /home/yourname/smfworks-skills/skills/morning-commute/main.py > /home/yourname/commute-$(date +\%Y-\%m-\%d).txt 2>&1
```

---

### 3. Combine with Coffee Briefing

Run both for a complete morning overview:

```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

---

## Configuration

Config file: `~/.config/smf/skills/morning-commute/config.json`

| Setting | Description |
|---------|-------------|
| `google_maps_api_key` | Your Google Maps API key |
| `home_address` | Your starting address |
| `work_address` | Your destination address |
| `departure_time` | Preferred departure (e.g., `"08:00"`) |
| `travel_mode` | `driving`, `transit`, `walking`, or `bicycling` |

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Error: Google Maps API key not configured`
**Fix:** Run `python3 main.py --configure`.

### `REQUEST_DENIED` from Google Maps
**Fix:** Your API key doesn't have the Directions API enabled. Go to Google Cloud Console → APIs → Enable "Directions API".

### `ZERO_RESULTS` — no route found
**Fix:** Verify your home and work addresses are valid. Try full street addresses with city and ZIP.

### Commute shows driving only, no transit
**Fix:** Not all locations have transit data. Try setting `travel_mode: transit` in config.

---

## FAQ

**Q: How much does the Google Maps API cost?**  
A: Google provides a $200/month free credit. A daily commute check uses roughly $0.005 per request (2 requests/day = $0.30/month) — well within the free tier.

**Q: Can I check multiple routes?**  
A: One route per configuration. To check multiple routes, run `--configure` to change the destination, or edit the config file directly.

**Q: Can I check the commute for a future time?**  
A: The skill checks traffic conditions for your configured departure time. Checking specific future times requires editing the config.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| Google Maps API | Free tier (Directions API enabled) |
| Internet | Required |

---

## Detailed Output Breakdown

### Route Summary
Shows your configured origin and destination addresses, and the total distance. This confirms you're checking the right route before acting on the data.

### Driving Section
- **Typical time:** What Google Maps estimates without traffic
- **Current time:** Real-time estimate with current traffic conditions
- **Estimated arrival:** When you'll arrive if you leave now
- **Recommendation:** If current time significantly exceeds typical, you'll see a recommendation to leave now or wait

### Transit Section
Shows the next departure time and estimated arrival for public transit on your route. Only appears if transit data is available for your location.

---

## Automation

### Daily morning briefing via cron

```bash
# Open crontab
crontab -e

# Add this line (weekdays at 7 AM):
0 7 * * 1-5 python3 /home/yourname/smfworks-skills/skills/morning-commute/main.py > /home/yourname/commute-today.txt 2>&1
```

Read it when you wake up:
```bash
cat ~/commute-today.txt
```

### Add to terminal startup

Add to `~/.bashrc` or `~/.zshrc` to see your commute briefing every time you open a terminal:

```bash
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

---

## Understanding Google Maps Costs

The Google Maps Directions API costs $0.005 per request. Google provides a $200/month free credit.

Daily usage estimate:
| Usage | Requests/day | Monthly cost | Within free tier? |
|-------|-------------|--------------|-------------------|
| 1 check/day | 2 | ~$0.30 | ✅ Yes |
| 3 checks/day | 6 | ~$0.90 | ✅ Yes |
| 10 checks/day | 20 | ~$3.00 | ✅ Yes |

For normal personal use, you will never exceed the free tier.

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/morning-commute)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
