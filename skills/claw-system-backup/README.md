# Claw System Backup

> Complete system backup tool for your entire computer

---

## What It Does

Claw System Backup creates full backups of your system — files, folders, databases, and system configuration — so you can recover from disasters, migrate to new hardware, or simply restore accidentally deleted files. It runs completely locally with no cloud dependencies.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install claw-system-backup
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Run your first backup in seconds:

```bash
python main.py backup
```

---

## Commands

### `backup`

**What it does:** Create a full system backup of all specified paths.

**Usage:**
```bash
python main.py backup [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--dest` | ❌ No | Backup destination folder | `~/Backups` |
| `--exclude` | ❌ No | Patterns to exclude | `--exclude "*.log"` |

**Example:**
```bash
python main.py backup
python main.py backup --dest ~/Backups
python main.py backup --exclude "*.tmp" --exclude "__pycache__"
```

**Output:**
```
✅ Backup created successfully!
   ID: BACKUP-20260320-143052
   Location: ~/.claw-backups/BACKUP-20260320-143052/
   Size: 2.3 GB
   Files: 15,432
```

---

### `list`

**What it does:** Display all existing backups with their status and size.

**Usage:**
```bash
python main.py list
```

**Example:**
```bash
python main.py list
```

**Output:**
```
📦 Available Backups:
------------------------------------------------------------
1. BACKUP-20260320-143052 | 2.3 GB | 15,432 files | 2026-03-20 14:30
2. BACKUP-20260319-120000 | 2.1 GB | 14,891 files | 2026-03-19 12:00
3. BACKUP-20260318-080000 | 2.0 GB | 14,102 files | 2026-03-18 08:00
```

---

### `restore`

**What it does:** Restore files from a previous backup.

**Usage:**
```bash
python main.py restore [backup-id]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `backup-id` | ✅ Yes | ID of backup to restore | `BACKUP-20260320-143052` |

**Example:**
```bash
python main.py restore BACKUP-20260320-143052
```

**Output:**
```
🔄 Restoring from BACKUP-20260320-143052...
   Restored: 15,432 files
   Location: ~/.claw-backups/BACKUP-20260320-143052/
✅ Restore complete!
```

---

### `status`

**What it does:** Show current backup status and what would be included in next backup.

**Usage:**
```bash
python main.py status
```

**Example:**
```bash
python main.py status
```

**Output:**
```
📊 Backup Status:
   Last backup: 2026-03-20 14:30 (2 hours ago)
   Next scheduled: 2026-03-21 02:00
   Files to backup: ~15,500
   Estimated size: 2.3 GB
```

---

### `schedule`

**What it does:** Set up automatic backup schedule using cron.

**Usage:**
```bash
python main.py schedule [cron-expression]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `cron-expression` | ✅ Yes | Standard cron format | `"0 2 * * *"` |

**Example:**
```bash
# Daily at 2 AM
python main.py schedule "0 2 * * *"

# Weekly on Sunday at 3 AM
python main.py schedule "0 3 * * 0"

# Every 6 hours
python main.py schedule "0 */6 * * *"
```

---

## Use Cases

- **Disaster recovery:** Restore your system after hardware failure
- **Migration:** Move to a new computer by restoring your backup
- **Accidental deletion:** Recover files you accidentally deleted
- **Before major changes:** Create a backup before system updates
- **Archive old state:** Keep historical snapshots of your system

---

## Tips & Tricks

- Run `python main.py status` before backups to estimate size and time
- Use `--exclude` patterns to skip large temporary files
- Set up scheduled backups with `schedule` for hands-off protection
- Store backups on an external drive for true disaster recovery
- Test restores periodically to ensure your backups work

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Backup destination full" | Free up space or specify a different `--dest` |
| "Permission denied" | Run with appropriate permissions |
| Backup too large | Use `--exclude` to skip logs, cache, temp files |
| Restore fails | Ensure backup ID is correct; check disk space |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Sufficient disk space for backups
- (Optional) `rsync` for efficient incremental backups

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/claw-system-backup)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
