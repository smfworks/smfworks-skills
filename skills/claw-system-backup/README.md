# Claw System Backup - SMF Works Pro Skill

💾 **Weekly full Linux system backup with compression and verification.**

## Overview

Claw System Backup creates compressed archives of your Linux system. Supports full system, incremental, or home-directory-only backups with automatic retention management.

**Schedule:** Weekly on Sundays at 2:00 AM (configurable)
**Retention:** 2 weeks (configurable)
**Tier:** Pro (requires SMF Works subscription + root access)

---

## Requirements

- **SMF Works Subscription:** Pro tier ($19.99/mo)
- **Root/Sudo Access:** Required for full system backup
- **Disk Space:** Sufficient space for backups (typically 1-10 GB)
- **Linux System:** Any modern Linux distribution

---

## What Gets Backed Up

### Backup Types

| Type | Includes | Size | Use Case |
|------|----------|------|----------|
| **full** | Entire filesystem | 5-20 GB | Complete disaster recovery |
| **incremental** | /etc, /home, /root, /boot | 1-5 GB | Recommended for most users |
| **home-only** | /home directory | 500 MB - 2 GB | Quick user data backup |

### Incremental Backup (Recommended)
Includes:
- `/etc` - System configuration
- `/home` - User home directories
- `/root` - Root user files
- `/boot` - Boot files
- Package databases

**Excluded:**
- `/proc`, `/sys`, `/dev`, `/run` - Virtual filesystems
- `/tmp`, `/var/tmp` - Temporary files
- `/var/cache` - Cache directories
- Previous backups

---

## Installation

```bash
smf install claw-system-backup
```

---

## Quick Start

### Step 1: Configure

```bash
smf run claw-system-backup --configure
```

### Step 2: Create First Backup

```bash
sudo smf run claw-system-backup
```

### Step 3: Schedule Weekly Backups

```bash
# Weekly on Sundays at 2:00 AM
openclaw cron add \
  --name "claw-system-backup" \
  --schedule "0 2 * * 0" \
  --command "sudo smf run claw-system-backup"
```

---

## Usage

### Create Backup

```bash
sudo smf run claw-system-backup
```

Output:
```
💾 Claw System Backup
   Type: incremental
   Destination: ~/.smf/system-backups/system_incremental_20260324_020000.tar.gz
   Sources: /etc, /home

📦 Creating backup (this may take several minutes)...

✅ Backup complete!
   File: system_incremental_20260324_020000.tar.gz
   Size: 2.34 GB
   Location: ~/.smf/system-backups/system_incremental_20260324_020000.tar.gz

🔍 Verifying backup...
   ✅ Backup verified successfully
   Contains 152,847 files/directories

🧹 Cleaning up old backups...
✅ Removed 1 old backup(s)

✅ Backup complete!
```

### List Backups

```bash
smf run claw-system-backup --list
```

Output:
```
💾 System Backups (3 total):

1. system_incremental_20260324_020000.tar.gz
   Created: 2026-03-24 02:00
   Size: 2.34 GB
   Path: ~/.smf/system-backups/system_incremental_20260324_020000.tar.gz

2. system_incremental_20260317_020000.tar.gz
   Created: 2026-03-17 02:00
   Size: 2.28 GB

Total size: 6.96 GB
```

### Verify Backup

```bash
smf run claw-system-backup --verify ~/.smf/system-backups/system_incremental_20260324_020000.tar.gz
```

### Restore (Advanced)

**Warning:** Restore operations can overwrite system files. Use with caution.

```bash
# Boot from live USB first, then:
smf run claw-system-backup --restore ~/.smf/system-backups/system_full_20260324_020000.tar.gz
```

---

## Configuration

### Configuration File

```
~/.config/smf/skills/claw-system-backup/config.json
```

### Example Configuration

```json
{
  "backup_dir": "~/.smf/system-backups",
  "retention_weeks": 2,
  "backup_type": "incremental",
  "exclude_paths": [
    "/proc",
    "/sys",
    "/dev",
    "/run",
    "/tmp",
    "/var/cache"
  ],
  "include_home": true,
  "include_etc": true,
  "compression": "gzip",
  "verify": true
}
```

### Configuration Options

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `backup_dir` | No | `~/.smf/system-backups` | Where to store backups |
| `retention_weeks` | No | `2` | How many weeks to keep |
| `backup_type` | No | `incremental` | full, incremental, home-only |
| `compression` | No | `gzip` | gzip, bzip2, xz, none |
| `verify` | No | `true` | Verify after creation |

---

## Scheduling

### Weekly with OpenClaw Cron

```bash
# Sundays at 2:00 AM
openclaw cron add \
  --name "claw-system-backup" \
  --schedule "0 2 * * 0" \
  --command "sudo smf run claw-system-backup"
```

### System Cron

```bash
crontab -e

# Weekly backup
0 2 * * 0 /usr/local/bin/smf run claw-system-backup
```

---

## Restore Process

### Emergency System Restore

**Prerequisites:**
- Boot from Linux live USB/DVD
- Mount backup drive
- Root shell

```bash
# 1. Mount backup drive
mkdir /mnt/backup
mount /dev/sdb1 /mnt/backup

# 2. Mount target filesystem
mkdir /mnt/target
mount /dev/sda1 /mnt/target

# 3. Restore
smf run claw-system-backup --restore /mnt/backup/system_full_20260324_020000.tar.gz

# 4. Reinstall bootloader
grub-install /dev/sda
update-grub
```

---

## Troubleshooting

### "Permission denied"

Run with sudo:
```bash
sudo smf run claw-system-backup
```

### "No space left on device"

```bash
# Check space
df -h ~/.smf/system-backups

# Clean up old backups
smf run claw-system-backup --cleanup

# Move backup location
smf run claw-system-backup --configure
# Set backup_dir to external drive
```

### "Command not found: tar"

```bash
# Install tar
sudo apt-get install tar
```

---

## Data & Privacy

- **All operations are local** - No data leaves your machine
- **No external APIs** - No cloud services
- **Compression** - Reduces size and obscures contents
- **You control location** - External drives, NAS, etc.

---

## Support

- **Documentation:** https://smfworks.com/skills/claw-system-backup
- **Issues:** https://github.com/smfworks/smfworks-skills/issues

---

*Powered by SMF Works | Pro Skill | Local-First*
