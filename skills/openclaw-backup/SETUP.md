# OpenClaw Backup - Setup Guide

Complete setup guide for the OpenClaw Backup Pro skill.

---

## Prerequisites

Before starting, ensure you have:

- [ ] SMF Works Pro subscription (active)
- [ ] Python 3.7+ installed
- [ ] Sufficient disk space for backups
- [ ] OpenClaw installed and configured

**Estimated setup time:** 10 minutes

---

## Step 1: Install the Skill (2 minutes)

```bash
# Install via SMF CLI
smf install openclaw-backup

# Verify installation
smf list | grep openclaw-backup
```

---

## Step 2: Run Configuration Wizard (5 minutes)

```bash
smf run openclaw-backup --configure
```

### 2.1 Choose Backup Location

```
Step 1: Backup Location
Backup directory [~/.smf/backups]: 
```

**Default:** `~/.smf/backups` (recommended)

**Alternative locations:**
- External drive: `/mnt/backup/openclaw`
- Network storage: `~/NAS/backups/openclaw`
- Cloud sync folder: `~/Dropbox/backups/openclaw`

### 2.2 Set Retention Period

```
Step 2: Retention
Keep backups for how many days? [2]: 3
```

**Recommendation:** 2-3 days

**Storage calculation:**
- Backup size: ~50 MB
- 2 days retention: ~100 MB
- 7 days retention: ~350 MB

### 2.3 Review What Gets Backed Up

```
Step 3: What to Backup
Default paths:
  - ~/.openclaw/workspace
  - ~/.openclaw/memory
  - ~/.openclaw/config

Add additional paths? (comma-separated, or Enter to skip): 
```

**Optional additions:**
- Custom projects: `~/projects/openclaw-custom`
- Additional configs: `~/.config/openclaw-extra`

### 2.4 Schedule

```
Step 4: Schedule
Recommended: Run daily at 1:00 AM
Command: openclaw cron add --name 'openclaw-backup' --schedule '0 1 * * *' --command 'smf run openclaw-backup'

✅ Configuration saved!

Run 'smf run openclaw-backup' to create your first backup.
```

---

## Step 3: Create First Backup (2 minutes)

```bash
smf run openclaw-backup
```

Expected output:
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
✅ Backup complete!
```

---

## Step 4: Verify Backup (1 minute)

### List Backups

```bash
smf run openclaw-backup --list
```

Expected output:
```
💾 Available Backups (1 total):

1. openclaw_backup_20260324_013000.tar.gz
   Created: 2026-03-24 01:30
   Size: 45.23 MB
   Path: ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz
```

### Test Restore

```bash
# Test restore to temporary location
smf run openclaw-backup --restore ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz
```

Expected output:
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

**Clean up test restore:**
```bash
rm -rf ~/.openclaw_restored
```

---

## Step 5: Schedule Daily Backups (5 minutes)

### Option A: OpenClaw Cron (Recommended)

```bash
# Daily at 1:00 AM
openclaw cron add \
  --name "openclaw-backup" \
  --schedule "0 1 * * *" \
  --command "smf run openclaw-backup"
```

### Option B: System Cron

```bash
# Edit crontab
crontab -e

# Add for 1:00 AM daily
0 1 * * * /usr/local/bin/smf run openclaw-backup
```

### Option C: OpenClaw Heartbeat

Add to your `HEARTBEAT.md`:

```markdown
## Daily Tasks (1:00 AM)

- [ ] Run OpenClaw Backup
```

---

## Configuration Reference

### Full Config File

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

### Manual Configuration

Edit directly:

```bash
nano ~/.config/smf/skills/openclaw-backup/config.json
```

---

## Troubleshooting

### "Pro skill requires SMF Works subscription"

**Solution:**
1. Subscribe: https://smf.works/subscribe
2. Run: `smf login`
3. Verify: `ls -la ~/.smf/token`

### "No space left on device"

**Check disk space:**
```bash
df -h ~/.smf/backups
```

**Solutions:**
- Reduce retention_days
- Move backup_dir to external drive
- Clean up old backups: `smf run openclaw-backup --cleanup`

### "Permission denied"

**Fix permissions:**
```bash
# Ensure backup directory is writable
mkdir -p ~/.smf/backups
chmod 755 ~/.smf/backups

# Ensure OpenClaw directory is readable
ls -la ~/.openclaw
```

### Backup is too large

**Check what's being backed up:**
```bash
# List largest directories
du -sh ~/.openclaw/*

# Add exclusions to config
nano ~/.config/smf/skills/openclaw-backup/config.json
```

**Common large directories to exclude:**
- `node_modules` (already excluded)
- Large data files
- Cache directories
- Log files (already excluded)

---

## Restore Process

### Emergency Restore

If OpenClaw is corrupted or lost:

```bash
# 1. Stop OpenClaw
sudo systemctl stop openclaw

# 2. Find latest backup
ls -t ~/.smf/backups/openclaw_backup_*.tar.gz | head -1

# 3. Restore
smf run openclaw-backup --restore ~/.smf/backups/openclaw_backup_20260324_013000.tar.gz

# 4. Activate restore
rm -rf ~/.openclaw
mv ~/.openclaw_restored ~/.openclaw

# 5. Restart OpenClaw
sudo systemctl start openclaw
```

---

## Support

- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Documentation:** https://smfworks.com/skills/openclaw-backup

---

**Setup complete! Your OpenClaw is now protected 💾**
