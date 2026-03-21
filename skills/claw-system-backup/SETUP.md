# Claw System Backup - Setup Guide

Complete setup guide for the Claw System Backup Pro skill.

---

## Prerequisites

- [ ] SMF Works Pro subscription (active)
- [ ] Root/sudo access on Linux system
- [ ] Sufficient disk space (2-10 GB recommended)
- [ ] `tar` command available

**Estimated setup time:** 15 minutes

---

## Step 1: Install (2 minutes)

```bash
smf install claw-system-backup
smf list | grep claw-system-backup
```

---

## Step 2: Configure (5 minutes)

```bash
smf run claw-system-backup --configure
```

### Backup Location
```
Backup directory [~/.smf/system-backups]: /mnt/backup/system
```

### Backup Type
```
Backup type [incremental]: incremental
```

**Types:**
- `full` - Entire system (5-20 GB)
- `incremental` - Key files + home (1-5 GB) ⭐ Recommended
- `home-only` - Just /home (500 MB - 2 GB)

### Retention
```
Keep backups for how many weeks? [2]: 2
```

### Compression
```
Compression [gzip]: gzip
```

**Options:** gzip (fast), bzip2 (smaller), xz (smallest), none

---

## Step 3: Test Backup (5 minutes)

```bash
sudo smf run claw-system-backup
```

Expected output:
```
💾 Claw System Backup
   Type: incremental
   Sources: /etc, /home
   
✅ Backup complete!
   Size: 2.34 GB
```

---

## Step 4: Schedule Weekly

```bash
# Sundays at 2:00 AM
openclaw cron add \
  --name "claw-system-backup" \
  --schedule "0 2 * * 0" \
  --command "sudo smf run claw-system-backup"
```

---

## Quick Reference

| Command | Action |
|---------|--------|
| `sudo smf run claw-system-backup` | Create backup |
| `smf run claw-system-backup --list` | List backups |
| `smf run claw-system-backup --cleanup` | Remove old backups |
| `smf run claw-system-backup --verify <file>` | Verify integrity |

---

**Setup complete! Your system is protected 💾**
