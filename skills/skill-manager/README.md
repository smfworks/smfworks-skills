# Skill Manager

> View, back up, and remove your installed OpenClaw skills — with an interactive terminal UI or simple command-line flags.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** System / Skill Management

---

## What It Does

Skill Manager is an OpenClaw skill that gives you visibility and control over your installed SMF Works skills. Launch the interactive terminal UI to browse all installed skills, see their sizes and installation dates, select any combination, and back them up or remove them. Or use command-line flags for quick, scriptable operations.

Skills are detected in `~/.smf/skills/`. Backups are saved to `~/.smf/backups/`. The tool optionally uses the `rich` library for a polished table display, but falls back gracefully if it's not installed.

**What it does NOT do:** It does not install new skills (use `git clone` or your skill installer for that), search online for skills, update skill versions, or manage skill configuration files.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **Skills installed** in `~/.smf/skills/`
- [ ] **No subscription required** — free tier skill
- [ ] **rich Python package** — optional, for enhanced display (graceful fallback if not installed)

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/skill-manager
# Optional: install rich for enhanced display
pip install rich
python3 main.py --list
```

---

## Quick Start

List all installed skills:

```bash
python3 main.py --list
```

Output:
```
Installed SMF Skills (8 total):

Name                      Tier       Size       Installed
------------------------------------------------------------
coffee-briefing           💎 pro     0.1 MB     2024-02-15
daily-news-digest         🎁 free    0.1 MB     2024-01-20
file-organizer            🎁 free    0.1 MB     2024-01-10
lead-capture              💎 pro     0.2 MB     2024-02-01
morning-commute           💎 pro     0.1 MB     2024-02-15
pdf-toolkit               🎁 free    0.1 MB     2024-01-12
system-monitor            🎁 free    0.1 MB     2024-01-10
task-manager              💎 pro     0.2 MB     2024-03-01

Total size: 1.0 MB
```

---

## Command Reference

### `--list` / `-l`

Prints a simple list of all installed skills with tier, size, and install date.

**Usage:**
```bash
python3 main.py --list
```

**Output:** Table showing name, tier indicator (💎 Pro / 🎁 Free), size in MB, and installation date for each installed skill.

---

### `--remove SKILL` / `-r SKILL`

Removes a specific skill by name. The skill's directory in `~/.smf/skills/` is deleted.

**Usage:**
```bash
python3 main.py --remove skill-name
```

**Example:**
```bash
python3 main.py --remove morning-commute
```

**Output:**
```
Removing morning-commute...
✅ morning-commute removed successfully.
```

---

### `--backup SKILL` / `-b SKILL`

Creates a backup of a specific skill to `~/.smf/backups/`.

**Usage:**
```bash
python3 main.py --backup skill-name
```

**Example:**
```bash
python3 main.py --backup coffee-briefing
```

**Output:**
```
Backing up coffee-briefing...
✅ coffee-briefing backed up to ~/.smf/backups/
```

---

### `--dry-run` / `-d`

Combined with `--remove`, shows what would be deleted without actually doing it.

**Usage:**
```bash
python3 main.py --remove skill-name --dry-run
```

**Example:**
```bash
python3 main.py --remove lead-capture --dry-run
```

**Output:**
```
[DRY RUN] Would remove: /home/user/.smf/skills/lead-capture
```

---

### Interactive Mode (no arguments)

Launches the full interactive terminal UI. Requires no arguments.

**Usage:**
```bash
python3 main.py
```

The interactive UI shows a numbered list of installed skills. You can select any combination and perform bulk backup or removal operations.

**Interactive commands:**

| Key | Action |
|-----|--------|
| Number (e.g., `1`) | Toggle selection on/off for that skill |
| `a` | Select all skills |
| `n` | Clear all selections |
| `b` | Backup selected skills |
| `r` | Remove selected skills |
| `q` | Quit |

---

## Use Cases

### 1. See what skills are installed and how much space they use

```bash
python3 main.py --list
```

---

### 2. Remove a skill you no longer use

```bash
python3 main.py --remove morning-commute
```

---

### 3. Back up a skill before modifying it

```bash
python3 main.py --backup coffee-briefing
```

---

### 4. Interactive cleanup of multiple old skills

```bash
python3 main.py
# Use numbers to select skills to remove
# Press r to remove selected
```

---

### 5. Preview what a removal would do

```bash
python3 main.py --remove task-manager --dry-run
```

---

## Configuration

No configuration file needed. The skill uses fixed paths:

| Setting | Value |
|---------|-------|
| Skills directory | `~/.smf/skills/` |
| Backups directory | `~/.smf/backups/` |
| Config directory | `~/.config/smf/skills/` |

---

## Troubleshooting

### `No skills installed.`
No skills found in `~/.smf/skills/`.  
**Fix:** Install skills first. Check the SMF Works documentation for skill installation.

### `❌ Backup failed.`
The backup operation failed — likely a permission issue or the skill name doesn't exist.  
**Fix:** Check the skill name exactly matches what's shown in `--list`.

### `❌ [error message]` on remove
The skill directory couldn't be removed.  
**Fix:** Check you have permissions on `~/.smf/skills/`. Use `--dry-run` first to confirm the skill exists.

### Interactive UI shows garbled output
This can happen in some terminal emulators without full Unicode support.  
**Fix:** Try a different terminal, or use `--list`, `--remove`, and `--backup` flags instead of the interactive mode.

---

## FAQ

**Q: Does removing a skill delete its configuration?**  
A: The `--remove` command removes the skill directory in `~/.smf/skills/`. Configuration files in `~/.config/smf/skills/` may remain. You can manually clean those up.

**Q: Where are backups stored?**  
A: `~/.smf/backups/`. Each backup is a copy of the skill directory.

**Q: Does this skill manage skills from other repositories?**  
A: It detects any skill directory found in `~/.smf/skills/`, regardless of source.

**Q: Does `rich` need to be installed?**  
A: No. Without `rich`, the skill falls back to a simple plain-text display. Both modes provide the same functionality.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| rich | Optional (graceful fallback) |
| OpenClaw | Any version |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/skill-manager)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
