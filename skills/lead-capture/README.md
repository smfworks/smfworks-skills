# Lead Capture

> Capture, store, and export sales leads from the terminal — with stats, CSV/JSON export, and a simple interactive intake form.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Sales / CRM

---

## What It Does

Lead Capture is an OpenClaw Pro skill for collecting and managing sales leads directly from your terminal. Run an interactive intake to capture lead details (name, email, company, phone, interest), list all stored leads, export to CSV or JSON, and view statistics on your lead pipeline.

Leads are stored locally in `~/.smf/leads/leads.json`. No cloud sync, no external CRM — just fast, local lead storage you own.

**What it does NOT do:** It does not sync to a CRM, send automated follow-up emails, score leads, or integrate with web forms.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/lead-capture
python3 main.py
```

Expected output (if Pro subscription is active):
```
Usage: python main.py <command> [options]

Commands:
  capture              - Capture a new lead (interactive)
  list [limit]         - List all leads
  export [csv|json]    - Export leads to file
  stats                - Show lead statistics
```

---

## Quick Start

Capture your first lead:

```bash
python3 main.py capture
```

The skill will prompt for:
- Name
- Email
- Company
- Phone (optional)
- Interest / notes

Then run:
```bash
python3 main.py list
```

---

## Command Reference

### `capture`

Interactive lead intake. Prompts for lead details and saves to local storage.

**Usage:**
```bash
python3 main.py capture
```

**Interactive session:**
```
📋 New Lead Capture
────────────────────
Name: Jane Smith
Email: jane@acmecorp.com
Company: Acme Corp
Phone (optional): +1 555 0100
Interest/Notes: Interested in Pro plan, asked about API access

✅ Lead saved: Jane Smith (Acme Corp)
```

---

### `list`

Shows stored leads, most recent first. Optional limit argument controls how many to show.

**Usage:**
```bash
python3 main.py list [limit]
```

**Example:**
```bash
python3 main.py list 10
```

**Output:**
```
📋 Leads (10 most recent):

1. Jane Smith — jane@acmecorp.com — Acme Corp
   Captured: 2024-03-15 09:42
   Notes: Interested in Pro plan, asked about API access

2. Bob Jones — bob@techco.io — TechCo
   Captured: 2024-03-14 14:21
   Notes: Demo request, budget approved

...
```

---

### `export`

Exports all leads to a file. Supports CSV and JSON formats.

**Usage:**
```bash
python3 main.py export [csv|json]
```

**Example — CSV:**
```bash
python3 main.py export csv
```

**Output:**
```
✅ Exported 47 leads to leads-2024-03-15.csv
```

**Example — JSON:**
```bash
python3 main.py export json
```

**Output:**
```
✅ Exported 47 leads to leads-2024-03-15.json
```

---

### `stats`

Shows pipeline statistics: total leads, recent activity, and capture rate.

**Usage:**
```bash
python3 main.py stats
```

**Output:**
```
📊 Lead Statistics
────────────────────
Total leads: 47
This week: 8
This month: 23
Avg per day (30d): 0.8

Top companies:
  Acme Corp: 3 leads
  TechCo: 2 leads
  InnovateLtd: 2 leads
```

---

## Use Cases

### 1. Capture a lead immediately after a sales call

```bash
python3 main.py capture
```

---

### 2. Export leads weekly for your CRM import

```bash
python3 main.py export csv
# Import the CSV into your CRM manually
```

---

### 3. Track weekly lead volume

```bash
python3 main.py stats
```

---

### 4. Review leads before a follow-up session

```bash
python3 main.py list 20
```

---

## Configuration

No configuration file needed. Leads stored at: `~/.smf/leads/leads.json`

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe). Ensure OpenClaw is authenticated.

### `No leads found`
No leads captured yet.  
**Fix:** Run `capture` to add your first lead.

### `Error: Invalid email format`
The email address entered during capture doesn't pass validation.  
**Fix:** Enter a valid email address (must contain `@` and a domain).

### Export file already exists
**Fix:** The export creates a date-stamped file. If you've already exported today, a new timestamped version is created.

---

## FAQ

**Q: Where are leads stored?**  
A: Locally at `~/.smf/leads/leads.json`. Nothing is sent to any cloud service.

**Q: Can I import leads from an existing CSV?**  
A: Not via CLI command. You can manually edit the JSON file to import existing leads.

**Q: Does it check for duplicate emails?**  
A: The skill accepts all entries. Check for duplicates in your exported CSV.

**Q: Can I delete a lead?**  
A: Edit `~/.smf/leads/leads.json` directly in a text editor to remove entries.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| OpenClaw | Authenticated |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/lead-capture)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
