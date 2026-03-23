# Skill Manager — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| smfworks-skills repository | Cloned via git | Free |
| Skills installed in `~/.smf/skills/` | The skills you want to manage | Depends on skill |
| rich (optional) | Python library for enhanced terminal display | Free |

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.9.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — (Optional) Install rich for Enhanced Display

```bash
pip install rich
```

Without `rich`, the skill uses plain-text output. Both modes are fully functional.

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/skill-manager
```

---

## Step 5 — Verify

```bash
python3 main.py --help
```

Expected:
```
usage: main.py [-h] [--list] [--remove SKILL] [--backup SKILL] [--dry-run]

SMF Skill Manager - Visual tool for managing installed OpenClaw skills

optional arguments:
  -h, --help            show this help message and exit
  --list, -l            List installed skills (simple view)
  --remove SKILL, -r SKILL
                        Remove a specific skill
  --backup SKILL, -b SKILL
                        Backup a specific skill
  --dry-run, -d         Show what would be done without doing it
```

---

## Verify Your Setup

List installed skills:

```bash
python3 main.py --list
```

If you have skills installed, you'll see them listed. If you see `No skills installed.`, that's correct if you haven't installed any SMF skills yet — the skill manager itself is working correctly.

---

## Configuration Options

No configuration needed. Skills are detected automatically from `~/.smf/skills/`.

---

## Troubleshooting

**`No skills installed.`** — Install some skills first. This means the manager is working; there's just nothing to manage yet.

**Interactive UI looks garbled** — Use `--list`, `--remove`, and `--backup` flags instead of the interactive mode.

---

## Quick Reference

```bash
# List all installed skills
python3 main.py --list

# Back up a skill before making changes
python3 main.py --backup skill-name

# Remove a skill you no longer need
python3 main.py --remove skill-name

# Preview removal without doing it
python3 main.py --remove skill-name --dry-run

# Launch interactive UI
python3 main.py
```

## Next Steps

See **HOWTO.md** for walkthroughs on backup, removal, and the interactive UI.
