# Claw System Backup — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Create a Full System Backup](#1-how-to-create-a-full-system-backup)
2. [How to List and Verify Your Backups](#2-how-to-list-and-verify-your-backups)
3. [How to Restore from a Backup](#3-how-to-restore-from-a-backup)
4. [How to Restore a Single File](#4-how-to-restore-a-single-file)
5. [How to Reduce Backup Size with Exclusions](#5-how-to-reduce-backup-size-with-exclusions)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Create a Full System Backup

**What this does:** Creates a compressed `.tar.gz` archive of your configured source directory (default: home directory).

```bash
cd ~/smfworks-skills/skills/claw-system-backup
python3 main.py
```

Output:
```
💾 Creating system backup...

Source: /home/user
Archive: /home/user/.smf/backups/system-2024-03-15-090001.tar.gz
Excluding: .cache, __pycache__, node_modules

Progress: ████████████████████ 100%

✅ Backup complete!
   Archive size: 4.82 GB
   Files backed up: 47,382
   Time taken: 3m 42s
```

---

## 2. How to List and Verify Your Backups

**List backups:**

```bash
python3 main.py --list
```

**Verify integrity of the latest backup:**

```bash
python3 main.py --verify ~/.smf/backups/system-2024-03-15-090001.tar.gz
```

Output:
```
🔍 Verifying backup: system-2024-03-15-090001.tar.gz
   Testing archive integrity...
   ✅ Archive is valid — 47,382 files verified
```

**Why verify?** A backup that can't be restored is useless. Verification catches corrupted archives before you need them.

---

## 3. How to Restore from a Backup

**⚠️ Warning:** Restore overwrites files in your home directory with those from the backup. Back up your current state first if needed.

```bash
# Optional: create a backup of current state first
python3 main.py

# Then restore from desired backup
python3 main.py --restore ~/.smf/backups/system-2024-03-14-090001.tar.gz
```

---

## 4. How to Restore a Single File

For restoring one file without overwriting everything, use tar directly:

**Step 1 — Find the file path inside the archive:**

```bash
tar -tzf ~/.smf/backups/system-2024-03-14-090001.tar.gz | grep "important-document"
```

Output:
```
home/user/Documents/Projects/important-document.pdf
```

**Step 2 — Extract just that file:**

```bash
tar -xzf ~/.smf/backups/system-2024-03-14-090001.tar.gz -C /tmp/ home/user/Documents/Projects/important-document.pdf
```

**Step 3 — Move it back:**

```bash
mv /tmp/home/user/Documents/Projects/important-document.pdf ~/Documents/Projects/
```

---

## 5. How to Reduce Backup Size with Exclusions

**When to use it:** Your backup is taking too long or consuming too much disk space.

**Step 1 — Find large directories:**

```bash
python3 ~/smfworks-skills/skills/system-monitor/main.py large-files ~ 20
```

**Step 2 — Add them to exclusions via configure.**

```bash
python3 main.py --configure
```

At the exclusions prompt, add large directories you don't need backed up:
```
Additional directories to exclude: Downloads,Videos,VMs
```

**Step 3 — Verify the next backup is smaller.**

```bash
python3 main.py
python3 main.py --list
```

---

## 6. Automating with Cron

### Open crontab

```bash
crontab -e
```

### Example: Weekly backup every Sunday at 2 AM

```bash
0 2 * * 0 python3 /home/yourname/smfworks-skills/skills/claw-system-backup/main.py >> /home/yourname/logs/system-backup.log 2>&1
```

### Example: Daily backup at 1 AM

```bash
0 1 * * * python3 /home/yourname/smfworks-skills/skills/claw-system-backup/main.py >> /home/yourname/logs/system-backup.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 2 * * 0` | Sundays at 2 AM |
| `0 1 * * *` | Every day at 1 AM |
| `0 0 1 * *` | First day of each month at midnight |

---

## 7. Combining with Other Skills

**Claw System Backup + OpenClaw Backup:** Double protection — system backup weekly, workspace backup daily:

```bash
# Daily workspace backup (crontab)
0 2 * * * python3 /home/yourname/smfworks-skills/skills/openclaw-backup/main.py >> ~/logs/workspace-backup.log 2>&1

# Weekly system backup (crontab)
0 1 * * 0 python3 /home/yourname/smfworks-skills/skills/claw-system-backup/main.py >> ~/logs/system-backup.log 2>&1
```

**Claw System Backup + System Monitor:** Check disk before backing up:

```bash
python3 ~/smfworks-skills/skills/system-monitor/main.py disk
python3 ~/smfworks-skills/skills/claw-system-backup/main.py
```

---

## 8. Troubleshooting Common Issues

### Backup takes 30+ minutes

Your home directory is large, or includes large files.  
**Fix:** Run `du -sh ~/*/` to find the largest subdirectories, then add them to exclusions.

### `tar: Removing leading '/' from member names`

This warning is normal — it means tar is creating a portable archive (without the leading `/`).

### Backup interrupted (Ctrl+C or crash)

The partial `.tar.gz` file may be corrupt.  
**Fix:** Delete the partial file and re-run. `python3 main.py --list` will show any zero-byte entries to clean up.

### `--verify` reports archive invalid

The backup file is corrupted.  
**Fix:** Delete it and create a new backup.

---

## 9. Tips & Best Practices

**Back up to a different physical drive.** The default is `~/.smf/backups` on the same disk. If the disk fails, you lose both data and backup. Configure a separate drive or NAS as the backup destination.

**Verify backups monthly.** Run `--verify` on your latest backup once a month. Confirming the archive is valid is the only way to know you can actually restore when needed.

**Adjust exclusions to balance size vs completeness.** Downloads, videos, and `node_modules` are common size contributors that don't need backing up. Add them to exclusions to keep backups manageable.

**Schedule backups during off-hours.** Backups are I/O intensive. 1–3 AM minimizes impact on your work sessions.

**Keep at least one backup off-site.** Copy the most recent backup to an external drive or cloud storage periodically. Local-only backups don't protect against fire, theft, or flood.
