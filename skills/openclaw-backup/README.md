# OpenClaw Backup - SMF Works Pro Skill

💾 **Daily backup of your OpenClaw agent with 2-day rolling retention.**

## Overview

OpenClaw Backup automatically backs up your OpenClaw workspace, memory, and configuration daily. Maintains a rolling 2-day history with simple one-command restore.

**Schedule:** Daily at 1:00 AM (configurable)
**Retention:** 2 days (configurable)
**Tier:** Pro (requires SMF Works subscription)

---

## Requirements

- **SMF Works Subscription:** Pro tier ($19.99/mo)
- **Disk Space:** Sufficient space for backups (typically 10-100 MB per backup)
- **No External APIs:** Fully local operation

---

## What Gets Backed Up

By default, the skill backs up:

| Path | Contents |
|------|----------|
| `~/.openclaw/workspace` | Your workspace files and projects |
| `~/.openclaw/memory` | Memory files and logs |
| `~/.openclaw/config` | Configuration files |

**Excluded by default:**
- Log files (`*.log`)
- Python cache (`__pycache__`)
- Git repositories (`.git`)
- Node modules (`node_modules`)
- Virtual environments (`.venv`, `venv`)

---

## Installation

```bash
smf install openclaw-backup
```

---

## Quick Start

### Step 1: Configure

```bash
smf run openclaw-backup --configure
```

The wizard will ask for:
- Backup directory location
- Retention period (default: 2 days)
- Additional paths to include (optional)

### Step 2: Create First Backup

```bash
smf run openclaw-backup
```

### Step 3: Schedule Daily Backups

```bash
openclaw cron add \
  --name "openclaw-backup" \
  --schedule "0 1 * * *" \
  --command "smf run openclaw-backup"
```

---

## Usage

### Create Backup

```bash
smf run openclaw-backup
```

Output:
```
📦 Creating backup: openclaw_backup_20260324_013000
   Destination: ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz
   ✓ Added: ~/.openclaw/workspace
   ✓ Added: ~/.openclaw/memory
   ✓ Added: ~/.openclaw/config

✅ Backup complete: openclaw_backup_20260324_013000
   Size: 45.23 MB
   Location: ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz

🧹 Cleaning up old backups...
✅ Removed 1 old backup(s)

✅ Backup complete!
```

### List Backups

```bash
smf run openclaw-backup --list
```

Output:
```
💾 Available Backups (3 total):

1. openclaw_backup_20260324_013000.tar.gz
   Created: 2026-03-24 01:30
   Size: 45.23 MB
   Path: ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz

2. openclaw_backup_20260323_013000.tar.gz
   Created: 2026-03-23 01:30
   Size: 44.89 MB
   Path: ~/.smf/backups/openclaw_backup_20260323_013000.tar.gz
```

### Restore from Backup

```bash
smf run openclaw-backup --restore ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz
```

Output:
```
📦 Restoring from: openclaw_backup_20260324_013000.tar.gz
   Destination: ~/.openclaw_restored

✅ Restore complete!
   Files restored to: ~/.openclaw_restored

To activate this restore:
   1. Stop OpenClaw if running
   2. Replace ~/.openclaw with restored files:
      rm -rf ~/.openclaw && mv ~/.openclaw_restored ~/.openclaw
   3. Restart OpenClaw
```

### Manual Cleanup

```bash
smf run openclaw-backup --cleanup
```

---

## Configuration

### Configuration File

```
~/.config/smf/skills/openclaw-backup/config.json
```

### Example Configuration

```json
{
  "backup_dir": "~/.smf/backups",
  "retention_days": 2,
  "include_paths": [
    "~/.openclaw/workspace",
    "~/.openclaw/memory",
    "~/.openclaw/config"
  ],
  "exclude_patterns": [
    "*.log",
    "__pycache__",
    ".git",
    "node_modules",
    ".venv",
    "venv"
  ],
  "compress": true,
  "verify": true
}
```

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `backup_dir` | No | `~/.smf/backups` | Where to store backups |
| `retention_days` | No | `2` | How many days to keep backups |
| `include_paths` | No | See above | Paths to backup |
| `exclude_patterns` | No | See above | Patterns to exclude |
| `compress` | No | `true` | Use gzip compression |
| `verify` | No | `true` | Verify backup integrity |

---

## Scheduling

### OpenClaw Cron (Recommended)

```bash
# Daily at 1:00 AM
openclaw cron add \
  --name "openclaw-backup" \
  --schedule "0 1 * * *" \
  --command "smf run openclaw-backup"
```

### System Cron

```bash
# Edit crontab
crontab -e

# Add for 1:00 AM daily
0 1 * * * /usr/local/bin/smf run openclaw-backup
```

---

## Restore Process

To restore your OpenClaw from a backup:

### Step 1: Stop OpenClaw

```bash
# If running as a service
sudo systemctl stop openclaw

# Or find and kill the process
pkill -f openclaw
```

### Step 2: Restore Files

```bash
# Option A: Use the skill
smf run openclaw-backup --restore ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz

# Option B: Manual restore
cd ~
rm -rf ~/.openclaw
tar -xzf ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz
mv openclaw_backup_*/openclaw ~/.openclaw
```

### Step 3: Restart OpenClaw

```bash
# If running as a service
sudo systemctl start openclaw

# Or start manually
openclaw start
```

---

## Backup Format

Backups are stored as compressed tar.gz archives:

```
~/.smf/backups/
├── openclaw_backup_20260324_013000.tar.gz
├── openclaw_backup_20260323_013000.tar.gz
└── openclaw_backup_20260322_013000.tar.gz
```

Archive contents:
```
openclaw_backup_20260324_013000/
├── workspace/
├── memory/
└── config/
```

---

## Troubleshooting

### "Pro skill requires SMF Works subscription"

Subscribe at [https://smf.works/subscribe](https://smf.works/subscribe) then run `smf login`.

### "No space left on device"

- Check disk space: `df -h`
- Reduce retention_days in config
- Move backup_dir to larger drive

### Backup is too large

- Add more exclude_patterns to config
- Exclude large data directories
- Use --list to see what's being backed up

### "Permission denied"

- Ensure you have read access to ~/.openclaw
- Check write permissions to backup_dir

---

## Data & Privacy

- **All operations are local** - No data leaves your machine
- **Backups stored locally** - You control where they go
- **No external APIs** - No cloud services involved
- **Encrypted at rest** - Filesystem encryption applies

---

## Support

- **Documentation:** https://smfworks.com/skills/openclaw-backup
- **Issues:** https://github.com/smfworks/smfworks-skills/issues

---

*Powered by SMF Works | Pro Skill | Local-First*
