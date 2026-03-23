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

## Next Steps

Setup complete. See **HOWTO.md** for daily usage and cron automation.
