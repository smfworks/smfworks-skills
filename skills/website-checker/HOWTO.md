# Website Checker — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). requests installed. Internet connection active.

---

## Table of Contents

1. [How to Check if a Website is Up](#1-how-to-check-if-a-website-is-up)
2. [How to Check an SSL Certificate](#2-how-to-check-an-ssl-certificate)
3. [How to Monitor Multiple Sites at Once](#3-how-to-monitor-multiple-sites-at-once)
4. [How to Check a Slow or Unreliable Site](#4-how-to-check-a-slow-or-unreliable-site)
5. [How to Verify a Redirect is Working](#5-how-to-verify-a-redirect-is-working)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Check if a Website is Up

**What this does:** Makes an HTTP GET request to the URL and reports the response status and time.

**When to use it:** After a deployment, when a user reports your site is down, or as a quick sanity check.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/website-checker
```

**Step 2 — Run the check command.**

```bash
python3 main.py check https://yourwebsite.com
```

**Output (site is up):**
```
✅ https://yourwebsite.com
   Status: 200
   Response time: 243.17ms
```

**Output (site is down):**
```
❌ Failed to check https://yourwebsite.com
   Error: Request failed: ConnectionError: HTTPSConnectionPool(host='yourwebsite.com', port=443): Max retries exceeded
```

**Step 3 — Interpret the status code.**

| Status Code | Meaning |
|-------------|---------|
| 200 | Site is up and working normally |
| 301/302 | Redirect — the skill follows it and shows the final URL |
| 403 | Forbidden — site is up but this URL requires authentication |
| 404 | Page not found — site is up but the URL is wrong |
| 500–503 | Server error — site is up but something is broken on it |

**Result:** You know definitively whether the site is reachable and what it returned.

---

## 2. How to Check an SSL Certificate

**What this does:** Connects to a domain over SSL and reports the certificate's issuer, expiration date, days remaining, and TLS version.

**When to use it:** Before your certificate expires (Let's Encrypt certificates expire every 90 days). Or when users report browser security warnings.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/website-checker
```

**Step 2 — Run the ssl command.**

Important: Pass only the domain name, not the full URL.

```bash
python3 main.py ssl yourwebsite.com
```

**Output (certificate is healthy):**
```
✅ SSL Certificate: yourwebsite.com
   Issuer: ((('organizationName', "Let's Encrypt"),),)
   Expires: Jun 14 12:00:00 2024 GMT
   Days until expiry: 91
   TLS Version: TLSv1.3
```

**Output (expiring in 10 days — warning):**
```
⚠️ SSL Certificate: yourwebsite.com
   Issuer: ((('organizationName', "Let's Encrypt"),),)
   Expires: Mar 25 12:00:00 2024 GMT
   Days until expiry: 10
   TLS Version: TLSv1.3
```

**Step 3 — Act on the result.**

- **91+ days:** No action needed
- **10–29 days:** Schedule renewal this week
- **Under 7 days:** Renew immediately — browsers will show security warnings when it expires

**Step 4 — For non-standard ports (e.g., internal services):**

```bash
python3 main.py ssl internal-service.example.com 8443
```

**Result:** You have the certificate status and exact expiry date — no need to dig through hosting dashboards.

---

## 3. How to Monitor Multiple Sites at Once

**What this does:** Checks a list of URLs in sequence and prints one status line per URL.

**When to use it:** You manage multiple websites for clients or internal services and need a quick overview of all of them.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/website-checker
```

**Step 2 — Run bulk with your sites.**

```bash
python3 main.py bulk https://client1.com https://client2.com https://client3.com https://my-api.example.com
```

**Output:**
```
Checking 4 URLs...

✅ https://client1.com - 200 (143ms)
✅ https://client2.com - 200 (287ms)
⚠️ https://client3.com - 403 (88ms)
❌ https://my-api.example.com - DOWN (Request failed: ConnectionError: ...)
```

**Step 3 — Investigate the ones that aren't 200.**

A 403 may be expected (protected endpoint). A DOWN needs investigation.

**Step 4 — Save your site list for easy reuse.**

Create a shell alias or script:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias check-all-sites='python3 ~/smfworks-skills/skills/website-checker/main.py bulk https://client1.com https://client2.com https://client3.com'
```

**Result:** Full status overview in one command.

---

## 4. How to Check a Slow or Unreliable Site

**What this does:** Uses a longer timeout for sites that normally take more than 10 seconds to respond.

**When to use it:** The default check returns a timeout error for a site you know is sometimes just slow.

### Steps

**Step 1 — Try with default timeout first.**

```bash
python3 main.py check https://slow-api.example.com
```

Output:
```
❌ Failed to check https://slow-api.example.com
   Error: Request failed: ReadTimeout: HTTPSConnectionPool(host='slow-api.example.com', port=443): Read timed out. (read timeout=10)
```

**Step 2 — Retry with a longer timeout.**

```bash
python3 main.py check https://slow-api.example.com --timeout 60
```

Output:
```
✅ https://slow-api.example.com
   Status: 200
   Response time: 34,821.43ms
```

**Step 3 — Interpret the result.**

34 seconds is extremely slow. This is either a performance problem worth investigating or expected for that endpoint.

**Result:** You confirmed the site is up, just slow, and measured exactly how slow.

---

## 5. How to Verify a Redirect is Working

**What this does:** When you redirect `http://` to `https://` or an old domain to a new one, this confirms the redirect is in place.

**When to use it:** After setting up a domain redirect, changing your site URL, or migrating to HTTPS.

### Steps

**Step 1 — Check the old URL.**

```bash
python3 main.py check http://old-domain.com
```

**Output (redirect working):**
```
✅ http://old-domain.com
   Status: 200
   Response time: 312.55ms
   Redirected to: https://www.new-domain.com/
```

**Output (redirect not set up):**
```
✅ http://old-domain.com
   Status: 200
   Response time: 89.12ms
```

(No "Redirected to" line means no redirect happened.)

**Result:** The "Redirected to" line confirms the redirect is working correctly.

---

## 6. Automating with Cron

Schedule regular site checks and log results. Review the log for downtime history.

### Open the cron editor

```bash
crontab -e
```

### Example: Check your main site every 30 minutes

```bash
*/30 * * * * python3 /home/yourname/smfworks-skills/skills/website-checker/main.py check https://yoursite.com >> /home/yourname/logs/site-check.log 2>&1
```

### Example: Check SSL certificate every morning

```bash
0 8 * * * python3 /home/yourname/smfworks-skills/skills/website-checker/main.py ssl yoursite.com >> /home/yourname/logs/ssl-check.log 2>&1
```

### Example: Check all client sites every hour

```bash
0 * * * * python3 /home/yourname/smfworks-skills/skills/website-checker/main.py bulk https://client1.com https://client2.com https://client3.com >> /home/yourname/logs/bulk-check.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `*/30 * * * *` | Every 30 minutes |
| `0 * * * *` | Every hour at :00 |
| `0 8 * * *` | Every day at 8 AM |
| `0 8 * * 1` | Every Monday at 8 AM |

### Create the log directory

```bash
mkdir -p ~/logs
```

### Check for downtime in logs

```bash
grep "❌" ~/logs/site-check.log | tail -20
```

---

## 7. Combining with Other Skills

**Website Checker + Email Campaign:** Check that your landing page is up before sending a campaign:

```bash
python3 ~/smfworks-skills/skills/website-checker/main.py check https://landing-page.com
# If ✅, proceed with campaign
```

**Website Checker + System Monitor:** Morning routine script — check both system health and site status:

```bash
#!/bin/bash
python3 ~/smfworks-skills/skills/system-monitor/main.py health
python3 ~/smfworks-skills/skills/website-checker/main.py bulk https://site1.com https://site2.com
```

---

## 8. Troubleshooting Common Issues

### `requests not installed. Run: pip install requests`

The package is missing.  
**Fix:** `pip install requests`

---

### `Request failed: ConnectionError: Max retries exceeded`

The site is unreachable from your network.  
**Fix:** 1) Confirm you have internet access. 2) Try opening the URL in a browser. 3) Check DNS: `nslookup yourdomain.com`.

---

### `Request failed: ReadTimeout: Read timed out. (read timeout=10)`

The site didn't respond within 10 seconds.  
**Fix:** Try with a longer timeout: `--timeout 30`. If still failing, the site is very slow or overloaded.

---

### `SSL Error: CERTIFICATE_VERIFY_FAILED`

The site's SSL certificate is invalid, expired, or self-signed.  
**Fix:** If it's your site, renew the certificate immediately. If it's someone else's, they have an SSL problem.

---

### `SSRF Protection: Access to localhost is not allowed`

You tried to check `http://localhost` or a private IP address.  
**Fix:** This is intentional security protection. The skill only checks public internet URLs.

---

### `Error: bulk requires at least 2 URLs`

You used `bulk` with only one URL.  
**Fix:** Use `check` for a single URL. Use `bulk` when you have two or more.

---

## 9. Tips & Best Practices

**Check SSL monthly for all production sites.** Let's Encrypt certificates expire every 90 days. A monthly check gives you ample warning. At 30 days or less, renew immediately.

**Use `bulk` for regular monitoring.** Build a list of your critical URLs and run `bulk` daily via cron. Review the log periodically for patterns.

**A 403 doesn't mean the site is down.** HTTP 403 (Forbidden) means the server responded — it's up — but this particular endpoint requires authentication. This is often expected.

**Response times over 2,000ms are worth investigating.** Sub-200ms is great. 200–1000ms is normal. Over 2000ms is slow enough to hurt user experience and bounce rates.

**Use absolute paths in cron.** Cron doesn't expand `~`. Use `/home/yourname/` instead of `~/` in crontab entries.

**Save your bulk URL list as a script.** If you check the same sites repeatedly, create a short shell script instead of retyping the URLs:

```bash
#!/bin/bash
python3 ~/smfworks-skills/skills/website-checker/main.py bulk \
  https://site1.com \
  https://site2.com \
  https://site3.com
```
