# System Monitor

> Monitor disk space, memory, CPU, and system health — find large files consuming space

---

## What It Does

System Monitor checks your computer's health — disk usage, RAM utilization, CPU load, and identifies large files that are eating up storage. Essential for keeping your system running smoothly and knowing when it's time to clean up.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install system-monitor
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Check your system health:

```bash
python main.py health
```

---

## Commands

### `disk`

**What it does:** Check disk space usage for a path.

**Usage:**
```bash
python main.py disk [path]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `path` | ❌ No | Path to check (default: /) | `/home` |

**Example:**
```bash
python main.py disk
python main.py disk /home
```

**Output:**
```
✅ Disk Usage (/)
   Total: 500.0 GB
   Used: 250.0 GB (50.0%)
   Free: 250.0 GB
```

---

### `memory`

**What it does:** Check RAM memory usage.

**Usage:**
```bash
python main.py memory
```

**Example:**
```bash
python main.py memory
```

**Output:**
```
✅ Memory Usage
   Total: 16.0 GB
   Used: 8.5 GB (53.1%)
   Available: 7.5 GB
```

---

### `cpu`

**What it does:** Check CPU usage and frequency.

**Usage:**
```bash
python main.py cpu
```

**Example:**
```bash
python main.py cpu
```

**Output:**
```
✅ CPU Usage
   Usage: 25%
   Cores: 8
   Frequency: 3600 MHz
```

---

### `info`

**What it does:** Get general system information.

**Usage:**
```bash
python main.py info
```

**Example:**
```bash
python main.py info
```

---

### `health`

**What it does:** Overall system health check with all metrics.

**Usage:**
```bash
python main.py health
```

**Example:**
```bash
python main.py health
```

**Output:**
```
✅ System Health: HEALTHY
   Timestamp: 2026-03-20 14:30:52

Checks:
   ✅ Disk: 50% used
   ✅ Memory: 53% used
   ✅ CPU: 25% used
```

---

### `large-files`

**What it does:** Find files larger than a threshold.

**Usage:**
```bash
python main.py large-files [directory] [n]
```

**Arguments:**

| Argument | Required | Description | Default |
|----------|----------|-------------|---------|
| `directory` | ❌ No | Directory to search | `~` |
| `n` | ❌ No | Number of files to return | `10` |

**Example:**
```bash
python main.py large-files
python main.py large-files ~/Downloads 20
```

---

## Use Cases

- **Disk full warning:** Check what's consuming space
- **Performance issues:** See if RAM or CPU is maxed out
- **Cleanup:** Find large files to delete
- **Monitoring:** Regular health checks via cron

---

## Tips & Tricks

- Run `health` for a quick overall status
- Use `large-files` to find space hogs
- Set up a cron job for daily health checks
- Check `/home` for user disk usage specifically

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "psutil not installed" | Run `pip install psutil` |
| Rate limited | Wait 60 seconds (30 calls/minute limit) |
| Permission denied | Some metrics need elevated permissions |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- psutil library (`pip install psutil`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/system-monitor)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
