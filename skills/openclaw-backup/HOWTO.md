# OpenClaw Backup — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Create a Backup](#1-how-to-create-a-backup)
2. [How to List Your Backups](#2-how-to-list-your-backups)
3. [How to Restore from a Backup](#3-how-to-restore-from-a-backup)
4. [How to Clean Up Old Backups](#4-how-to-clean-up-old-backups)
5. [Automating with Cron](#5-automating-with-cron)
6. [Combining with Other Skills](#6-combining-with-other-skills)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)
8. [Tips & Best Practices](#8-tips--best-practices)

---

## 1. How to Create a Backup

**What this does:** Creates a compressed `.tar.gz` archive of your OpenClaw workspace directory and applies the retention policy.

**When to use it:** Before making major changes, before upgrading OpenClaw, or on a scheduled basis.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/openclaw-backup
```

**Step 2 — Run the backup.**

```bash
python3 main.py
```

Output:
```
💾 Creating OpenClaw workspace backup...

Backing up: /home/user/.openclaw/workspace
Archive: /home/user/.openclaw/backups/workspace-2024-03-15-090001.tar.gz

✅ Backup complete!
   Size: 2.34 MB
   Retention: Keeping last 2 backups
   Removed: 0 old backups
```

**Result:** A compressed backup of your entire workspace is saved.

---

## 2. How to List Your Backups

**What this does:** Shows all available backups with creation dates and sizes.

```bash
python3 main.py --list
```

Output:
```
💾 Available Backups (2 total):

1. workspace-2024-03-15-090001.tar.gz
   Created: 2024-03-15 09:00
   Size: 2.34 MB
   Path: /home/user/.openclaw/backups/workspace-2024-03-15-090001.tar.gz

2. workspace-2024-03-14-090002.tar.gz
   Created: 2024-03-14 09:00
   Size: 2.31 MB
   Path: /home/user/.openclaw/backups/workspace-2024-03-14-090002.tar.gz
```

---

## 3. How to Restore from a Backup

**What this does:** Restores your workspace from a backup archive.

**When to use it:** After accidental deletion, corruption, or when rolling back to a known good state.

### Steps

**Step 1 — List backups to find the one you want.**

```bash
python3 main.py --list
```

**Step 2 — Run restore with the backup path.**

```bash
python3 main.py --restore /home/user/.openclaw/backups/workspace-2024-03-14-090002.tar.gz
```

**⚠️ Warning:** Restore overwrites your current workspace. If you have recent work you want to keep, run a manual backup first before restoring.

```bash
# Back up current state first
python3 main.py
# Then restore from older backup
python3 main.py --restore /path/to/backup.tar.gz
```

**Result:** Your workspace is restored to the state captured in the backup.

---

## 4. How to Clean Up Old Backups

The skill automatically applies retention policy on each backup run. But you can trigger cleanup manually:

```bash
python3 main.py --cleanup
```

Output:
```
🧹 Cleaning up old backups...

✅ Removed 3 old backup(s)
```

---

## 5. Automating with Cron

### Open crontab

```bash
crontab -e
```

### Example: Daily backup at 2 AM

```bash
0 2 * * * python3 /home/yourname/smfworks-skills/skills/openclaw-backup/main.py >> /home/yourname/logs/openclaw-backup.log 2>&1
```

### Example: Backup before and after major work sessions

```bash
# Morning backup at 8 AM
0 8 * * * python3 /home/yourname/smfworks-skills/skills/openclaw-backup/main.py >> /home/yourname/logs/openclaw-backup.log 2>&1

# Evening backup at 10 PM
0 22 * * * python3 /home/yourname/smfworks-skills/skills/openclaw-backup/main.py >> /home/yourname/logs/openclaw-backup.log 2>&1
```

### Create the log directory

```bash
mkdir -p ~/logs
```

### Check backup logs

```bash
cat ~/logs/openclaw-backup.log | tail -20
```

---

## 6. Combining with Other Skills

**OpenClaw Backup + Claw System Backup:** Use both for complete machine protection:

```bash
# Back up OpenClaw workspace
python3 ~/smfworks-skills/skills/openclaw-backup/main.py

# Back up entire home directory
python3 ~/smfworks-skills/skills/claw-system-backup/main.py
```

**OpenClaw Backup + System Monitor:** Check disk space before backing up:

```bash
python3 ~/smfworks-skills/skills/system-monitor/main.py disk
python3 ~/smfworks-skills/skills/openclaw-backup/main.py
```

---

## 7. Troubleshooting Common Issues

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe) and re-authenticate.

### Backup failed — disk space error
**Fix:** Check available space: `df -h ~/.openclaw/backups`. Free up space or configure backup to a different location.

### `No backups found` when listing
**Fix:** Run `python3 main.py` first to create at least one backup.

### Restore seems to have no effect
**Fix:** OpenClaw may need to be restarted to pick up the restored workspace. Restart the OpenClaw service after restoring.

---

## 8. Tips & Best Practices

**Run a backup before any significant change.** Editing SOUL.md, major memory updates, or skill configuration changes are all good triggers for a manual backup.

**Increase retention if you're actively experimenting.** If you're doing a lot of experimentation and might need to roll back multiple days, increase the retention count via `--configure`. 5–7 days is reasonable.

**Verify backups monthly.** Run `--list` and confirm backups exist and have reasonable sizes. A zero-byte backup or missing backup means the cron job may have failed silently.

**Keep the log file.** The `>> ~/logs/openclaw-backup.log 2>&1` in the cron entry is essential. Review it periodically to ensure backups are completing successfully.

**Consider separate backup location for important machines.** The default backs up to the same machine. For critical setups, configure the backup to a different drive or network share so a disk failure doesn't take both your data and your backup.
