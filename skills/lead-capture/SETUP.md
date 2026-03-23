# Lead Capture — Setup Guide

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
| smfworks-skills repository | Cloned via git | Included with Pro |

---

## Step 1 — Subscribe to SMF Works Pro

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe) and complete the subscription. Pro gives you access to all 14 Pro skills.

---

## Step 2 — Authenticate OpenClaw

Ensure your OpenClaw installation is authenticated with your Pro account:

```bash
openclaw auth status
```

Expected: Your email and `Pro` tier shown.

---

## Step 3 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/lead-capture
```

---

## Step 5 — Verify

```bash
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]

Commands:
  capture              - Capture a new lead (interactive)
  list [limit]         - List all leads
  export [csv|json]    - Export leads to file
  stats                - Show lead statistics
```

If you see `Error: SMF Works Pro subscription required`, complete Step 1–2.

---

## Verify Your Setup

Capture a test lead:

```bash
python3 main.py capture
```

Enter test details when prompted. Then verify it was saved:

```bash
python3 main.py list 1
```

You should see the test lead. Setup is complete.

---

## Configuration Options

No configuration file needed. Lead storage: `~/.smf/leads/leads.json` (auto-created on first capture).

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe) and re-authenticate OpenClaw.

**`python3: command not found`** — Install Python 3.8+ from [python.org](https://python.org).

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on capturing, listing, exporting, and automating lead management.

## Pro Subscription Benefits

With SMF Works Pro ($19.99/mo) you get access to all 14 Pro skills:
- Lead Capture (this skill)
- Coffee Briefing, Morning Commute
- OpenClaw Backup, Claw System Backup, Database Backup
- Report Generator, Email Campaign
- Task Manager, Self Improvement
- Invoice Generator, Form Builder, Booking Engine
- OpenClaw Optimizer
