# Email Campaign

> Send beautiful HTML email campaigns to your contacts from a CSV list

---

## What It Does

Email Campaign lets you send professional HTML email campaigns directly from your computer. Upload a CSV of contacts, write or paste an HTML template, and send personalized emails to your entire list — no monthly fees or email service subscriptions required.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Pro tier:**
```bash
smfw install email-campaign
smf login
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Send your first email campaign:

```bash
python main.py send --list contacts.csv --template newsletter.html
```

---

## Commands

### `send`

**What it does:** Send an HTML email campaign to all contacts in a CSV list.

**Usage:**
```bash
python main.py send --list [contacts.csv] --template [template.html]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--list` | ✅ Yes | CSV file with contacts | `contacts.csv` |
| `--template` | ✅ Yes | HTML email template | `template.html` |
| `--subject` | ❌ No | Email subject line | `"Monthly Newsletter"` |

**Example:**
```bash
python main.py send --list contacts.csv --template newsletter.html --subject "March Newsletter"
```

**Output:**
```
📧 Email Campaign Starting...
   Contacts: 150
   Template: newsletter.html
   Subject: March Newsletter

✅ Sent: 150 / 150 emails
   Failed: 0
```

---

### `preview`

**What it does:** Preview how your email template looks before sending.

**Usage:**
```bash
python main.py preview --template [template.html]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--template` | ✅ Yes | HTML email template | `template.html` |

**Example:**
```bash
python main.py preview --template newsletter.html
```

---

### `validate`

**What it does:** Check your contact list for issues before sending.

**Usage:**
```bash
python main.py validate --list [contacts.csv]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--list` | ✅ Yes | CSV file with contacts | `contacts.csv` |

**Example:**
```bash
python main.py validate --list contacts.csv
```

**Output:**
```
✅ Contact list valid!
   Total: 150 contacts
   Valid emails: 148
   Issues found: 2 (duplicates)
   Duplicate emails removed.
```

---

### `schedule`

**What it does:** Schedule an email campaign to send at a specific time.

**Usage:**
```bash
python main.py schedule --template [template.html] --list [contacts.csv] --time [datetime]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--template` | ✅ Yes | HTML email template | `template.html` |
| `--list` | ✅ Yes | CSV file with contacts | `contacts.csv` |
| `--time` | ✅ Yes | Send time (YYYY-MM-DD HH:MM) | `2026-03-25 10:00` |

**Example:**
```bash
python main.py schedule --template newsletter.html --list contacts.csv --time "2026-03-25 10:00"
```

---

### `stats`

**What it does:** Display statistics about sent campaigns.

**Usage:**
```bash
python main.py stats
```

**Example:**
```bash
python main.py stats
```

**Output:**
```
📊 Campaign Statistics:
   Total sent: 1,250
   Total failed: 12
   Campaigns sent: 8
   Last sent: 2026-03-20
```

---

## Use Cases

- **Newsletters:** Send monthly updates to subscribers
- **Announcements:** Announce product launches or company news
- **Event invitations:** Invite contacts to webinars or events
- **Promotions:** Send promotional offers to customers
- **Follow-ups:** Re-engage dormant customers

---

## Tips & Tricks

- Always preview before sending to catch formatting issues
- Use `--validate` to clean your list before large sends
- Keep HTML templates simple — complex layouts break in some email clients
- Use `{{name}}` placeholders in templates to personalize emails
- Schedule campaigns for optimal open times (Tuesday-Thursday mornings)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "SMTP connection failed" | Check your email provider's SMTP settings |
| "Template not found" | Verify the template file path is correct |
| "No valid contacts" | Ensure CSV has `email` column header |
| Emails going to spam | Use proper SPF/DKIM records for your domain |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- SMTP server access (Gmail, SendGrid, Mailgun, etc.)
- Valid HTML email template

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/email-campaign)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
