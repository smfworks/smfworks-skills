# OpenClaw Backup

> Backup and restore your OpenClaw workspace, skills, and settings

---

## What It Does

OpenClaw Backup creates complete backups of your entire OpenClaw setup — your workspace files, memory, skills, and configuration. Restore everything to a working state after a system crash, or migrate to a new machine.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install openclaw-backup
smf login
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Backup your entire OpenClaw workspace:

```bash
python main.py backup
```

---

## Commands

### `backup`

**What it does:** Create a full backup of your OpenClaw setup.

**Usage:**
```bash
python main.py backup [options]
```

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--dest` | ❌ No | Backup destination folder | `--dest ~/Backups` |

**Example:**
```bash
python main.py backup
python main.py backup --dest ~/OpenClaw-Backups
```

**Output:**
```
✅ OpenClaw Backup Created!
   ID: OPENCLAW-20260320-143052
   Location: ~/.openclaw-backups/OPENCLAW-20260320-143052/
   Size: 125 MB
   Included:
     - Workspace files
     - Memory files
     - Skills configuration
     - User settings
```

---

### `list`

**What it does:** Display all available backups.

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
📦 OpenClaw Backups:
------------------------------------------------------------
1. OPENCLAW-20260320-143052 | 125 MB | 2026-03-20 14:30
2. OPENCLAW-20260319-080000 | 120 MB | 2026-03-19 08:00
3. OPENCLAW-20260318-020000 | 118 MB | 2026-03-18 02:00
```

---

### `restore`

**What it does:** Restore OpenClaw from a previous backup.

**Usage:**
```bash
python main.py restore [backup-id]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `backup-id` | ✅ Yes | Backup ID to restore | `OPENCLAW-20260320-143052` |

**Example:**
```bash
python main.py restore OPENCLAW-20260320-143052
```

---

### `config`

**What it does:** Configure backup settings and destination.

**Usage:**
```bash
python main.py config
```

**Example:**
```bash
python main.py config
```

---

## Use Cases

- **Before updates:** Protect your setup before system upgrades
- **Migration:** Move OpenClaw to a new computer
- **Disaster recovery:** Restore after system crash
- **Version control:** Keep historical snapshots of your workspace

---

## Tips & Tricks

- Set up scheduled backups with cron for automatic protection
- Store backups on a separate drive for true disaster recovery
- Test restores periodically to verify your backups work
- Use `--dest` to organize backups by location

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Backup destination full" | Free up space or use different `--dest` |
| "Permission denied" | Check you have write access to destination |
| "Backup ID not found" | Check with `python main.py list` |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- Sufficient disk space for backups

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/openclaw-backup)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
