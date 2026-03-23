# Text Formatter — Setup Guide

**Estimated setup time:** 3 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys, no external packages required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Already installed on macOS 12+ and most Linux distros | Free |
| smfworks-skills repository | Cloned via git | Free |
| A terminal | Any terminal application | Free |

Text Formatter has zero external dependencies — it uses only Python's standard library.

---

## Step 1 — Verify Python Is Installed

```bash
python3 --version
```

Expected output:
```
Python 3.11.4
```

Any version 3.8 or newer is fine.

---

## Step 2 — Get the Skills Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

Or update if you already have it:

```bash
cd ~/smfworks-skills && git pull
```

---

## Step 3 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/text-formatter
```

Confirm the files are present:

```bash
ls
```

Expected:
```
HOWTO.md   README.md   SETUP.md   main.py
```

---

## Step 4 — Verify the Skill Works

Run with no arguments:

```bash
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]
Commands: case, clean, count

Examples:
  python main.py case upper "hello world"
  python main.py case camel "hello world"
  python main.py clean < input.txt
  python main.py clean --aggressive < messy.txt
  python main.py count < document.txt
```

---

## Verify Your Setup

Run a quick test:

```bash
python3 main.py case upper "setup test"
```

Expected output:
```
SETUP TEST
```

If you see `SETUP TEST`, setup is complete.

---

## Configuration Options

No configuration needed. All options are passed as arguments at runtime.

---

## Troubleshooting

**`python3: command not found`** — Install Python from [python.org](https://python.org) or via your package manager.

**`No such file or directory: main.py`** — Run `cd ~/smfworks-skills/skills/text-formatter` first.

---

## Next Steps

Head to **HOWTO.md** for goal-based walkthroughs covering all three commands, pipe usage, and cron automation.

```bash
cat HOWTO.md
```
