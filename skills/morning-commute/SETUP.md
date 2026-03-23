# Morning Commute — Setup Guide

**Estimated setup time:** 15–20 minutes  
**Difficulty:** Moderate (requires Google Maps API key)  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| Google Maps API key | Free $200/mo credit from Google | Free for personal use |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe to SMF Works Pro

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe).

Verify authentication:
```bash
openclaw auth status
```

---

## Step 2 — Get a Google Maps API Key

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (e.g., "Morning Commute")
3. Go to APIs & Services → Library
4. Search "Directions API" → Enable it
5. Go to APIs & Services → Credentials
6. Click "Create Credentials" → "API Key"
7. Copy the key — it looks like: `AIzaSyD1a2b3c4d5e6f7g8h9i0j`
8. (Recommended) Restrict the key to the Directions API only

**Cost:** Google gives $200/month free credit. A daily commute check costs ~$0.005 — well within free tier.

---

## Step 3 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 4 — Configure the Skill

```bash
cd ~/smfworks-skills/skills/morning-commute
python3 main.py --configure
```

Prompts:
```
Google Maps API Key: [paste key]
Home address: 123 Main St, New York, NY 10001
Work address: 456 Business Ave, New York, NY 10002
Departure time [08:00]: 08:00
Travel mode (driving/transit/walking/bicycling) [driving]: driving

✅ Configuration saved!
```

---

## Step 5 — Verify

```bash
python3 main.py
```

Expected: A formatted commute briefing with travel time and traffic conditions.

---

## Configuration File

Location: `~/.config/smf/skills/morning-commute/config.json`

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`REQUEST_DENIED`** — Enable the Directions API in Google Cloud Console for your project.

**`ZERO_RESULTS`** — Use full street addresses with city and ZIP code.

**`API key not valid`** — Check the key is correctly copied with no extra spaces.

---

## Configuration File Details

Your configuration is saved at:
```
~/.config/smf/skills/morning-commute/config.json
```

Sample configuration:
```json
{
  "google_maps_api_key": "AIzaSyD1a2b3c4d5e6f7g8h9i0j",
  "home_address": "123 Main St, New York, NY 10001",
  "work_address": "456 Business Ave, New York, NY 10002",
  "departure_time": "08:00",
  "travel_mode": "driving"
}
```

Edit directly or re-run `--configure` to update.

---

## Google Maps API Setup in Detail

**Step 1 — Create a Google Cloud Project:**

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click the project selector at the top → "New Project"
3. Name: `Morning Commute` → Click "Create"
4. Wait for project creation (30 seconds)

**Step 2 — Enable the Directions API:**

1. In the left sidebar: APIs & Services → Library
2. Search: `Directions API`
3. Click the result → Click "Enable"
4. Wait for the API to enable

**Step 3 — Create an API Key:**

1. APIs & Services → Credentials
2. Click "+ Create Credentials" → "API Key"
3. Your new key is displayed — copy it
4. Click "Edit API key" to add restrictions (recommended)

**Step 4 — Restrict Your API Key (Recommended):**

Restricting your key prevents unauthorized use if it's ever exposed:

1. In the API key settings page:
2. Under "Application restrictions" → Select "IP addresses"
3. Add your machine's public IP (find it at whatismyip.com)
4. Under "API restrictions" → "Restrict key" → Select "Directions API"
5. Save

**Step 5 — Verify the API Key Works:**

Test directly:
```bash
curl "https://maps.googleapis.com/maps/api/directions/json?origin=New+York&destination=Brooklyn&key=YOUR_KEY_HERE" | python3 -m json.tool | head -5
```

Expected: A JSON response with route data (not an error).

---

## Understanding Google Maps Costs

The Directions API costs $0.005 per request (as of 2024). Google provides $200 free credit per month.

**Your estimated monthly cost:**
```
1 check/day × 30 days × $0.005 = $0.15/month
2 checks/day × 30 days × $0.005 = $0.30/month
```

Both are well within the $200 free tier. You won't be charged unless you significantly exceed this.

**Monitor your usage:**
- Go to Google Cloud Console → Billing → Overview
- Verify charges remain at $0 (within free credit)

**Set up billing alerts:**
- Billing → Budgets & alerts → Create Budget
- Set alert threshold at $5 to catch any unexpected usage

---

## Travel Mode Options

Configure via `--configure` or edit the config file:

| Mode | When to use | What it shows |
|------|-------------|---------------|
| `driving` | You commute by car | Traffic-aware route, current conditions |
| `transit` | You use public transit | Bus/train schedules, walking segments |
| `walking` | Short commute on foot | Walking route, estimated time |
| `bicycling` | You bike | Bike-friendly routes |

**Tip:** Set to `driving` even if you sometimes take transit — driving mode shows the best traffic picture. Transit mode requires transit data to be available for your area.

---

## Address Format Tips

For best results, use complete addresses:

**Good:**
```
123 Main Street, New York, NY 10001, USA
456 Business Ave Suite 200, Chicago, IL 60601
```

**Less reliable:**
```
123 Main St
My Office
Work
```

Google Maps is flexible, but complete addresses with ZIP codes are most reliable. Test your addresses at maps.google.com first to confirm they resolve correctly.

---

## Departure Time Format

Set as 24-hour format: `HH:MM`

| Time | Format |
|------|--------|
| 7:00 AM | `07:00` |
| 8:30 AM | `08:30` |
| 9:00 AM | `09:00` |
| 5:30 PM | `17:30` |

The skill queries Google Maps for traffic conditions at your configured departure time.

---

## Verifying Your Setup Works Correctly

After running `--configure`, test that everything is working:

**Step 1 — Run the skill:**
```bash
python3 main.py
```

**Step 2 — Check the output includes traffic data:**

A working output looks like:
```
🚗 Morning Commute Briefing — Wednesday, March 15, 2024
Departure: 8:00 AM

📍 Route: 123 Main St → 456 Business Ave
   Distance: 12.3 miles

🚗 Driving
   Typical time: 28 min
   Current time: 32 min
   Estimated arrival: 8:32 AM
```

**Step 3 — Verify traffic data is live:**

If "Typical time" and "Current time" are the same, traffic data may not be working. This can happen if:
- You're running it outside business hours (less traffic data available)
- The Directions API isn't fully enabled yet (wait 5 minutes after enabling)

**Step 4 — Test edge cases:**

Run during different times to see how traffic varies:
```bash
# Normal time
python3 main.py

# Verify it shows reasonable numbers for your route
```

---

## Common Setup Mistakes

**Wrong API key (has extra spaces or missing characters):**
API keys from Google Cloud Console are exactly 39 characters. If yours is shorter or longer, re-copy it carefully.

**Directions API enabled but key not working:**
There can be a 5-minute delay after enabling a new API before the key starts working. Wait and retry.

**Home or work address resolves to wrong location:**
Test your addresses at maps.google.com before configuring. If Google Maps shows the right place, the skill will too.

**Configured for `transit` mode but no transit data appears:**
Not all areas have detailed transit data in Google Maps. Switch to `driving` for the best results.

---

## Uninstalling / Resetting

To reset the configuration and start fresh:

```bash
rm ~/.config/smf/skills/morning-commute/config.json
python3 main.py --configure
```

This wipes the saved config without deleting the skill files.

---

## Next Steps

Setup complete. See **HOWTO.md** for daily usage and cron automation.
