# Website Checker — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pip | Python package manager | Free |
| requests | Python HTTP library | Free |
| smfworks-skills repository | Cloned via git | Free |
| Internet connection | Required for checking URLs | — |

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.9.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Install the requests Package

```bash
pip install requests
```

Expected output:
```
Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Installing collected packages: requests
Successfully installed requests-2.31.0
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/website-checker
```

---

## Step 5 — Verify the Skill

```bash
python3 main.py
```

Expected:
```
Usage: python main.py <command> [options]

Commands:
  check <url> [--timeout N]            - Check single URL
  ssl <domain> [port]                  - Check SSL certificate
  bulk <url1> <url2> ...               - Check multiple URLs
```

---

## Verify Your Setup

Run a real check on a known-good site:

```bash
python3 main.py check https://google.com
```

Expected:
```
✅ https://google.com
   Status: 200
   Response time: 187.42ms
```

If you see a status code and response time, setup is complete.

---

## Configuration Options

No configuration file or environment variables needed. All options are passed as command arguments.

**Security notes:** The skill blocks requests to localhost, private IP ranges (192.168.x.x, 10.x.x.x), and non-HTTP schemes. This is intentional SSRF protection and cannot be disabled.

---

## Troubleshooting

**`requests not installed`** — Run `pip install requests`.

**`pip: command not found`** — Try `pip3 install requests` or `python3 -m pip install requests`.

**`Connection refused` on first test** — Check your internet connection. The skill requires internet access to check URLs.

---

## Next Steps

Setup complete. See **HOWTO.md** for:
- How to check a single site
- How to verify SSL certificates
- How to monitor a list of sites
- How to schedule automatic checks with cron

```bash
cat HOWTO.md
```
