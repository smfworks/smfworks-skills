# Website Checker

> Check if websites are up, measure response times, and verify SSL certificates

---

## What It Does

Website Checker monitors your websites and APIs. Test if URLs are accessible, measure response times, check SSL certificate expiration, and verify multiple sites at once. Essential for monitoring production services.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install website-checker
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Check if a website is up:

```bash
python main.py check https://example.com
```

---

## Commands

### `check`

**What it does:** Check if a URL is accessible and measure response time.

**Usage:**
```bash
python main.py check [url] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url` | ✅ Yes | Website URL to check | `https://example.com` |

**Options:**

| Option | Required | Description | Default |
|--------|----------|-------------|---------|
| `--timeout` | ❌ No | Request timeout in seconds (1-300) | `10` |

**Example:**
```bash
python main.py check https://google.com
python main.py check https://example.com --timeout 30
```

**Output:**
```
✅ https://google.com
   Status: 200
   Response time: 45.23ms
```

---

### `ssl`

**What it does:** Check SSL certificate information and expiration.

**Usage:**
```bash
python main.py ssl [domain] [port]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `domain` | ✅ Yes | Domain to check | `example.com` |
| `port` | ❌ No | SSL port number | `443` |

**Example:**
```bash
python main.py ssl example.com
python main.py ssl smf.works
python main.py ssl example.com 8443
```

**Output:**
```
✅ SSL Certificate: smf.works
   Issuer: Let's Encrypt
   Expires: Mar 20 12:00:00 2026 GMT
   Days until expiry: 365
   TLS Version: TLSv1.3
```

---

### `bulk`

**What it does:** Check multiple URLs at once.

**Usage:**
```bash
python main.py bulk [url1] [url2] [url3] ...
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url1` | ✅ Yes | First URL to check | `https://google.com` |
| `url2...` | ✅ Yes | Additional URLs | `https://github.com` |

**Example:**
```bash
python main.py bulk https://google.com https://github.com https://twitter.com
```

**Output:**
```
✅ https://google.com - 200 (45.23ms)
✅ https://github.com - 200 (123.45ms)
❌ https://broken-site.com - DOWN (Connection timeout)
```

---

## Use Cases

- **Uptime monitoring:** Verify your website is responding
- **SSL monitoring:** Check certificate expiration dates
- **API health checks:** Test if APIs are responding
- **Performance monitoring:** Track response times over time
- **Incident response:** Quick checks during outages

---

## Tips & Tricks

- Set up cron to run checks daily and alert on failures
- Use `--timeout` for slow sites (up to 300 seconds)
- SSL checks show 🔴 when expiring in <7 days
- Bulk checks are great for monitoring multiple services

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "requests not installed" | Run `pip install requests` |
| "Connection timeout" | Site may be down; try with `--timeout 30` |
| "SSL Error" | Certificate may be invalid or self-signed |
| "Access denied" | Site may block automated requests |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- `requests` library (`pip install requests`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/website-checker)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
