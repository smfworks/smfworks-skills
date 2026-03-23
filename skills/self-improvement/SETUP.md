# Self Improvement — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

```bash
openclaw auth status
```

If not subscribed: [smfworks.com/subscribe](https://smfworks.com/subscribe)

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate and Verify

```bash
cd ~/smfworks-skills/skills/self-improvement
python3 main.py help
```

---

## Verify Your Setup

Log a test item:

```bash
python3 main.py log-learning "Test entry to verify setup" --tags test
```

Expected:
```
✅ Learning logged: LRN-YYYYMMDD-XXXXXX
   Category: best-practice
   Tags: test
```

Then list it:

```bash
python3 main.py list
```

Your test entry should appear.

---

## Storage Location

All logged items are stored at:
```
~/.smf/improvement/
├── errors/
├── learnings/
├── insights/
└── promoted.md
```

These directories are created automatically on first use.

---

## Category Reference

**Error categories:** `file-io`, `network`, `config`, `logic`, `syntax`, `runtime`

**Learning categories:** `best-practice`, `pattern`, `anti-pattern`, `optimization`, `architecture`

Specify with `--category CATEGORY` when logging. If omitted, defaults are used.

---

## Tag Guidelines

Tags make items searchable. Recommended conventions:
- Language/framework: `python`, `javascript`, `react`, `django`
- Domain: `database`, `api`, `frontend`, `config`, `security`
- Pattern type: `bug`, `performance`, `refactor`, `architecture`

Use consistent tags for better search results.

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`python3: command not found`** — Install Python 3.8+.

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on logging errors, capturing learnings, searching your knowledge base, and building agent memory.
