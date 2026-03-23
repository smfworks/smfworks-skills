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
5. Copy the default API key — it looks like: `YOUR_OWM_API_KEY_HERE`

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

---

## Configuration File Details

Your configuration is saved at:
```
~/.config/smf/skills/coffee-briefing/config.json
```

Sample configuration:
```json
{
  "openweathermap_api_key": "YOUR_OWM_API_KEY_HERE",
  "location": "New York",
  "temperature_unit": "imperial",
  "google_credentials": "/home/user/google-credentials.json",
  "news_categories": ["technology", "business"],
  "google_calendar_token": "/home/user/.config/smf/skills/coffee-briefing/token.json"
}
```

You can edit this file directly to update settings:
```bash
nano ~/.config/smf/skills/coffee-briefing/config.json
```

Or re-run `--configure` to update via the wizard.

---

## OpenWeatherMap API Details

The free OpenWeatherMap API provides:

| Feature | Free Tier |
|---------|-----------|
| Current weather | ✅ Yes |
| 5-day forecast | ✅ Yes |
| Hourly forecast | ✅ Yes |
| Calls/minute | 60 |
| Calls/month | 1,000,000 |

One daily briefing = 1–2 API calls. You'll never approach the free tier limit.

**Available temperature units:**
- `imperial` — Fahrenheit (°F) — for US users
- `metric` — Celsius (°C) — for international users
- `standard` — Kelvin (K) — not recommended for daily use

**Location formats:**
- City name: `New York` or `London` or `Paris`
- With country: `London,GB` or `Paris,FR` (more precise, avoids ambiguity)
- ZIP code (US): `10001`
- Coordinates: `40.7128,-74.0060`

---

## Google Calendar API Details

The Google Calendar API is free for personal use:

| Feature | Free |
|---------|------|
| Read calendar events | ✅ Free |
| API calls/day | 1,000,000 |
| OAuth setup required | ✅ Yes (one-time) |

**Which calendars are included?**  
By default, all calendars associated with the Google account you authenticated with. Primary, secondary, shared, and subscribed calendars all appear.

**Google Cloud Console Steps in Detail:**

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click "Select a project" → "New Project"
3. Name it "Coffee Briefing" → Create
4. In the left menu: APIs & Services → Library
5. Search "Google Calendar API" → Click result → "Enable"
6. APIs & Services → Credentials → "Create Credentials" → "OAuth client ID"
7. Configure the OAuth consent screen first if prompted:
   - User type: External
   - App name: Coffee Briefing
   - User support email: your email
   - Save and continue through all steps
8. Back to credentials: "Create Credentials" → "OAuth client ID"
9. Application type: **Desktop app**
10. Name: Coffee Briefing Desktop
11. Create → Download JSON
12. Save as `~/google-credentials.json`

**First-run authorization:**

The first time you run `python3 main.py`, a browser window opens (or a URL is printed for headless servers). Follow the Google OAuth flow to grant read access to your calendar. A `token.json` is saved for future runs.

---

## Troubleshooting Google Calendar Setup

**"This app isn't verified" warning:**
This appears because your OAuth app is not verified by Google. Click "Advanced" → "Go to Coffee Briefing (unsafe)" → Continue. This is safe for personal apps you created yourself.

**`invalid_client` error:**
Your credentials JSON is malformed. Re-download it from Google Cloud Console.

**Calendar is empty despite having events:**
Check that the authenticated Google account has events. If you have multiple Google accounts, ensure you authorized the right one.

**`Token has been expired or revoked`:**
Delete the token file and re-authenticate:
```bash
rm ~/.config/smf/skills/coffee-briefing/token.json
python3 main.py
```

---

## Next Steps

Setup complete. See **HOWTO.md** for daily usage, cron automation, and customization tips.
