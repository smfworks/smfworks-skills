# Skill Manager - SMF Works Free Skill

🎛️ **Visual tool for managing installed OpenClaw skills.**

## Overview

Skill Manager provides an interactive terminal UI to view, backup, and cleanly remove installed SMF Skills. Perfect for testing skills on a machine and cleaning up when you're done.

**Key Features:**
- 📊 Visual table view of all installed skills
- ✅ Checkbox selection for batch operations
- 💾 One-click backup before removal
- 🗑️ Clean removal (skill files + config + wrapper)
- 📏 See disk usage and tier (Free/Pro)
- ⚠️ Safety warnings for Pro skills

## Installation

```bash
smf install skill-manager
```

## Requirements

- Python 3.7+
- `rich` library (auto-installed if available)
- No external APIs — fully local

## Usage

### Interactive Mode (Recommended)

```bash
smf run skill-manager
```

**Interactive Commands:**

| Command | Action |
|---------|--------|
| `number` | Toggle selection by index (e.g., `1` selects first skill) |
| `a` | Select all skills |
| `n` | Clear selection (none) |
| `b` | Backup selected skills |
| `r` | Remove selected skills |
| `q` | Quit |

### List View (Simple)

```bash
smf run skill-manager --list
```

Output:
```
Installed SMF Skills (5 total):

Name                      Tier       Size       Installed
--------------------------------------------------------
file-organizer            🎁 Free    1.2 MB     2026-03-20
coffee-briefing           💎 Pro     2.3 MB     2026-03-21
morning-commute           💎 Pro     3.1 MB     2026-03-21
openclaw-backup           💎 Pro     0.8 MB     2026-03-22
claw-system-backup        💎 Pro     1.5 MB     2026-03-22

Total size: 8.9 MB
```

### Remove Specific Skill

```bash
# Dry run (see what would happen)
smf run skill-manager --remove coffee-briefing --dry-run

# Actually remove
smf run skill-manager --remove coffee-briefing
```

### Backup Specific Skill

```bash
smf run skill-manager --backup coffee-briefing
```

Backup goes to: `~/.smf/backups/coffee-briefing_20260324_123456/`

## What Gets Removed

When you remove a skill, Skill Manager cleans up:

| Location | Contents |
|----------|----------|
| `~/.smf/skills/<skill>/` | Skill code and files |
| `~/.config/smf/skills/<skill>/` | Skill configuration |
| `~/.local/bin/smf-<skill>` | CLI wrapper script |

## Visual Features

### Interactive Table View

```
┌────────────────────────────────────────────────────────────────┐
│                    SMF Skill Manager                           │
├────────────────────────────────────────────────────────────────┤
│ Select │ Name              │ Tier   │ Size   │ Config │ Description      │
├────────────────────────────────────────────────────────────────┤
│ [✓]    │ file-organizer    │ Free   │ 1.2 MB │ ✓      │ Organize files │
│ [ ]    │ coffee-briefing   │ Pro    │ 2.3 MB │ ✗      │ Morning briefing│
│ [✓]    │ old-test-skill    │ Free   │ 5.6 MB │ ✓      │ (outdated)      │
│ [ ]    │ morning-commute   │ Pro    │ 3.1 MB │ ✗      │ Commute info    │
└────────────────────────────────────────────────────────────────┘

Selected: 2 skills (6.8 MB)
⚠️  0 Pro skills selected

Commands: number toggle | a (all) | n (none) | b (backup) | r (remove) | q (quit)
Enter command:
```

### Removal Confirmation

```
The following will be REMOVED:
  • file-organizer
  • old-test-skill

Total: 2 skills

⚠️  Warning: 0 Pro skills will be removed.

Create backup first? [Y/n]:
Are you sure? [y/N]: y

✅ Removed 2 skills
```

## Safety Features

- **Dry Run Mode:** Preview what will happen before doing it
- **Backup Option:** Automatically backup before removal
- **Pro Skill Warning:** Alerts when removing subscription skills
- **Confirmation Required:** Double-check before destructive actions
- **Config Preservation:** Option to keep or remove config files

## Use Cases

### Testing Skills

```bash
# Install a skill to test
smf install test-skill

# Test it...
smf run test-skill

# Clean up when done
smf run skill-manager
# Select test-skill → r → confirm
```

### Disk Space Cleanup

```bash
# See what's taking space
smf run skill-manager --list

# Remove large unused skills
smf run skill-manager
# Select by size → backup → remove
```

### Migration Prep

```bash
# Backup everything before moving machines
smf run skill-manager
# a (select all) → b (backup)

# Backups saved to ~/.smf/backups/
```

## Troubleshooting

### "No skills installed"

Install some skills first:
```bash
smf install file-organizer
```

### Rich not available (fallback mode)

If `rich` isn't installed, Skill Manager falls back to a text-based interface:
```bash
pip install rich
```

### Can't remove skill

- Check you have permissions: `ls -la ~/.smf/skills/`
- Try with dry-run first: `smf run skill-manager --remove <skill> --dry-run`

## Data & Privacy

- **All local operations** — no data leaves your machine
- Backups stored locally in `~/.smf/backups/`
- No cloud services involved

## Support

- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Documentation:** https://smfworks.com/skills/skill-manager

---

*Powered by SMF Works | Free Skill | Local-First*
