# Claw System Backup

> Create a complete compressed backup of your entire home directory — with integrity verification, rolling retention, and selective restore.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** System / Backup

---

## What It Does

Claw System Backup is an OpenClaw Pro skill that creates full compressed tar archives of your home directory (or any configured source), with configurable retention, backup verification via checksums, selective restore by file/folder, and scheduled cleanup of old archives.

Unlike OpenClaw Backup (which only backs up the workspace), Claw System Backup is a general-purpose home directory backup solution — covering all your documents, configurations, projects, and data.

**What it does NOT do:** It does not sync to cloud storage, encrypt archives (use an encrypted filesystem for that), back up mounted network drives, or handle incremental backups (each backup is a full archive).

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **`tar` command available** — standard on macOS and Linux
- [ ] **Sufficient disk space** — each backup equals the size of your home directory

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/claw-system-backup
python3 main.py --configure
```

---

## Quick Start

Create a backup:

```bash
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
   Retention: Kept last 3 backups, removed 0 old
```

---

## Command Reference

### Default — Create Backup

```bash
python3 main.py
```

Creates a new backup and applies retention policy.

---

### `--list` / `-l`

Lists all available backups.

```bash
python3 main.py --list
```

Output:
```
💾 Available Backups (3 total):

1. system-2024-03-15-090001.tar.gz
   Created: 2024-03-15 09:00
   Size: 4.82 GB
   Path: /home/user/.smf/backups/system-2024-03-15-090001.tar.gz

2. system-2024-03-14-090001.tar.gz
   Created: 2024-03-14 09:00
   Size: 4.79 GB
```

---

### `--verify BACKUP`

Verifies a backup archive's integrity by checking its contents.

```bash
python3 main.py --verify /path/to/backup.tar.gz
```

Output:
```
🔍 Verifying backup: system-2024-03-15-090001.tar.gz
   Testing archive integrity...
   ✅ Archive is valid — 47,382 files verified
```

---

### `--restore BACKUP`

Restores from a backup. Extracts the full archive to the source directory.

```bash
python3 main.py --restore /path/to/backup.tar.gz
```

---

### `--cleanup`

Removes old backups beyond the retention count.

```bash
python3 main.py --cleanup
```

---

### `--configure` / `-c`

Interactive configuration wizard.

```bash
python3 main.py --configure
```

---

## Use Cases

### 1. Weekly home directory backup

```bash
python3 main.py
```

### 2. Backup before OS upgrade

```bash
python3 main.py
# Then proceed with upgrade
```

### 3. Verify backup integrity monthly

```bash
python3 main.py --list
python3 main.py --verify /path/to/latest-backup.tar.gz
```

### 4. Restore specific files after accidental deletion

Extract from backup manually:
```bash
tar -xzf /path/to/backup.tar.gz home/user/Documents/important-file.txt -C /tmp/
```

---

## Configuration

Config file: `~/.config/smf/skills/claw-system-backup/config.json`

| Setting | Default | Description |
|---------|---------|-------------|
| Source directory | `~` (home directory) | What to back up |
| Backup directory | `~/.smf/backups` | Where to store backups |
| Retention count | 3 | Number of backups to keep |
| Exclude patterns | `.cache`, `__pycache__`, `node_modules`, `.git` | Directories to skip |

Excluded by default to reduce backup size:
- `.cache/` — browser and app caches (can be regenerated)
- `__pycache__/` — Python bytecode (regenerated automatically)
- `node_modules/` — npm packages (restored with `npm install`)

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### Backup is taking very long
Large home directories take time. The progress indicator shows completion percentage. Consider adding more exclusion patterns for large cache or build directories.

### `tar: command not found`
**Fix:** `tar` is standard on macOS and Linux. If missing: `sudo apt install tar` on Ubuntu.

### Disk full during backup
**Fix:** Reduce retention count, add exclusion patterns, or back up to a larger drive.

### `--verify` reports corrupt archive
**Fix:** The backup may have been interrupted. Delete it and create a fresh backup.

---

## FAQ

**Q: How much space do backups take?**  
A: Each backup equals roughly the size of your home directory minus excluded directories. With 3-backup retention, you need ~3× home directory size free.

**Q: Are node_modules excluded by default?**  
A: Yes — they're large, easily regenerated with `npm install`, and don't belong in backups. The exclusion list is configurable.

**Q: Can I back up just one directory instead of the whole home?**  
A: Yes — configure the source directory to any path via `--configure`.

**Q: How do I restore a single file?**  
A: Extract it manually: `tar -xzf backup.tar.gz --strip-components=1 -C /tmp/ path/to/file`

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| tar | Standard on macOS/Linux |
| SMF Works Pro | Required ($19.99/mo) |
| Disk space | ~3× home directory size (for 3-backup retention) |
| External APIs | None |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/claw-system-backup)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
