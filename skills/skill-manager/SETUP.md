# Skill Manager - Setup Guide

Quick setup guide for the Skill Manager.

---

## Prerequisites

- [ ] SMF CLI installed
- [ ] At least one skill installed (to manage)
- [ ] Python 3.7+

---

## Quick Start (2 minutes)

### Step 1: Install

```bash
smf install skill-manager
```

### Step 2: Launch

```bash
smf run skill-manager
```

That's it! No configuration needed.

---

## Optional: Install Rich for Better UI

For the best visual experience, install the `rich` library:

```bash
pip install rich
```

This gives you:
- Beautiful tables with colors
- Progress bars during backups
- Better formatting and spacing

Without `rich`, Skill Manager works fine but uses a simpler text interface.

---

## First Use

```bash
# Launch interactive manager
smf run skill-manager

# You'll see:
# - List of installed skills
# - Commands at bottom
# - Just type numbers to select, 'r' to remove, 'q' to quit
```

---

## Common Tasks

### See what's installed
```bash
smf run skill-manager --list
```

### Remove one skill
```bash
smf run skill-manager --remove coffee-briefing
```

### Backup before removing
```bash
smf run skill-manager
# Select skills → b (backup) → r (remove)
```

### Clean up test skills
```bash
smf run skill-manager
# 1. Select test skills by number
# 2. b (backup) - optional
# 3. r (remove)
# 4. Confirm
```

---

## Support

- **Issues:** https://github.com/smfworks/smfworks-skills/issues

---

**Ready to manage your skills! 🎛️**
