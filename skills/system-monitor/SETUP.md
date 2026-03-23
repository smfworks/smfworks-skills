# System Monitor — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pip | Python package manager | Free |
| psutil | Python system stats library | Free |
| smfworks-skills repository | Cloned via git | Free |

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.10.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Install psutil

```bash
pip install psutil
```

Expected output:
```
Collecting psutil
  Downloading psutil-5.9.6-cp311-cp311-linux_x86_64.whl (404 kB)
Installing collected packages: psutil
Successfully installed psutil-5.9.6
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/system-monitor
```

---

## Step 5 — Verify

```bash
python3 main.py health
```

Expected output:
```
✅ System Health: HEALTHY
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   ✅ Disk: 47.3%
   ✅ Memory: 62.1%
   ✅ Cpu: 18.4%
```

If you see status indicators and percentages, setup is complete.

---

## Configuration Options

No configuration needed. All options are passed as command arguments.

---

## Troubleshooting

**`psutil not installed`** — Run `pip install psutil`.

**`pip: command not found`** — Try `pip3 install psutil` or `python3 -m pip install psutil`.

---

## Next Steps

See **HOWTO.md** for walkthroughs on disk checks, large-file scanning, health monitoring, and cron automation.

---

## Quick Reference

Once setup is complete, the most useful commands are:

```bash
# Daily health check
python3 main.py health

# Check disk space
python3 main.py disk

# Check memory
python3 main.py memory

# Find large files in your home directory
python3 main.py large-files ~ 10
```

These four commands cover 90% of everyday use cases.
