# OpenClaw Backup — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| Free disk space | At least 2× your workspace size | — |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe).

```bash
openclaw auth status
```

Expected: Your email and `Pro` tier shown.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/openclaw-backup
```

---

## Step 4 — Configure

```bash
python3 main.py --configure
```

Accept defaults or customize:
- Backup directory (default: `~/.openclaw/backups`)
- Retention count (default: 2 days)

---

## Step 5 — Create Your First Backup

```bash
python3 main.py
```

Expected:
```
💾 Creating OpenClaw workspace backup...
✅ Backup complete!
   Size: 2.34 MB
   Retention: Keeping last 2 backups
```

---

## Step 6 — Verify

```bash
python3 main.py --list
```

You should see your backup listed with size and creation timestamp.

---

## Configuration Options

Config file: `~/.config/smf/skills/openclaw-backup/config.json`

| Setting | Default | Description |
|---------|---------|-------------|
| Backup directory | `~/.openclaw/backups` | Where to store backups |
| Retention | 2 | Number of backups to keep |

---

## Set Up Automatic Daily Backups

Add to crontab for automatic protection:

```bash
crontab -e
```

Add:
```bash
0 2 * * * python3 /home/yourname/smfworks-skills/skills/openclaw-backup/main.py >> /home/yourname/logs/openclaw-backup.log 2>&1
```

Create the log directory:
```bash
mkdir -p ~/logs
```

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**Not enough disk space** — Use `df -h` to check available space. Free up disk or change backup location.

**`python3: command not found`** — Install Python 3.8+.

---

## Next Steps

Setup complete. See **HOWTO.md** for backup, restore, and automation walkthroughs.
