# System Monitor

> Check disk space, memory, CPU usage, and overall system health — and find the large files eating your storage.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / System Utilities

---

## What It Does

System Monitor is an OpenClaw skill that gives you a quick, clear view of your machine's health from the terminal. Check how full your disk is, see current memory and CPU usage, get a summary of overall system health, and scan directories for large files that may be eating your storage.

Each check shows a status indicator: ✅ healthy, ⚠️ warning (>80% used), or 🔴 critical (>90% used) — so you can tell at a glance if something needs attention.

**What it does NOT do:** It does not monitor continuously in the background, send alerts, track historical usage over time, or terminate runaway processes.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **psutil Python package** — required for memory and CPU checks (installed during setup)
- [ ] **No subscription required** — free tier skill
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/system-monitor
pip install psutil
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]

Commands:
  disk [path]                          - Check disk usage
  memory                               - Check memory usage
  cpu                                  - Check CPU usage
  info                                 - System information
  health                               - Overall system health
  large-files [directory] [n]          - Find large files

Examples:
  python main.py disk
  python main.py memory
  python main.py health
  python main.py large-files ~/Downloads 20
```

---

## Quick Start

Check overall system health in one command:

```bash
python3 main.py health
```

Output:
```
✅ System Health: HEALTHY
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   ✅ Disk: 47.3%
   ✅ Memory: 62.1%
   ✅ Cpu: 18.4%
```

---

## Command Reference

### `disk`

Shows how much space is used and available on a disk. Defaults to the root filesystem (`/`). Pass a path to check the disk containing that path.

**Usage:**
```bash
python3 main.py disk [path]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `path` | ❌ No | Directory to check. Defaults to `/`. | `~/Documents` |

**Example:**
```bash
python3 main.py disk
```

**Output:**
```
✅ Disk Usage (/)
   Total: 499.08 GB
   Used: 234.71 GB (47.0%)
   Free: 264.37 GB
```

**Example — check a specific path:**
```bash
python3 main.py disk ~/Documents
```

**Output (warning threshold):**
```
⚠️ Disk Usage (/home/user/Documents)
   Total: 499.08 GB
   Used: 415.32 GB (83.2%)
   Free: 83.76 GB
```

---

### `memory`

Shows RAM usage: total, used, available, and percentage.

**Usage:**
```bash
python3 main.py memory
```

**Output:**
```
✅ Memory Usage
   Total: 16.0 GB
   Used: 9.82 GB (61.4%)
   Available: 6.18 GB
```

**Critical output:**
```
🔴 Memory Usage
   Total: 8.0 GB
   Used: 7.63 GB (95.4%)
   Available: 0.37 GB
```

---

### `cpu`

Shows current CPU usage percentage, number of cores, and clock frequency.

**Usage:**
```bash
python3 main.py cpu
```

**Output:**
```
✅ CPU Usage
   Usage: 23.7%
   Cores: 8
   Frequency: 2400.0 MHz
```

**Note:** CPU usage is measured over a 1-second interval to get a meaningful reading rather than an instantaneous spike.

---

### `info`

Displays general system information: OS, hostname, architecture, and processor type.

**Usage:**
```bash
python3 main.py info
```

**Output:**
```
📊 System Information
   Platform: Linux-6.2.0-39-generic-x86_64-with-glibc2.35
   Hostname: my-workstation
   Machine: x86_64
   Processor: x86_64
   Boot Time: 2024-03-15 06:12:44
```

---

### `health`

Runs disk, memory, and CPU checks together and reports an overall status. If any check hits warning threshold (>80%), status is `WARNING`. If any hits critical (>90%), status is `CRITICAL`.

**Usage:**
```bash
python3 main.py health
```

**Output (healthy):**
```
✅ System Health: HEALTHY
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   ✅ Disk: 47.3%
   ✅ Memory: 62.1%
   ✅ Cpu: 18.4%
```

**Output (warning):**
```
⚠️ System Health: WARNING
   Timestamp: 2024-03-15T09:42:11.234567

Checks:
   ⚠️ Disk: 84.7%
   ✅ Memory: 58.2%
   ✅ Cpu: 12.1%
```

---

### `large-files`

Scans a directory (and all subdirectories) for files 100 MB or larger. Returns up to N results, sorted by size descending.

**Usage:**
```bash
python3 main.py large-files [directory] [n]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `directory` | ❌ No | Directory to scan. Defaults to `~` (home directory). | `~/Downloads` |
| `n` | ❌ No | Number of files to show. Defaults to 10. | `20` |

**Example:**
```bash
python3 main.py large-files ~/Downloads 5
```

**Output:**
```
📁 Top 5 Large Files in ~/Downloads
   1. ~/Downloads/ubuntu-22.04.3.iso (1024.0 MB)
   2. ~/Downloads/project-backup.zip (847.3 MB)
   3. ~/Downloads/course-videos/lesson-1.mp4 (512.8 MB)
   4. ~/Downloads/old-database-dump.sql (384.2 MB)
   5. ~/Downloads/photos-archive.tar.gz (201.7 MB)
```

**Note:** Only files 100 MB or larger appear in results. Directories outside your home directory are not scanned.

---

## Use Cases

### 1. Quick morning system check

```bash
python3 main.py health
```

One command gives you the full picture in 3 seconds.

---

### 2. Find what's filling your drive

```bash
python3 main.py disk
python3 main.py large-files ~ 20
```

First confirm the drive is getting full, then find which files are the culprits.

---

### 3. Diagnose slow performance

```bash
python3 main.py memory
python3 main.py cpu
```

High memory or CPU usage explains why everything feels slow.

---

### 4. Check a specific drive or mount point

```bash
python3 main.py disk /mnt/backup
```

---

### 5. Get system info for a bug report

```bash
python3 main.py info
```

Quickly get OS and hardware details when filing support tickets.

---

## Configuration

No configuration file or environment variables needed.

**Status thresholds (built-in, not configurable):**

| Status | Threshold |
|--------|-----------|
| ✅ good | < 80% used |
| ⚠️ warning | 80–89% used |
| 🔴 critical | ≥ 90% used |

**Built-in limits:**

| Setting | Value |
|---------|-------|
| Max files to scan (large-files) | 10,000 |
| Max results returned | 100 |
| Rate limit | 30 calls per 60 seconds |
| Search directories | Home, /tmp, /var/tmp, /home only |

---

## Troubleshooting

### `psutil not installed. Run: pip install psutil`
Memory and CPU commands require psutil.  
**Fix:** `pip install psutil`

### `Rate limit exceeded. Max 30 calls per 60 seconds.`
You're calling the skill too rapidly.  
**Fix:** Wait 60 seconds and try again. This limit prevents resource exhaustion from scripts.

### `Path does not exist: /some/path`
The path you passed to `disk` doesn't exist.  
**Fix:** Check the path with `ls /some/path` first.

### `Path traversal detected`
You used `..` in a path.  
**Fix:** Use absolute paths: `/home/yourname/folder` instead of `../../folder`.

### `Directory outside allowed search paths`
You tried to scan a directory outside home, `/tmp`, or `/home`.  
**Fix:** Only paths within your home directory can be scanned by `large-files`.

### `Error: n must be an integer`
You passed a non-numeric value as the count for `large-files`.  
**Fix:** Use an integer: `python3 main.py large-files ~/Downloads 15`

---

## FAQ

**Q: Does this work on macOS?**  
A: Yes. The skill uses Python's standard `platform` and `shutil` modules plus `psutil`, all of which work on macOS.

**Q: Will `large-files` scan network drives?**  
A: Only if the network drive is mounted inside your home directory or `/tmp`. Mounts outside these paths are blocked.

**Q: Does `cpu` show per-core usage?**  
A: No — it shows total CPU usage as a percentage across all cores.

**Q: Why does `large-files` only show files ≥100 MB?**  
A: This is the built-in minimum size threshold. Files smaller than 100 MB are not included in results.

**Q: How does the health command decide overall status?**  
A: If any check is `critical`, the overall status is CRITICAL. If any check is `warning` (and none are critical), the overall status is WARNING. Otherwise it's HEALTHY.

**Q: Can I use this in a cron job to get alerts?**  
A: Yes — see HOWTO.md for examples of scheduling health checks and capturing output to a log file.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| psutil | 5.0 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/system-monitor)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
