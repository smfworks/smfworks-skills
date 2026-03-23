# OpenClaw Optimizer — Setup Guide

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
| OpenClaw workspace | `~/.openclaw/workspace/` must exist | — |

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
cd ~/smfworks-skills/skills/openclaw-optimizer
python3 main.py help
```

---

## Verify Your Setup

Run a quick audit:

```bash
python3 main.py audit
```

You should see a workspace analysis with size, file count, and recommendations. If you see `Error: SMF Works Pro subscription required`, complete Step 1 first.

---

## What the Optimizer Analyzes

The optimizer reads (never writes) these locations:

| Location | What it analyzes |
|----------|-----------------|
| `~/.openclaw/workspace/` | Workspace total size and breakdown |
| `~/.openclaw/workspace/MEMORY.md` | Long-term memory file size |
| `~/.openclaw/workspace/memory/` | Daily memory files count and age |
| `~/.smf/skills/` | Installed skills count and sizes |

---

## Understanding Warning Thresholds

| Item | Good | Warning | Critical |
|------|------|---------|----------|
| MEMORY.md | < 8 KB | 8–15 KB | > 15 KB |
| Daily memory files | < 30 | 30–60 | > 60 |
| Installed skills | < 10 | 10–20 | > 20 |
| Workspace total | < 2 MB | 2–5 MB | > 5 MB |

These thresholds represent the point where workspace bloat starts to noticeably impact agent performance.

---

## Schedule Monthly Audits

Add to crontab:

```bash
crontab -e
```

```bash
0 9 1 * * python3 /home/yourname/smfworks-skills/skills/openclaw-optimizer/main.py report >> /home/yourname/logs/optimizer.log 2>&1
```

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`Workspace not found`** — Verify `~/.openclaw/workspace/` exists: `ls ~/.openclaw/workspace/`

**Audit shows all green — nothing to optimize** — Your workspace is in good shape. Run again monthly to stay on top of it.

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on running audits, analyzing context bloat, applying recommendations, and scheduling automated checks.
