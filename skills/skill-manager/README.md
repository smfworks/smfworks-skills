# Skill Manager

> Interactive tool to view, backup, and cleanly remove installed OpenClaw skills

---

## What It Does

Skill Manager provides a visual terminal interface to manage your installed OpenClaw skills. See disk usage, identify Pro vs Free skills, backup before removal, and cleanly uninstall skills including their config files and wrapper scripts.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install skill-manager
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Open the interactive management UI:

```bash
smf run skill-manager
```

---

## Commands

### Interactive Mode

**What it does:** Visual TUI for managing skills.

**Usage:**
```bash
smf run skill-manager
```

**Interactive Commands:**

| Command | Action |
|---------|--------|
| `number` | Toggle selection by index (e.g., `1` selects first) |
| `a` | Select all skills |
| `n` | Clear selection |
| `b` | Backup selected skills |
| `r` | Remove selected skills |
| `q` | Quit |

**Example:**
```
SMF Skill Manager
================================================================================

Installed SMF Skills (5 total):

Name                      Tier       Size       Config
-----------------------------------------------------------------
file-organizer            Free       1.2 MB     Yes
coffee-briefing           Pro        2.3 MB     No
skill-manager             Free       0.8 MB     No

Selected: 0 skills

Commands: number toggle | a (all) | n (none) | b (backup) | r (remove) | q (quit)
Enter command: 1

Selected: 1 skill (1.2 MB)
Enter command: r

Are you sure? yes
✅ Removed 1 skill
```

---

### `--list`

**What it does:** Display simple text list of installed skills.

**Usage:**
```bash
smf run skill-manager --list
```

**Output:**
```
Installed SMF Skills (5 total):

Name                      Tier       Size       Installed
----------------------------------------------------------------
file-organizer            Free       1.2 MB     2026-03-20
coffee-briefing           Pro        2.3 MB     2026-03-21
skill-manager             Free       0.8 MB     2026-03-20

Total size: 8.9 MB
```

---

### `--remove`

**What it does:** Remove a specific skill.

**Usage:**
```bash
smf run skill-manager --remove [skill-name]
```

**Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--dry-run` | ❌ No | Preview without actually removing |

**Example:**
```bash
# Preview what would happen
smf run skill-manager --remove coffee-briefing --dry-run

# Actually remove
smf run skill-manager --remove coffee-briefing
```

---

### `--backup`

**What it does:** Backup a specific skill to `~/.smf/backups/`.

**Usage:**
```bash
smf run skill-manager --backup [skill-name]
```

**Example:**
```bash
smf run skill-manager --backup coffee-briefing
```

---

## What Gets Removed

When you remove a skill, Skill Manager cleans up:

| Location | Contents |
|----------|----------|
| `~/.smf/skills/<skill>/` | Skill code and files |
| `~/.config/smf/skills/<skill>/` | Skill configuration |
| `~/.local/bin/smf-<skill>` | CLI wrapper script |

---

## Use Cases

- **Testing cleanup:** Remove skills you tried out
- **Disk space:** Identify and remove large unused skills
- **Migration prep:** Backup all skills before moving machines
- **Organization:** See what skills you have installed

---

## Tips & Tricks

- Use `--dry-run` before removing to see exactly what will happen
- Always backup Pro skills before removing — they require a subscription to reinstall
- Run `skill-manager --list` to see disk usage at a glance
- Pro skills show a warning before removal

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No skills installed" | Install some skills first with `smf install <skill>` |
| Rich not available | Falls back to text mode; install rich with `pip install rich` |
| Permission denied | Check permissions: `ls -la ~/.smf/skills/` |

---

## Requirements

- Python 3.7+
- OpenClaw installed
- `rich` library (optional, for visual UI)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/skill-manager)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
