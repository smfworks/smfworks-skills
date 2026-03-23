# Claw System Backup — Setup Guide

**Estimated setup time:** 10 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| `tar` | Standard on macOS and Linux | Free |
| Free disk space | At least 3× your home directory size | — |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe).

```bash
openclaw auth status
```

Expected: Your email and `Pro` tier shown.

---

## Step 2 — Check Available Disk Space

```bash
df -h ~
```

You need at least 3× your home directory's current size for 3 rolling backups. Check your home directory size:

```bash
du -sh ~
```

---

## Step 3 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 4 — Configure the Skill

```bash
cd ~/smfworks-skills/skills/claw-system-backup
python3 main.py --configure
```

Configuration prompts:
```
Source directory [~]: 
Backup directory [~/.smf/backups]: 
Retention count (number of backups to keep) [3]: 
Additional directories to exclude (comma-separated): 

✅ Configuration saved!
```

Accept defaults or customize. If you want to back up to an external drive, enter its path as the backup directory.

---

## Step 5 — First Backup

```bash
python3 main.py
```

The first backup may take several minutes depending on your home directory size.

Expected output:
```
💾 Creating system backup...
✅ Backup complete!
   Archive size: 4.82 GB
   Retention: Kept last 3 backups
```

---

## Step 6 — Verify the Backup

```bash
python3 main.py --list
```

You should see the backup listed with size and timestamp.

Optionally verify integrity:
```bash
python3 main.py --verify /path/to/backup.tar.gz
```

---

## Configuration File

`~/.config/smf/skills/claw-system-backup/config.json`

Default exclusions (to reduce backup size):
- `.cache/`
- `__pycache__/`
- `node_modules/`
- `.git/`

---

## Set Up Automatic Weekly Backups

```bash
crontab -e
```

Add (Sunday at 2 AM):
```bash
0 2 * * 0 python3 /home/yourname/smfworks-skills/skills/claw-system-backup/main.py >> /home/yourname/logs/system-backup.log 2>&1
```

```bash
mkdir -p ~/logs
```

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**Backup takes too long** — Add large directories to the exclusion list in config. Common candidates: `~/Downloads`, `~/Videos`, `~/.local/share`.

**Disk space error** — Free up space or configure backup directory to a larger drive.

**`tar: command not found`** — Install tar: `sudo apt install tar` (Ubuntu/Debian).

---

## Next Steps

Setup complete. See **HOWTO.md** for backup, verify, restore, and automation walkthroughs.
