# Lead Capture — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Capture a New Lead](#1-how-to-capture-a-new-lead)
2. [How to List and Review Your Leads](#2-how-to-list-and-review-your-leads)
3. [How to Export Leads for Your CRM](#3-how-to-export-leads-for-your-crm)
4. [How to View Lead Statistics](#4-how-to-view-lead-statistics)
5. [Automating with Cron](#5-automating-with-cron)
6. [Troubleshooting Common Issues](#6-troubleshooting-common-issues)
7. [Tips & Best Practices](#7-tips--best-practices)

---

## 1. How to Capture a New Lead

**What this does:** Runs an interactive form prompting for lead details and saves to local storage.

**When to use it:** Immediately after a sales call, demo, or networking event.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/lead-capture
```

**Step 2 — Run capture.**

```bash
python3 main.py capture
```

**Step 3 — Fill in the details.**

```
📋 New Lead Capture
────────────────────
Name: Jane Smith
Email: jane@acmecorp.com
Company: Acme Corp
Phone (optional): +1 555 0100
Interest/Notes: Interested in Pro plan, asked about API pricing

✅ Lead saved: Jane Smith (Acme Corp)
```

**Result:** Lead is saved to `~/.smf/leads/leads.json` immediately.

---

## 2. How to List and Review Your Leads

**When to use it:** Before a follow-up session to remind yourself who you need to contact.

### Steps

```bash
python3 main.py list 20
```

Output:
```
📋 Leads (20 most recent):

1. Jane Smith — jane@acmecorp.com — Acme Corp
   Captured: 2024-03-15 09:42
   Notes: Interested in Pro plan, asked about API pricing

2. Bob Jones — bob@techco.io — TechCo
   Captured: 2024-03-14 14:21
   Notes: Demo request, budget approved Q2
...
```

---

## 3. How to Export Leads for Your CRM

**When to use it:** Weekly, to import fresh leads into your CRM (HubSpot, Salesforce, etc.).

### Steps

**Step 1 — Export to CSV.**

```bash
python3 main.py export csv
```

Output:
```
✅ Exported 47 leads to leads-2024-03-15.csv
```

**Step 2 — Import into your CRM.**

Most CRMs have a "Import CSV" option. Upload the exported file. Column headers match standard CRM fields.

**Step 3 — Or export to JSON for custom processing.**

```bash
python3 main.py export json
```

---

## 4. How to View Lead Statistics

```bash
python3 main.py stats
```

Output:
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
```

---

## 5. Automating with Cron

### Example: Auto-export leads every Sunday

```bash
0 9 * * 0 python3 /home/yourname/smfworks-skills/skills/lead-capture/main.py export csv >> /home/yourname/logs/lead-capture.log 2>&1
```

---

## 6. Troubleshooting Common Issues

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe) and re-authenticate.

### `Error: Invalid email format`
**Fix:** Enter a valid email with `@` and domain.

---

## 7. Tips & Best Practices

**Capture leads immediately** — don't wait until end of day. Details are freshest right after the conversation.

**Use the Notes field liberally** — capture context: budget, timeline, decision-makers, objections. This makes follow-ups far more effective.

**Export weekly** — build a habit of exporting every Monday morning and importing to your CRM. Never let more than a week of leads pile up un-synced.

**Review your stats monthly** — the `stats` command reveals your lead generation trends. If this week's count is down, investigate what changed.

**Back up your leads file periodically.** Your leads are stored at `~/.smf/leads/leads.json`. Copy it to a safe location regularly:

```bash
cp ~/.smf/leads/leads.json ~/Backups/leads-backup-$(date +%Y-%m-%d).json
```

---

## Combining with Other Skills

**Lead Capture + CSV Converter:** Export leads as JSON, then convert to Excel for your team:

```bash
python3 ~/smfworks-skills/skills/lead-capture/main.py export json
python3 ~/smfworks-skills/skills/csv-converter/main.py json-to-csv leads-$(date +%Y-%m-%d).json leads.csv
python3 ~/smfworks-skills/skills/csv-converter/main.py csv-to-excel leads.csv leads-report.xlsx
```

**Lead Capture + Report Generator:** Generate a monthly leads report:

```bash
python3 ~/smfworks-skills/skills/lead-capture/main.py export csv
python3 ~/smfworks-skills/skills/report-generator/main.py create --data leads-$(date +%Y-%m-%d).csv --title "Monthly Leads"
```

---

## Understanding the Data

Leads are stored in `~/.smf/leads/leads.json` as a JSON array. Each lead looks like:

```json
{
  "id": "LEAD-20240315-a1b2c3",
  "name": "Jane Smith",
  "email": "jane@acmecorp.com",
  "company": "Acme Corp",
  "phone": "+1 555 0100",
  "notes": "Interested in Pro plan",
  "captured_at": "2024-03-15T09:42:11"
}
```

You can view or edit this file directly in any text editor if you need to:
- Correct a typo in a lead
- Add leads from another source
- Delete a duplicate
- Add custom fields

```bash
# View the raw data
cat ~/.smf/leads/leads.json | python3 -m json.tool | head -30
```

