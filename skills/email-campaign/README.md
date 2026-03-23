# Email Campaign

> Create and send personalized email campaigns from the terminal — with rate limiting, unsubscribe compliance, dry-run preview, and campaign statistics.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Requires:** SMTP credentials (Gmail, SendGrid, Mailgun, or any SMTP server)  
**Version:** 1.0  
**Category:** Marketing / Communications

---

## What It Does

Email Campaign is an OpenClaw Pro skill for sending personalized email campaigns via any SMTP server. Create a campaign, load a subscriber CSV, preview the send with a dry run, then actually send. Built-in rate limiting delays each send to avoid triggering spam filters, and every email automatically includes an unsubscribe link for legal compliance.

**What it does NOT do:** It does not provide email tracking (open rates, click rates), manage bounces automatically, or provide a visual template editor.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **SMTP credentials** — see SETUP.md

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/email-campaign
# Configure SMTP credentials (see SETUP.md)
python3 main.py help
```

---

## Quick Start

```bash
# Create a campaign
python3 main.py create --name "March Newsletter"

# Preview send (dry run)
python3 main.py send --campaign march-newsletter-20240315 --list subscribers.csv

# Actually send
python3 main.py send --campaign march-newsletter-20240315 --list subscribers.csv --send
```

---

## Command Reference

### `create`

Creates a new email campaign. Can be interactive or use flags for name, subject, and template.

**Usage:**
```bash
python3 main.py create                             # Interactive mode
python3 main.py create --name "Campaign Name"     # With name
python3 main.py create --name NAME --subject "Subject" --from email@domain.com
```

**Interactive session:**
```
Campaign name: March Newsletter
Subject line: Your March Update from Acme
From email: hello@acme.com
Template (default/newsletter): newsletter

✅ Campaign created: march-newsletter-20240315
   Edit your campaign body at: ~/.smf/campaigns/march-newsletter-20240315/body.txt
```

---

### `list`

Lists all campaigns with status and creation date.

```bash
python3 main.py list
```

Output:
```
📧 Email Campaigns (3 total):

1. march-newsletter-20240315 — Draft — 2024-03-15
2. promo-spring-20240310 — Sent (247 recipients) — 2024-03-10
3. welcome-series-20240301 — Sent (89 recipients) — 2024-03-01
```

---

### `edit --campaign ID`

Opens the campaign body for editing.

```bash
python3 main.py edit --campaign march-newsletter-20240315
```

This opens the body file in your default text editor, or you can edit it directly:
```bash
nano ~/.smf/campaigns/march-newsletter-20240315/body.txt
```

---

### `send --campaign ID --list FILE [--send]`

Sends a campaign to a subscriber list. Without `--send`, performs a dry run showing what would be sent. With `--send`, actually delivers emails.

**Usage:**
```bash
python3 main.py send --campaign ID --list subscribers.csv           # Dry run
python3 main.py send --campaign ID --list subscribers.csv --send    # Real send
```

**Subscriber CSV format:**
```csv
email,name,company
alice@example.com,Alice,Acme Corp
bob@example.com,Bob,TechCo
```

**Dry run output:**
```
📧 Campaign: March Newsletter
   Subject: Your March Update from Acme
   Recipients: 247
   From: hello@acme.com

[DRY RUN] Would send to:
  1. alice@example.com (Alice, Acme Corp)
  2. bob@example.com (Bob, TechCo)
  ...

Rate limiting: 1.5s between emails
Estimated send time: 6 min 10 sec
```

**Real send output:**
```
📧 Sending campaign: March Newsletter
   Recipients: 247

   Sending 1/247: alice@example.com... ✅
   Sending 2/247: bob@example.com... ✅
   ...

✅ Campaign sent!
   Sent: 247
   Errors: 0
   Time: 6m 18s
```

---

### `stats --campaign ID`

Shows statistics for a sent campaign.

```bash
python3 main.py stats --campaign march-newsletter-20240315
```

Output:
```
📊 Campaign Statistics: March Newsletter

Sent: 247
Errors: 3
Success rate: 98.8%
Send time: 6m 18s
```

---

### `sample-list`

Creates a sample subscriber CSV for testing.

```bash
python3 main.py sample-list --output test-list.csv
```

---

## Use Cases

### 1. Monthly newsletter to subscribers

Create, edit, and send a monthly newsletter.

### 2. Promotional campaign with dry run preview

Always dry run first to verify recipients and timing before the real send.

### 3. Automated welcome email series

Schedule campaigns via cron after new subscribers are added.

---

## Configuration — SMTP Credentials

Set these environment variables before running any send command:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password
```

**Gmail App Password:** Gmail requires an "App Password" (not your regular Gmail password) when 2FA is enabled. Generate at: myaccount.google.com/apppasswords.

**SendGrid:** `SMTP_HOST=smtp.sendgrid.net`, `SMTP_PORT=587`, `SMTP_USER=apikey`, `SMTP_PASS=your-sendgrid-api-key`

Add to `~/.bashrc` or `~/.zshrc` to persist:
```bash
echo 'export SMTP_HOST=smtp.gmail.com' >> ~/.bashrc
echo 'export SMTP_USER=your@gmail.com' >> ~/.bashrc
# Note: storing passwords in .bashrc is acceptable for personal use
```

---

## Rate Limiting

The skill automatically adds a delay between each email to avoid triggering spam filters. Large lists are sent in batches with pauses.

| List size | Behavior |
|-----------|---------|
| Small (<50) | 1–2 seconds between emails |
| Medium (50–200) | Batch pauses added |
| Large (200+) | Extended batch pauses |

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `SMTP Authentication Failed`
**Fix:** Verify `SMTP_USER` and `SMTP_PASS`. For Gmail, use an App Password, not your regular password.

### `Connection refused to smtp.gmail.com:587`
**Fix:** Port 587 with STARTTLS is the standard. Some networks block it — try port 465 (SSL) or check your firewall.

### High error rate during send
**Fix:** Some email addresses are invalid or the recipient server is rejecting. The errors are logged. Check `stats` after sending.

### Emails going to spam
**Fix:** Ensure you have a valid From address, your domain has SPF/DKIM records, and you're using a reputable SMTP provider.

---

## FAQ

**Q: Does it track open rates?**  
A: No. The skill doesn't inject tracking pixels or link redirects. For tracking, use a dedicated ESP like Mailchimp or SendGrid's tracking features.

**Q: Are unsubscribe links included automatically?**  
A: Yes — all emails automatically include an unsubscribe notice for legal compliance (CAN-SPAM, GDPR).

**Q: Can I personalize the email with recipient name?**  
A: Yes — use `{{name}}` and `{{company}}` placeholders in your campaign body. They're replaced with values from the subscriber CSV.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| SMTP server | Required (Gmail, SendGrid, etc.) |
| External APIs | None (direct SMTP) |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/email-campaign)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
