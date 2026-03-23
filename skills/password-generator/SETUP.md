# Password Generator — Setup Guide

**Estimated setup time:** 3 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys, no external packages required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| smfworks-skills repository | Cloned via git | Free |

Password Generator uses only Python's standard library (`secrets`, `string`, `math`). No pip installs needed.

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.8.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/password-generator
```

---

## Step 4 — Verify the Skill

```bash
python3 main.py
```

Expected:
```
Usage: python main.py <command> [options]
Commands:
  password [length]                  - Generate random password
  passphrase [word_count]            - Generate passphrase
  check <password>                  - Check password strength
```

---

## Verify Your Setup

Generate a test password:

```bash
python3 main.py password 16
```

Expected output (values will differ — that's the point):
```
Generated password: K7#mX2@pQ9vR!nLw
Strength: Strong ✅
Entropy: 104.8 bits
```

If you see a password with strength and entropy info, setup is complete.

---

## Configuration Options

No configuration file or environment variables needed. All behavior is controlled by command-line arguments.

---

## Troubleshooting

**`python3: command not found`** — Install Python from [python.org](https://python.org).

**`No such file or directory: main.py`** — Run `cd ~/smfworks-skills/skills/password-generator` first.

---

## Quick Reference

After setup, these are your three main commands:

```bash
# Generate a secure password (16 chars default)
python3 main.py password

# Generate a memorable passphrase
python3 main.py passphrase

# Check strength of an existing password
python3 main.py check "your-existing-password"
```

## Next Steps

See **HOWTO.md** for walkthroughs on all three commands, best practices for different use cases, and cron automation examples.
