# Report Generator — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pandas | Python data analysis library | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

```bash
openclaw auth status
```

If not subscribed: [smfworks.com/subscribe](https://smfworks.com/subscribe)

---

## Step 2 — Install pandas

```bash
pip install pandas
```

---

## Step 3 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/report-generator
```

---

## Step 5 — Verify

```bash
python3 main.py help
```

Expected output shows all commands and examples.

---

## Verify Your Setup

Generate a sample report:

```bash
python3 main.py create --sample sales
```

Expected:
```
✅ Report generated: sales-report-2024-03-15.html
   Rows: 120
   Format: HTML
```

Open the HTML file in your browser to verify the report renders correctly.

---

## Configuration Options

No configuration file needed. All options are passed as command-line arguments.

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`pandas not installed`** — Run `pip install pandas`.

---

## Next Steps

Setup complete. See **HOWTO.md** for walkthroughs on creating reports from real data, available templates, and cron automation.
