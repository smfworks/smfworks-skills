# OpenClaw Backup

> Automatically back up your OpenClaw workspace with 2-day rolling retention — so you never lose your agent memory, skills, or configuration.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** System / Backup

---

## What It Does

OpenClaw Backup is an OpenClaw Pro skill that creates compressed backups of your OpenClaw workspace directory (`~/.openclaw/workspace`). It maintains a rolling 2-day retention policy — keeping the last 2 backups and automatically removing older ones to conserve disk space.

Schedule it via cron for automatic daily protection, or run manually before major changes.

**What it does NOT do:** It does not back up to cloud storage, encrypt backups, handle large files (>500 MB workspace), or back up OpenClaw's installation files (only the workspace).

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **Sufficient disk space** — typically 2× your workspace size

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/openclaw-backup
python3 main.py --configure
python3 main.py
```

---

## Quick Start

Create your first backup:

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

---

## Command Reference

### Default (no arguments)

Creates a new backup and applies retention policy.

```bash
python3 main.py
```

---

### `--list` / `-l`

Lists all available backups with size and creation date.

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

### `--restore BACKUP`

Restores your workspace from a backup file.

```bash
python3 main.py --restore /path/to/backup.tar.gz
```

**Important:** Restore overwrites the current workspace. Back up the current state first if needed.

---

### `--cleanup`

Manually triggers retention policy — removes backups beyond the configured retention count.

```bash
python3 main.py --cleanup
```

---

### `--configure` / `-c`

Interactive setup wizard for backup directory, retention count, and other settings.

```bash
python3 main.py --configure
```

---

## Use Cases

### 1. Daily automated backup (recommended)

Schedule via cron — see HOWTO.md for complete setup.

### 2. Manual backup before experimenting

Before making significant changes to your workspace:
```bash
python3 main.py
```

### 3. Restore after accidental deletion

```bash
python3 main.py --list
python3 main.py --restore /path/to/latest-backup.tar.gz
```

### 4. Pre-upgrade backup

Before upgrading OpenClaw:
```bash
python3 main.py
# Then proceed with upgrade
```

---

## Configuration

Config file: `~/.config/smf/skills/openclaw-backup/config.json` (or similar, set during `--configure`)

| Setting | Default | Description |
|---------|---------|-------------|
| Source directory | `~/.openclaw/workspace` | What to back up |
| Backup directory | `~/.openclaw/backups` | Where to store backups |
| Retention count | 2 | How many backups to keep |

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Error: Insufficient disk space`
**Fix:** Free up disk space, or change the backup directory to a drive with more space via `--configure`.

### Restore shows workspace files are different from backup
This is expected — you've made changes since the backup was taken.  
**Fix:** Review the diff carefully before restoring to avoid losing recent work.

### `No backups found`
**Fix:** Run `python3 main.py` first to create a backup.

---

## FAQ

**Q: What exactly is backed up?**  
A: The entire `~/.openclaw/workspace` directory, including MEMORY.md, AGENTS.md, daily notes, SOUL.md, IDENTITY.md, and any files you've created there.

**Q: Are backups encrypted?**  
A: No. Backups are `.tar.gz` compressed archives stored locally. Keep your backup directory on an encrypted volume if data security is a concern.

**Q: What happens if backup storage fills up?**  
A: The retention policy automatically removes oldest backups during each run. With 2-day retention and typical workspace size, storage use stays very low.

**Q: Can I back up to an external drive?**  
A: Yes — configure the backup directory to point to your external drive path via `--configure`.

---

---

## What Gets Backed Up

The backup covers your entire `~/.openclaw/workspace` directory, which includes:

| File/Folder | Description |
|-------------|-------------|
| `MEMORY.md` | Your long-term curated memory |
| `SOUL.md` | Your agent's identity and values |
| `AGENTS.md` | Workspace conventions and rules |
| `USER.md` | Information about you |
| `IDENTITY.md` | Agent name and persona |
| `TOOLS.md` | Local environment notes |
| `memory/` | Daily memory log files |
| `HEARTBEAT.md` | Heartbeat configuration |
| Any custom files | Documents, scripts, notes you've stored |

OpenClaw's installation files and the skills repository itself are NOT backed up — only your personal workspace data.

---

## Backup File Format

Backups are `.tar.gz` archives. You can inspect or extract them manually:

```bash
# List contents of a backup
tar -tzf /path/to/backup.tar.gz

# Extract to a specific directory for inspection
mkdir /tmp/backup-inspect
tar -xzf /path/to/backup.tar.gz -C /tmp/backup-inspect
```

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| Disk space | 2× workspace size recommended |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/openclaw-backup)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
