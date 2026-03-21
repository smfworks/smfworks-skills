# Email Campaign Manager

Create, manage, and send personalized email campaigns. Supports HTML templates, mailing lists, and delivery tracking.

## Features

- ✅ **Campaign Creation** — Build email campaigns with templates
- ✅ **HTML Templates** — Newsletter and default styles included
- ✅ **Personalization** — Insert recipient data (name, company, etc.)
- ✅ **Mailing Lists** — Import from CSV with validation
- ✅ **Dry Run Mode** — Test before sending
- ✅ **SMTP Support** — Works with any email provider (Gmail, SendGrid, etc.)
- ✅ **Campaign Tracking** — Sent count, opens, clicks
- ✅ **Sample Data** — Test with built-in sample lists

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install email-campaign
```

## Quick Start

### 1. Create a Campaign

```bash
# Interactive mode
smf run email-campaign create
```

You'll be prompted for:
- Campaign name
- Email subject
- From email address
- Template style (default or newsletter)

### 2. Edit the Email Body

```bash
# Edit campaign HTML
smf run email-campaign edit --campaign your-campaign-id
```

This opens the HTML in your default editor (`$EDITOR` or nano).

### 3. Create a Mailing List

```bash
# Create sample list for testing
smf run email-campaign sample-list --output my-list.csv
```

Or create your own CSV:
```csv
email,first_name,last_name,company
john@example.com,John,Smith,Acme Corp
jane@example.com,Jane,Doe,Tech Inc
```

### 4. Test (Dry Run)

```bash
smf run email-campaign send --campaign your-campaign-id --list my-list.csv
```

This shows what would happen without sending emails.

### 5. Send the Campaign

```bash
# Configure SMTP first (see Setup section)
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password

# Send for real
smf run email-campaign send --campaign your-campaign-id --list my-list.csv --send
```

## Usage

### Creating Campaigns

**Interactive:**
```bash
smf run email-campaign create
```

**Command line:**
```bash
smf run email-campaign create \
  --name "March Newsletter" \
  --subject "March Updates from Our Team" \
  --from newsletter@yourcompany.com \
  --template newsletter
```

### Listing Campaigns

```bash
smf run email-campaign list
```

Output:
```
📧 3 Campaign(s)
--------------------------------------------------------------------------------
ID                                           Name                      Status
--------------------------------------------------------------------------------
march-newsletter-20260320-143052              March Newsletter          draft
february-update-20260215-091234             February Update           sent
welcome-series-20260110-154422              Welcome Series            draft
```

### Editing Campaign Content

```bash
smf run email-campaign edit --campaign march-newsletter-20260320-143052
```

This opens the HTML file in your editor. Edit the content, save, and close.

### Sending Campaigns

**Dry run (test):**
```bash
smf run email-campaign send --campaign your-campaign-id --list subscribers.csv
```

**Actually send:**
```bash
smf run email-campaign send --campaign your-campaign-id --list subscribers.csv --send
```

### Checking Statistics

```bash
smf run email-campaign stats --campaign your-campaign-id
```

Output:
```
📊 Campaign Statistics
========================================
Name: March Newsletter
Status: sent
Created: 2026-03-20
Sent: 2026-03-21

Sent: 150
Opens: 89
Clicks: 34
```

## Email Templates

### Default Template

Simple, clean HTML:
```html
<!DOCTYPE html>
<html>
<body style="font-family: Arial, sans-serif;">
    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
        <p>Hello {{FIRST_NAME}},</p>
        <p>Your email content here...</p>
        <p>Best regards,<br>{{FROM_NAME}}</p>
        <hr>
        <p style="font-size: 12px;">
            <a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a>
        </p>
    </div>
</body>
</html>
```

### Newsletter Template

Styled with header and footer:
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #2563eb; color: white; padding: 20px; }
        .content { padding: 20px; }
        .footer { background: #f3f4f6; padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{CAMPAIGN_NAME}}</h1>
        </div>
        <div class="content">
            <p>Hello {{FIRST_NAME}},</p>
            <p>Your newsletter content here...</p>
        </div>
        <div class="footer">
            <p><a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a></p>
        </div>
    </div>
</body>
</html>
```

## Personalization Variables

Use these placeholders in your email templates:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{FIRST_NAME}}` | Recipient's first name | John |
| `{{LAST_NAME}}` | Recipient's last name | Smith |
| `{{EMAIL}}` | Recipient's email | john@example.com |
| `{{CAMPAIGN_NAME}}` | Campaign name | March Newsletter |
| `{{FROM_NAME}}` | Sender name (from email) | newsletter |
| `{{UNSUBSCRIBE_URL}}` | Unsubscribe link | #unsubscribe... |
| `{{COMPANY}}` | Custom field from CSV | Acme Corp |

**Custom fields:** Any column in your CSV can be used:
- CSV column: `plan_type`
- Template: `{{PLAN_TYPE}}`

## SMTP Configuration

### Gmail

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password
```

**Note:** Use an App Password, not your regular password:
1. Go to Google Account settings
2. Security → 2-Step Verification → App passwords
3. Generate new app password for "Mail"

### SendGrid

```bash
export SMTP_HOST=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASS=your-sendgrid-api-key
```

### Mailgun

```bash
export SMTP_HOST=smtp.mailgun.org
export SMTP_PORT=587
export SMTP_USER=postmaster@your-domain.com
export SMTP_PASS=your-mailgun-password
```

### Other Providers

| Provider | Host | Port |
|----------|------|------|
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 587 |
| Zoho | smtp.zoho.com | 587 |

## Mailing List Format

### CSV Format

```csv
email,first_name,last_name,company,plan_type
john@example.com,John,Smith,Acme Corp,premium
jane@example.com,Jane,Doe,Tech Inc,basic
bob@example.com,Bob,Johnson,Startup LLC,premium
```

**Required column:** `email`

**Optional columns:** Any fields you want to personalize with

### Validation

Email Campaign Manager automatically:
- Removes duplicates
- Validates email format
- Lowercases all emails
- Skips empty rows

## Campaign Storage

Campaigns are stored in:
```
~/.smf/campaigns/
├── campaign-id-1/
│   ├── config.json       # Campaign settings
│   └── body.html         # Email template
├── campaign-id-2/
│   ├── config.json
│   └── body.html
└── ...
```

Logs are stored in:
```
~/.smf/logs/
├── campaign-id-1-send.log
└── ...
```

## Best Practices

### 1. Always Test First

```bash
# Dry run before sending
smf run email-campaign send --campaign my-campaign --list my-list.csv

# Review output
# Only add --send when ready
```

### 2. Use Double Opt-In

Only send to people who:
- Signed up for your list
- Confirmed their subscription
- Haven't unsubscribed

### 3. Include Unsubscribe Link

Always include in your template:
```html
<p><a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a></p>
```

### 4. Respect Rate Limits

Most providers limit sending:
- Gmail: ~100 emails/day (personal), ~2000/day (Workspace)
- SendGrid: Varies by plan
- Mailgun: Varies by plan

### 5. Monitor Bounces

Check your SMTP provider dashboard for:
- Bounced emails
- Spam complaints
- Delivery rates

## Automation

### Weekly Newsletter

Create `~/weekly-newsletter.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password

# Generate newsletter content
# (Your content generation logic here)

# Send campaign
smf run email-campaign send \
  --campaign weekly-newsletter \
  --list ~/subscribers.csv \
  --send
```

Make executable and add to cron:
```bash
chmod +x ~/weekly-newsletter.sh
crontab -e

# Every Monday at 9 AM
0 9 * * 1 ~/weekly-newsletter.sh
```

### Welcome Series

```bash
# Day 0: Welcome email
smf run email-campaign send --campaign welcome-day-0 --list new-subscribers.csv --send

# Day 1: Getting started
smf run email-campaign send --campaign welcome-day-1 --list new-subscribers.csv --send

# Day 7: Tips and tricks
smf run email-campaign send --campaign welcome-day-7 --list new-subscribers.csv --send
```

## Troubleshooting

### "SMTP configuration required"

**Problem:** Environment variables not set

**Solution:**
```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password
```

### "Authentication failed"

**Problem:** Wrong password or app password needed

**Solution:**
- Gmail: Use App Password (not regular password)
- Check 2FA is enabled for app passwords
- Verify SMTP settings with provider

### "No valid recipients found"

**Problem:** CSV format wrong or empty

**Solution:**
```bash
# Check CSV format
head my-list.csv

# Should show:
# email,first_name,last_name
# john@example.com,John,Smith
```

### Emails going to spam

**Tips:**
- Use authenticated domain (SPF, DKIM, DMARC)
- Don't use ALL CAPS
- Avoid spam trigger words
- Include unsubscribe link
- Test with spam checker tools

## Pricing

**Email Campaign Manager is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use dedicated email services (Mailchimp, SendGrid, etc.)

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
