# Morning Commute — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Google Maps API key configured. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Check Your Morning Commute](#1-how-to-check-your-morning-commute)
2. [How to Change Your Route or Departure Time](#2-how-to-change-your-route-or-departure-time)
3. [How to Compare Driving vs Transit](#3-how-to-compare-driving-vs-transit)
4. [Automating with Cron](#4-automating-with-cron)
5. [Combining with Other Skills](#5-combining-with-other-skills)
6. [Troubleshooting Common Issues](#6-troubleshooting-common-issues)
7. [Tips & Best Practices](#7-tips--best-practices)

---

## 1. How to Check Your Morning Commute

**What this does:** Queries Google Maps for current traffic on your configured route and presents a commute briefing.

**When to use it:** Every morning 15–30 minutes before you plan to leave.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/morning-commute
```

**Step 2 — Run the briefing.**

```bash
python3 main.py
```

Output:
```
🚗 Morning Commute Briefing — Wednesday, March 15, 2024
Departure: 8:00 AM
═══════════════════════════════════════════════════════

📍 Route: 123 Main St → 456 Business Ave
   Distance: 12.3 miles

🚗 Driving
   Typical time: 28 min
   Current time: 42 min ⚠️ (heavy traffic)
   Estimated arrival: 8:42 AM

🚇 Transit
   Next departure: 8:07 AM
   Estimated arrival: 8:51 AM

Configure: smf run morning-commute --configure
```

**Step 3 — Decide your commute strategy.**

- If current time is close to typical, traffic is normal — leave as planned
- If current time is significantly longer (as above), consider:
  - Leaving earlier
  - Taking transit if faster
  - Waiting for traffic to clear

**Result:** You leave at the right time with confidence.

---

## 2. How to Change Your Route or Departure Time

**When to use it:** You're working at a different location today, or have an earlier/later meeting.

### Steps

**Step 1 — Re-run configure.**

```bash
python3 main.py --configure
```

**Step 2 — Update the relevant settings.**

Press Enter to keep any setting unchanged, or type a new value.

**Step 3 — Run to verify the new route.**

```bash
python3 main.py
```

**Result:** Your briefing now shows the updated route.

---

## 3. How to Compare Driving vs Transit

**When to use it:** You're deciding whether to drive or take public transit.

### Steps

**Step 1 — Check driving (if that's your current mode).**

```bash
python3 main.py
```

Note the estimated travel time.

**Step 2 — Switch mode to transit.**

Edit `~/.config/smf/skills/morning-commute/config.json` and change `travel_mode` to `transit`, or re-run `--configure`.

**Step 3 — Run again for transit comparison.**

```bash
python3 main.py
```

**Step 4 — Decide which is faster today.**

**Result:** Data-driven commute decision every morning.

---

## 4. Automating with Cron

### Open crontab

```bash
crontab -e
```

### Example: Generate commute briefing weekdays at 7 AM

```bash
0 7 * * 1-5 python3 /home/yourname/smfworks-skills/skills/morning-commute/main.py > /home/yourname/commute-brief.txt 2>&1
```

Then read it when you wake up:
```bash
cat ~/commute-brief.txt
```

### Example: Print commute in terminal at login (add to ~/.bashrc)

```bash
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

---

## 5. Combining with Other Skills

**Morning Commute + Coffee Briefing:** Complete morning overview — weather, calendar, commute:

```bash
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

Create a `morning.sh` script:
```bash
#!/bin/bash
echo "=== MORNING BRIEFING ==="
python3 ~/smfworks-skills/skills/coffee-briefing/main.py
echo ""
echo "=== COMMUTE ==="
python3 ~/smfworks-skills/skills/morning-commute/main.py
```

---

## 6. Troubleshooting Common Issues

### `Error: SMF Works Pro subscription required`

**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe) and re-authenticate.

### `REQUEST_DENIED` from Google Maps

Google Maps API isn't configured correctly.  
**Fix:** Go to Google Cloud Console → APIs & Services → Library → Ensure "Directions API" is enabled for your project. Check your API key restrictions.

### `ZERO_RESULTS`

No route was found between your addresses.  
**Fix:** Use complete street addresses with city, state, and ZIP code. Avoid abbreviations.

### Traffic data not shown

Traffic data requires the "Directions API" specifically with traffic model support.  
**Fix:** Ensure `driving` mode is set (transit/walking don't show traffic). Verify API key has correct permissions.

---

## 7. Tips & Best Practices

**Run 15–20 minutes before departure.** Too early and traffic conditions may change; too late and you're already rushing. The 15–20 minute window is the sweet spot.

**Save driving vs transit comparison data.** If you regularly commute, note which days driving is faster vs transit. Patterns emerge (e.g., Thursdays are always congested).

**Use cron for passive awareness.** Schedule the briefing to run at 7 AM so you can glance at the output while having breakfast — no need to remember to run it manually.

**Restrict your Google Maps API key.** In Google Cloud Console, add an IP restriction to your API key so only your machine can use it. This prevents abuse if the key is accidentally exposed.

**Check the Google API dashboard monthly.** Even on the free tier, verify your usage in Google Cloud Console under APIs & Services → Dashboard. One daily check is ~$0.30/month — easily within the $200 free credit.
