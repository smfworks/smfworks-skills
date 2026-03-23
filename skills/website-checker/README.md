# Website Checker

> Check if a website is up, measure its response time, verify its SSL certificate, and monitor multiple sites at once.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Web Utilities

---

## What It Does

Website Checker is an OpenClaw skill that lets you quickly verify whether a website is reachable, how fast it responds, and whether its SSL/TLS certificate is valid and not expiring soon. You can check a single URL, inspect a certificate's expiration date, or run a bulk check on multiple sites at once.

It uses HTTP/HTTPS requests via the `requests` library and native Python SSL socket inspection — no external APIs, no accounts needed.

**What it does NOT do:** It does not monitor sites continuously in real-time, send email/SMS alerts automatically, measure page load time (only time-to-first-byte), check DNS records, or bypass authentication to check protected pages.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **requests Python package** — installed during setup
- [ ] **No subscription required** — free tier skill
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/website-checker
pip install requests
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]

Commands:
  check <url> [--timeout N]            - Check single URL
  ssl <domain> [port]                  - Check SSL certificate
  bulk <url1> <url2> ...               - Check multiple URLs

Examples:
  python main.py check https://google.com
  python main.py check https://google.com --timeout 30
  python main.py ssl smf.works
  python main.py ssl smf.works 8443
  python main.py bulk https://google.com https://github.com
```

---

## Quick Start

Check if a website is up:

```bash
python3 main.py check https://google.com
```

Output:
```
✅ https://google.com
   Status: 200
   Response time: 187.42ms
```

---

## Command Reference

### `check`

Checks whether a URL is reachable via HTTP GET. Reports the HTTP status code, response time, and whether the final URL differs from the input (indicating a redirect).

**Usage:**
```bash
python3 main.py check <url> [--timeout N]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url` | ✅ Yes | URL to check. `https://` is added if scheme is missing. | `https://example.com` |
| `--timeout N` | ❌ No | Seconds to wait before giving up. Default: 10. Min: 1. Max: 300. | `--timeout 30` |

**Example — basic check:**
```bash
python3 main.py check https://smfworks.com
```

**Output:**
```
✅ https://smfworks.com
   Status: 200
   Response time: 243.17ms
```

**Example — site is down:**
```bash
python3 main.py check https://broken-site.example.com
```

**Output:**
```
❌ Failed to check https://broken-site.example.com
   Error: Request failed: ConnectionError: HTTPSConnectionPool(host='broken-site.example.com', port=443): Max retries exceeded
```

**Example — with custom timeout:**
```bash
python3 main.py check https://slow-api.example.com --timeout 30
```

**Example — URL with redirect:**
```bash
python3 main.py check http://google.com
```

**Output:**
```
✅ http://google.com
   Status: 200
   Response time: 312.55ms
   Redirected to: https://www.google.com/
```

---

### `ssl`

Checks the SSL/TLS certificate for a domain — expiration date, days until expiry, issuer, and TLS version.

**Usage:**
```bash
python3 main.py ssl <domain> [port]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `domain` | ✅ Yes | Domain name to check. Do NOT include `https://`. | `smfworks.com` |
| `port` | ❌ No | Port to connect to. Default: 443. | `8443` |

**SSL status indicators:**

| Status | Condition |
|--------|-----------|
| ✅ | Certificate expires in 30+ days |
| ⚠️ | Certificate expires in 7–29 days — renew soon |
| 🔴 | Certificate expires in fewer than 7 days — urgent |

**Example:**
```bash
python3 main.py ssl smfworks.com
```

**Output (healthy):**
```
✅ SSL Certificate: smfworks.com
   Issuer: ((('organizationName', "Let's Encrypt"),),)
   Expires: Jun 14 12:00:00 2024 GMT
   Days until expiry: 91
   TLS Version: TLSv1.3
```

**Output (expiring soon):**
```
⚠️ SSL Certificate: mysite.example.com
   Issuer: ((('organizationName', 'ZeroSSL'),),)
   Expires: Mar 25 12:00:00 2024 GMT
   Days until expiry: 10
   TLS Version: TLSv1.3
```

**Example — non-standard port:**
```bash
python3 main.py ssl myserver.example.com 8443
```

---

### `bulk`

Checks two or more URLs in sequence and prints a status summary line for each.

**Usage:**
```bash
python3 main.py bulk <url1> <url2> [more urls...]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url1` | ✅ Yes | First URL to check | `https://google.com` |
| `url2` | ✅ Yes | Second URL to check | `https://github.com` |
| additional URLs | ❌ No | More URLs to check | `https://smfworks.com` |

**Example:**
```bash
python3 main.py bulk https://google.com https://github.com https://mysite.com https://broken.example.com
```

**Output:**
```
Checking 4 URLs...

✅ https://google.com - 200 (187ms)
✅ https://github.com - 200 (312ms)
✅ https://mysite.com - 200 (94ms)
❌ https://broken.example.com - DOWN (Request failed: ConnectionError: ...)
```

---

## Use Cases

### 1. Verify your website is up after a deployment

```bash
python3 main.py check https://yoursite.com
```

A 200 status and sub-500ms response confirms the deployment worked.

---

### 2. Check SSL before it expires

```bash
python3 main.py ssl yoursite.com
```

Run this monthly. If expiry is under 30 days, renew your certificate immediately.

---

### 3. Monitor a list of client sites

```bash
python3 main.py bulk https://client1.com https://client2.com https://client3.com https://client4.com
```

One command, status for every site.

---

### 4. Debug a slow website

```bash
python3 main.py check https://slow-site.com --timeout 60
```

A response time over 2,000ms indicates a slow server or heavy page.

---

### 5. Confirm a redirect is working

```bash
python3 main.py check http://old-domain.com
```

The "Redirected to" line confirms your redirect is configured correctly.

---

## Configuration

No configuration file or environment variables needed.

**Built-in constants:**

| Setting | Value |
|---------|-------|
| Default timeout | 10 seconds |
| SSL warning threshold | 30 days to expiry |
| SSL critical threshold | 7 days to expiry |
| Max timeout | 300 seconds |

**Security limits:**
- Localhost and `127.x.x.x` are blocked (SSRF protection)
- Private IP ranges (192.168.x.x, 10.x.x.x) are blocked
- Only `http://` and `https://` schemes are allowed

---

## Troubleshooting

### `requests not installed. Run: pip install requests`
**Fix:** `pip install requests`

### `❌ Failed to check ... ConnectionError: Max retries exceeded`
The site is unreachable — it may be down, or DNS is failing.  
**Fix:** Try opening the URL in a browser. Check DNS with `nslookup yourdomain.com`.

### `SSL Error: CERTIFICATE_VERIFY_FAILED`
The site's SSL certificate is invalid, expired, or self-signed.  
**Fix:** This is a real SSL problem with the site. If it's your site, renew or fix the certificate.

### `Connection timeout`
The site didn't respond within the timeout period.  
**Fix:** Try again with a longer timeout: `--timeout 30`. If it still fails, the site is very slow or down.

### `SSRF Protection: Access to localhost is not allowed`
You tried to check a localhost or internal IP URL.  
**Fix:** This is a security restriction. The skill only checks public internet URLs.

### `❌ port must be at most 65535, got: 99999`
Invalid port number.  
**Fix:** Use a valid port between 1 and 65535.

### `Error: bulk requires at least 2 URLs`
You provided only one URL to the bulk command.  
**Fix:** Use `check` for a single URL, or provide at least two URLs for `bulk`.

---

## FAQ

**Q: Does this check if my site is accessible globally?**  
A: It checks from your machine's network. For global availability checks, consider services like UptimeRobot or Pingdom.

**Q: What does response time measure?**  
A: Time from sending the HTTP GET request to receiving the complete response headers. It does not include JavaScript execution or page rendering.

**Q: What's the difference between status 200 and 301/302?**  
A: 200 = OK. 301/302 = redirected (the skill follows redirects and reports the final URL and final status code).

**Q: Can I check HTTPS sites with self-signed certificates?**  
A: The SSL check will fail on self-signed certificates. The URL check (`check` command) uses the `requests` library which also validates certificates by default.

**Q: Does the SSL check work on non-standard ports?**  
A: Yes — pass the port as a second argument: `python3 main.py ssl myserver.example.com 8443`

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| requests | 2.25 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/website-checker)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
