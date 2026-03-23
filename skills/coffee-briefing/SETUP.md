# Coffee Briefing — Setup Guide

**Estimated setup time:** 20–30 minutes  
**Difficulty:** Moderate (requires API key and Google OAuth setup)  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| OpenWeatherMap API key | Free tier at openweathermap.org | Free |
| Google Calendar API credentials | OAuth 2.0 setup | Free |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe to SMF Works Pro

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe) and complete the subscription process.

Authenticate OpenClaw:
```bash
openclaw auth status
```

Expected: Your email and `Pro` tier shown.

---

## Step 2 — Get a Free OpenWeatherMap API Key

1. Go to [openweathermap.org/api](https://openweathermap.org/api)
2. Click "Subscribe" under "Current Weather Data" (free tier)
3. Create an account or log in
4. Go to your [API keys page](https://home.openweathermap.org/api_keys)
5. Copy the default API key — it looks like: `a1b2c3d4e5f67890a1b2c3d4e5f67890`

**Note:** New API keys take up to 2 hours to activate. If you get a 401 error after setup, wait and try again.

---

## Step 3 — Set Up Google Calendar Access

Coffee Briefing reads your Google Calendar via the Google Calendar API. This requires a one-time OAuth setup.

**3a — Create a Google Cloud Project:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project (e.g., "Coffee Briefing")
3. Enable the Google Calendar API: search "Calendar API" → Enable

**3b — Create OAuth Credentials:**
1. Go to APIs & Services → Credentials
2. Click "Create Credentials" → "OAuth client ID"
3. Application type: "Desktop app"
4. Name it "Coffee Briefing"
5. Download the JSON file — save it as `~/google-credentials.json`

**3c — Run OAuth authentication:**
The first time Coffee Briefing runs with your credentials, it will open a browser for you to authorize access. Follow the prompts and accept.

---

## Step 4 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 5 — Configure the Skill

```bash
cd ~/smfworks-skills/skills/coffee-briefing
python3 main.py --configure
```

The wizard will prompt for:
- Your OpenWeatherMap API key
- Your city name (e.g., `New York` or `London,GB`)
- Temperature unit (F or C)
- Path to Google credentials JSON file
- News categories

Sample configuration session:
```
OpenWeatherMap API Key: [paste your key]
City: New York
Temperature unit (F/C): F
Google credentials path: /home/user/google-credentials.json
News categories [technology,business]: technology,business

✅ Configuration saved!
```

---

## Step 6 — First Run and Google OAuth

On the first run, a browser window will open for Google Calendar authorization:

```bash
python3 main.py
```

If you're on a headless server, follow the authorization URL instructions shown in the terminal.

After authorization, a token file is saved locally and you won't need to authorize again.

---

## Verify Your Setup

```bash
python3 main.py
```

Expected: A formatted briefing with weather, calendar events, and headlines.

---

## Configuration File

Location: `~/.config/smf/skills/coffee-briefing/config.json`

```json
{
  "openweathermap_api_key": "your-key-here",
  "location": "New York",
  "temperature_unit": "imperial",
  "google_credentials": "/home/user/google-credentials.json",
  "news_categories": ["technology", "business"]
}
```

---

## Troubleshooting Setup Issues

**`Error: OpenWeatherMap API key not configured`** — Run `--configure` again.

**`401 Unauthorized` from weather API** — New OWM keys take up to 2 hours to activate. Wait and retry.

**`City not found`** — Try adding country code: `London,GB` or `Paris,FR`.

**Google Calendar OAuth errors** — Ensure your credentials JSON is valid and the Calendar API is enabled in your Google Cloud project.

**`Error: credentials.json not found`** — The path in config doesn't point to a valid file. Re-run `--configure` with the correct path.

---

## Next Steps

Setup complete. See **HOWTO.md** for daily usage, cron automation, and customization tips.
