# Skill Manager — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to List Your Installed Skills](#1-how-to-list-your-installed-skills)
2. [How to Back Up a Skill](#2-how-to-back-up-a-skill)
3. [How to Remove a Skill You No Longer Need](#3-how-to-remove-a-skill-you-no-longer-need)
4. [How to Use the Interactive UI](#4-how-to-use-the-interactive-ui)
5. [How to Preview a Removal Before Doing It](#5-how-to-preview-a-removal-before-doing-it)
6. [Automating with Cron](#6-automating-with-cron)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)
8. [Tips & Best Practices](#8-tips--best-practices)

---

## 1. How to List Your Installed Skills

**What this does:** Prints a table of all installed skills with tier, size, and installation date.

**When to use it:** When you want to see what you have installed, how much space skills take up, or to verify a skill was installed or removed.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/skill-manager
```

**Step 2 — Run the list command.**

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

**Result:** A clear inventory of everything installed with tier and size at a glance.

---

## 2. How to Back Up a Skill

**What this does:** Copies a skill's directory to `~/.smf/backups/` before you modify or remove it.

**When to use it:** Before removing a skill you might want to restore later. Before customizing a skill's code. Before a major system change.

### Steps

**Step 1 — List skills to find the exact name.**

```bash
python3 main.py --list
```

**Step 2 — Back up the skill.**

```bash
python3 main.py --backup coffee-briefing
```

Output:
```
Backing up coffee-briefing...
✅ coffee-briefing backed up to ~/.smf/backups/
```

**Step 3 — Verify the backup exists.**

```bash
ls ~/.smf/backups/
```

You should see a directory or archive for `coffee-briefing`.

**Result:** The skill is backed up. You can safely modify or remove it knowing you can restore from the backup.

---

## 3. How to Remove a Skill You No Longer Need

**What this does:** Deletes a skill's directory from `~/.smf/skills/`.

**When to use it:** You've stopped using a skill and want to free up space. Or you want to do a clean reinstall.

### Steps

**Step 1 — Back up the skill first (recommended).**

```bash
python3 main.py --backup skill-name
```

**Step 2 — Preview what will be removed.**

```bash
python3 main.py --remove morning-commute --dry-run
```

Output:
```
[DRY RUN] Would remove: /home/user/.smf/skills/morning-commute
```

**Step 3 — Remove the skill.**

```bash
python3 main.py --remove morning-commute
```

Output:
```
Removing morning-commute...
✅ morning-commute removed successfully.
```

**Step 4 — Confirm it's gone.**

```bash
python3 main.py --list
```

`morning-commute` should no longer appear in the list.

**Result:** The skill is removed from your system.

---

## 4. How to Use the Interactive UI

**What this does:** Launches a full-screen terminal interface where you can browse skills, select multiple items, and perform bulk backup or removal.

**When to use it:** You want to remove or back up multiple skills at once, or you prefer a visual interface to command flags.

### Steps

**Step 1 — Launch the interactive UI.**

```bash
python3 main.py
```

**Step 2 — Read the skill list.**

The UI displays numbered skills with their details.

**Step 3 — Select skills.**

Type a number and press Enter to toggle a skill's selection. Type `a` to select all, `n` to deselect all.

```
Enter command: 1
```

(Selects skill #1)

**Step 4 — Perform an action.**

- Type `b` + Enter to **backup** all selected skills
- Type `r` + Enter to **remove** all selected skills
- Type `q` + Enter to **quit**

**Result:** Bulk operations on multiple skills through an easy interactive interface.

---

## 5. How to Preview a Removal Before Doing It

**What this does:** Shows exactly what `--remove` would do without actually making changes.

**When to use it:** Any time you want to confirm you're targeting the right skill before deleting anything.

### Steps

**Step 1 — Run with `--dry-run`.**

```bash
python3 main.py --remove skill-name --dry-run
```

Output:
```
[DRY RUN] Would remove: /home/user/.smf/skills/skill-name
```

**Step 2 — Review the path.** Confirm this is the right skill.

**Step 3 — If correct, run without `--dry-run`.**

```bash
python3 main.py --remove skill-name
```

**Result:** Zero-risk preview before any destructive action.

---

## 6. Automating with Cron

You can schedule a weekly skill inventory report.

### Example: Weekly skill list report every Monday at 9 AM

```bash
0 9 * * 1 python3 /home/yourname/smfworks-skills/skills/skill-manager/main.py --list >> /home/yourname/logs/skill-inventory.log 2>&1
```

### Create the log directory

```bash
mkdir -p ~/logs
```

---

## 7. Troubleshooting Common Issues

### `No skills installed.`

No skills were found in `~/.smf/skills/`.  
**Fix:** Install skills first. The manager is working correctly; there's nothing to manage yet.

---

### `❌ Backup failed.`

The backup operation encountered an error.  
**Fix:** Check the skill name exactly matches what's shown in `--list`. Verify `~/.smf/backups/` exists and is writable: `mkdir -p ~/.smf/backups`

---

### Interactive UI shows garbled output

Your terminal doesn't support the Unicode characters or terminal control codes used by the UI.  
**Fix:** Use the command-line flags instead: `--list`, `--remove`, `--backup`.

---

### `❌ [error message]` on remove

Removal failed.  
**Fix:** Check you have write permissions on `~/.smf/skills/`. Try `ls -la ~/.smf/skills/` to verify ownership.

---

## 8. Tips & Best Practices

**Always back up before removing.** Even if you're sure you don't need a skill, a backup takes 2 seconds and could save you 20 minutes of reinstallation later.

**Use `--dry-run` before any removal.** One extra command to confirm you're targeting the right thing. Habit-forming and protective.

**Back up pro skills before any system change.** Pro skills may have configurations and customizations that take time to recreate. A backup preserves everything.

**Use `--list` regularly to audit what you have installed.** Over time you may install skills for specific projects and forget they're there. A regular list check keeps things tidy.

**Install `rich` for a better experience.** `pip install rich` takes 10 seconds and makes the interactive UI and list much more readable. Highly recommended.
