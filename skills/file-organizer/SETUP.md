# File Organizer — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Already installed on most Macs and Linux systems | Free |
| OpenClaw | Installed on your machine | Free |
| smfworks-skills repository | Downloaded via git | Free |
| Write permissions | On the folders you want to organize | — |

No accounts to create. No API keys to obtain. No configuration files to edit.

---

## Step 1 — Verify Python Is Installed

Open a terminal and run:

```bash
python3 --version
```

You should see something like:
```
Python 3.11.4
```

Any version 3.8 or higher is fine. If you see `command not found`, install Python from [python.org](https://python.org) before continuing.

---

## Step 2 — Verify OpenClaw Is Installed

```bash
openclaw --version
```

You should see something like:
```
OpenClaw v1.2.0
```

If OpenClaw isn't installed, visit [smfworks.com](https://smfworks.com) for installation instructions.

---

## Step 3 — Get the Skills Repository

If you haven't already cloned the smfworks-skills repository:

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

Expected output:
```
Cloning into '/home/yourname/smfworks-skills'...
remote: Enumerating objects: 412, done.
remote: Counting objects: 100% (412/412), done.
Receiving objects: 100% (412/412), 384.22 KiB | 2.14 MiB/s, done.
```

If you already have the repository, update it:

```bash
cd ~/smfworks-skills
git pull
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/file-organizer
```

List the files to confirm everything is present:

```bash
ls
```

You should see:
```
HOWTO.md   README.md   SETUP.md   main.py
```

---

## Step 5 — Run the Skill for the First Time

This command runs the skill with no arguments, which prints the usage guide:

```bash
python3 main.py
```

You should see exactly this:
```
Usage: python main.py <command> [options]

Commands:
  organize-date <directory> [dest_directory]  - Organize by date
  organize-type <directory> [dest_directory]  - Organize by file type
  find-duplicates <directory>               - Find duplicate files

Examples:
  python main.py organize-date ~/Downloads
  python main.py organize-type ~/Documents ~/Organized
  python main.py find-duplicates ~/Pictures
```

If you see this output, setup is complete.

---

## Verify Your Setup

Run a real test on a folder you control. Create a test directory with a few files:

```bash
mkdir ~/test-organizer
touch ~/test-organizer/photo.jpg
touch ~/test-organizer/resume.pdf
touch ~/test-organizer/data.csv
touch ~/test-organizer/song.mp3
```

Now organize it by type:

```bash
python3 main.py organize-type ~/test-organizer
```

You should see:
```
✅ Organized 4 files by type

Organized into:
  Audio: 1 files
  Documents: 1 files
  Images: 1 files
  Spreadsheets: 1 files
```

Verify the result:
```bash
ls ~/test-organizer/
```

You should see:
```
Audio  Documents  Images  Spreadsheets
```

Setup is working correctly. Clean up the test:

```bash
rm -rf ~/test-organizer
```

---

## Configuration Options

File Organizer requires no configuration file. There are no environment variables to set and no config file to edit. All behavior is controlled entirely by the command and arguments you pass when running the skill.

The skill has the following built-in limits which are not configurable:

| Setting | Value |
|---------|-------|
| Maximum file size processed | 100 MB |
| Maximum duplicate name counter | 1,000 |
| Maximum directory scan depth | 10 levels |

---

## Troubleshooting Setup Issues

**`python3: command not found`**  
Python 3 is not installed or not on your PATH. Install it from [python.org](https://python.org) or use your system package manager (`sudo apt install python3` on Ubuntu/Debian, `brew install python3` on macOS).

**`No such file or directory: main.py`**  
You're not in the right directory. Make sure you ran `cd ~/smfworks-skills/skills/file-organizer` first.

**`Permission denied`**  
The folder you're trying to organize requires elevated permissions. Only organize folders you own (typically anything inside your home directory `~/`).

**`Cannot operate on system directory`**  
You pointed the skill at a system path like `/usr` or `/etc`. These are blocked for safety. Only use it on your own folders.

---

## Next Steps

Your setup is complete. Head to **HOWTO.md** for goal-based walkthroughs:

- How to clean up your Downloads folder
- How to organize a photo archive by date
- How to find and remove duplicate files
- How to automate organizing with cron

```bash
cat HOWTO.md
```
