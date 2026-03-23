# Lead Capture

> Capture, qualify, and manage sales leads with automatic scoring

---

## What It Does

Lead Capture helps you collect and organize potential customers. Add leads with contact info and notes, automatically score them based on engagement signals, and export prioritized lists for your sales team.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install lead-capture
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Capture your first lead:

```bash
python main.py capture --name "Jane Doe" --email "jane@company.com"
```

---

## Commands

### `capture`

**What it does:** Add a new lead to your database.

**Usage:**
```bash
python main.py capture [options]
```

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--name` | ✅ Yes | Contact name | `--name "Jane Doe"` |
| `--email` | ✅ Yes | Email address | `--email "jane@company.com"` |
| `--phone` | ❌ No | Phone number | `--phone "555-1234"` |
| `--company` | ❌ No | Company name | `--company "Acme Corp"` |
| `--source` | ❌ No | Where lead came from | `--source "Website"` |
| `--notes` | ❌ No | Additional notes | `--notes "Interested in enterprise plan"` |

**Example:**
```bash
python main.py capture --name "Jane Doe" --email "jane@company.com" --company "Acme"
python main.py capture --name "John Smith" --email "john@corp.com" --source "Trade show"
```

---

### `list`

**What it does:** Display all leads, sorted by score.

**Usage:**
```bash
python main.py list
```

**Example:**
```bash
python main.py list
```

**Output:**
```
👥 Your Leads (5):
------------------------------------------------------------
1. ⭐⭐⭐ Hot | Jane Doe | jane@company.com | Acme Corp
2. ⭐⭐ Warm  | John Smith | john@corp.com | —
3. ⭐ Cold  | Bob Wilson | bob@email.com | Wilson & Sons
```

---

### `export`

**What it does:** Export leads to CSV or JSON format.

**Usage:**
```bash
python main.py export [options]
```

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--format` | ❌ No | Export format: `csv` or `json` | `--format csv` |
| `--output` | ❌ No | Output file path | `--output leads.csv` |

**Example:**
```bash
python main.py export --format csv --output leads.csv
python main.py export --format json --output leads.json
```

---

### `search`

**What it does:** Search leads by keyword.

**Usage:**
```bash
python main.py search [keyword]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `keyword` | ✅ Yes | Search term | `consulting` |

**Example:**
```bash
python main.py search "enterprise"
python main.py search "referral"
```

---

### `score`

**What it does:** Score and prioritize leads.

**Usage:**
```bash
python main.py score
```

**Example:**
```bash
python main.py score
```

---

## Use Cases

- **Website forms:** Capture leads from contact forms
- **Trade shows:** Collect badges and add leads after events
- **Referrals:** Track who referred whom
- **Sales prioritization:** Focus on hottest leads first

---

## Tips & Tricks

- Add `--source` to track where leads come from
- Use `score` regularly to identify hot leads
- Export to CSV to import into other CRM tools
- Search by company name to find all contacts at one company

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Email already exists" | Lead already captured; use search to find it |
| "Invalid email format" | Check the email address format |
| Empty export | Ensure you have leads captured first |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/lead-capture)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
