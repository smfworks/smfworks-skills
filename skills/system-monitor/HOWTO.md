# System Monitor — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). psutil installed.

---

## Table of Contents

1. [How to Check Disk Space](#1-how-to-check-disk-space)
2. [How to Check Memory and CPU](#2-how-to-check-memory-and-cpu)
3. [How to Run a Full Health Check](#3-how-to-run-a-full-health-check)
4. [How to Find Large Files Eating Your Storage](#4-how-to-find-large-files-eating-your-storage)
5. [How to Get System Info for a Support Ticket](#5-how-to-get-system-info-for-a-support-ticket)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Check Disk Space

**What this does:** Shows how full a disk is, with a status indicator so you know immediately whether to be concerned.

**When to use it:** When downloads are failing, when your machine feels slow, or just to confirm you have room for something large.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/system-monitor
```

**Step 2 — Run the disk command.**

```bash
python3 main.py disk
```

Output:
```
✅ Disk Usage (/)
   Total: 499.08 GB
   Used: 234.71 GB (47.0%)
   Free: 264.37 GB
```

**Step 3 — Interpret the status.**

- ✅ = below 80% used — plenty of space
- ⚠️ = 80–89% used — consider cleaning up
- 🔴 = 90%+ used — action needed soon

**Step 4 — Check a specific path if needed.**

If you have a separate data drive or partition mounted at `/data`:

```bash
python3 main.py disk /data
```

**Result:** You know exactly how much space you have and whether you need to take action.

---

## 2. How to Check Memory and CPU

**What this does:** Shows current RAM and CPU usage with status indicators.

**When to use it:** When your computer feels sluggish and you want to know if it's memory pressure, a runaway process eating CPU, or something else.

### Steps

**Step 1 — Check memory.**

```bash
python3 main.py memory
```

Output:
```
✅ Memory Usage
   Total: 16.0 GB
   Used: 9.82 GB (61.4%)
   Available: 6.18 GB
```

**Step 2 — Check CPU.**

```bash
python3 main.py cpu
```

Output:
```
⚠️ CPU Usage
   Usage: 83.2%
   Cores: 8
   Frequency: 2400.0 MHz
```

**Step 3 — Interpret.**

If CPU is above 70% and you're not doing anything heavy, a background process is likely responsible. Use `top` or `htop` to find it.

If memory is above 80%, close unused applications or consider adding RAM.

**Result:** You've identified whether performance issues are memory-related or CPU-related.

---

## 3. How to Run a Full Health Check

**What this does:** Checks disk, memory, and CPU together and reports a single overall status.

**When to use it:** Daily routine checks, or before starting a resource-intensive task.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/system-monitor
```

**Step 2 — Run health.**

```bash
python3 main.py health
```

**Healthy output:**
```
✅ System Health: HEALTHY
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   ✅ Disk: 47.3%
   ✅ Memory: 62.1%
   ✅ Cpu: 18.4%
```

**Warning output:**
```
⚠️ System Health: WARNING
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   ⚠️ Disk: 84.7%
   ✅ Memory: 58.2%
   ✅ Cpu: 12.1%
```

**Critical output:**
```
🔴 System Health: CRITICAL
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   🔴 Disk: 93.1%
   ✅ Memory: 55.8%
   ✅ Cpu: 22.3%
```

**Step 3 — Take action if needed.**

If disk is critical, run `large-files` to find what to delete. If memory is critical, close applications. If CPU is critical, check `top` for runaway processes.

**Result:** One command, full picture, clear status.

---

## 4. How to Find Large Files Eating Your Storage

**What this does:** Scans a directory and all its subdirectories for files 100 MB or larger, sorted by size.

**When to use it:** Your disk is showing 80%+ used and you want to know what to delete.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/system-monitor
```

**Step 2 — First confirm the disk is filling up.**

```bash
python3 main.py disk
```

Output:
```
⚠️ Disk Usage (/)
   Total: 499.08 GB
   Used: 415.32 GB (83.2%)
   Free: 83.76 GB
```

**Step 3 — Scan your home directory for large files.**

```bash
python3 main.py large-files ~ 15
```

Output:
```
📁 Top 15 Large Files in ~
   1. ~/Downloads/ubuntu-22.04.3.iso (1024.0 MB)
   2. ~/Videos/screen-recording-2024-01.mp4 (892.3 MB)
   3. ~/Downloads/project-backup.zip (847.3 MB)
   4. ~/Documents/client-db-dump.sql (512.1 MB)
   5. ~/Downloads/course-videos/lesson-1.mp4 (488.7 MB)
   6. ~/Downloads/old-backup.tar.gz (347.2 MB)
   7. ~/VMs/ubuntu.vmdk (287.4 MB)
   8. ~/Downloads/photoshop-installer.dmg (241.1 MB)
   9. ~/Pictures/archive-2022.zip (198.3 MB)
   10. ~/node_modules/.cache/webpack/bundle.js.cache (187.4 MB)
```

**Step 4 — Delete or move what you don't need.**

```bash
# Delete a file you no longer need
rm ~/Downloads/ubuntu-22.04.3.iso

# Or move to external drive
mv ~/Downloads/old-backup.tar.gz /Volumes/External/backups/
```

**Step 5 — Re-run to verify improvement.**

```bash
python3 main.py disk
```

**Result:** You found the specific files using your disk space and freed it up.

---

## 5. How to Get System Info for a Support Ticket

**What this does:** Displays your OS version, hostname, architecture, and processor type.

**When to use it:** When filing a bug report or support ticket that asks for system information.

### Steps

**Step 1 — Run the info command.**

```bash
python3 main.py info
```

Output:
```
📊 System Information
   Platform: Linux-6.2.0-39-generic-x86_64-with-glibc2.35
   Hostname: my-laptop
   Machine: x86_64
   Processor: x86_64
   Boot Time: 2024-03-15 06:12:44
```

**Step 2 — Copy the output into your support ticket or bug report.**

**Result:** Complete system information ready in one command.

---

## 6. Automating with Cron

Schedule health checks to run automatically and log results. Review logs to spot trends before they become problems.

### Open the cron editor

```bash
crontab -e
```

### Example: Run health check every morning at 8 AM

```bash
0 8 * * * cd /home/yourname/smfworks-skills/skills/system-monitor && python3 main.py health >> /home/yourname/logs/system-health.log 2>&1
```

### Example: Check disk usage every hour

```bash
0 * * * * python3 /home/yourname/smfworks-skills/skills/system-monitor/main.py disk >> /home/yourname/logs/disk-usage.log 2>&1
```

### Example: Run large-files scan every Sunday

```bash
0 9 * * 0 python3 /home/yourname/smfworks-skills/skills/system-monitor/main.py large-files /home/yourname 20 >> /home/yourname/logs/large-files.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 8 * * *` | Every day at 8 AM |
| `0 * * * *` | Every hour at :00 |
| `0 9 * * 0` | Every Sunday at 9 AM |
| `*/15 * * * *` | Every 15 minutes |

### Create the log directory first

```bash
mkdir -p ~/logs
```

### Review logs

```bash
# See the last 20 health checks
tail -40 ~/logs/system-health.log

# Check for any warnings or criticals
grep -E "WARNING|CRITICAL" ~/logs/system-health.log
```

---

## 7. Combining with Other Skills

**System Monitor + File Organizer:** Find large files, then organize them:

```bash
python3 ~/smfworks-skills/skills/system-monitor/main.py large-files ~/Downloads 20
# Then organize what remains:
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-type ~/Downloads
```

**System Monitor + OpenClaw Backup:** Check disk space before running a backup:

```bash
python3 ~/smfworks-skills/skills/system-monitor/main.py disk
# If plenty of space, run backup:
python3 ~/smfworks-skills/skills/openclaw-backup/main.py backup
```

---

## 8. Troubleshooting Common Issues

### `psutil not installed. Run: pip install psutil`

psutil is missing from your Python environment.  
**Fix:** `pip install psutil`

---

### `Rate limit exceeded. Max 30 calls per 60 seconds.`

You're running the skill too rapidly (more than 30 calls per minute).  
**Fix:** Wait 60 seconds. This is a safety limit to prevent resource exhaustion from scripts.

---

### `Directory outside allowed search paths`

You tried to scan a path outside your home directory with `large-files`.  
**Fix:** Only `~` (home), `/tmp`, and `/home` can be scanned. Use a path inside your home directory.

---

### `Path does not exist`

The path you passed to `disk` doesn't exist on your system.  
**Fix:** Verify the path with `ls /your/path` first.

---

### CPU usage seems unrealistically high

The `cpu` command measures over a 1-second interval. If something else is running during that second, the reading will be high.  
**Fix:** Run it again — a second sample gives a better average picture.

---

## 9. Tips & Best Practices

**Run `health` first, then drill down.** Start with `python3 main.py health` to see which resource (disk/memory/CPU) is the problem, then run the specific check for details.

**Schedule daily health logs.** A daily cron job creating a log file lets you spot trends — like disk usage creeping up 2% per week — before it becomes a crisis.

**Use `large-files` before any major project.** Before starting a large download, video export, or virtual machine creation, confirm you have enough free space.

**Don't ignore 80% disk warnings.** At 80%, you still have time to clean up calmly. At 95%, you'll start seeing errors in applications.

**The `large-files` command shows files ≥100 MB only.** If you have thousands of small files filling your disk, this command won't help. Use `du -sh ~/*/` to find which subdirectories are large, then investigate inside them.

**Check before cron jobs that write large outputs.** If your cron jobs write logs or exports, confirm disk space beforehand with a `disk` check in the same script.
