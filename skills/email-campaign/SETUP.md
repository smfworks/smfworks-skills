# Email Campaign Manager - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and sending email campaigns.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [SMTP Configuration](#smtp-configuration)
5. [Creating Your First Campaign](#creating-your-first-campaign)
6. [Managing Mailing Lists](#managing-mailing-lists)
7. [Sending Campaigns](#sending-campaigns)
8. [Automation](#automation)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **SMTP Provider:** Gmail, SendGrid, Mailgun, or any SMTP server
- **Domain:** (Optional but recommended) Custom domain with SPF/DKIM

### Required Accounts

**SMTP Provider Account:**
- Gmail (Google Account)
- SendGrid account
- Mailgun account
- Or your own SMTP server

**SMF Works Subscription:**
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

### Required Python Packages
```bash
# No additional packages required
# Uses only Python standard library (smtplib)
```

---

## Installation

### Step 1: Install SMF CLI

```bash
# One-liner install
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Reload PATH
source ~/.bashrc  # or ~/.zshrc
```

### Step 2: Authenticate

```bash
# Login with your subscription
smf login

# Verify
smf status
```

Expected output:
```
🔐 SMF Works Status
----------------------------------------
✅ Subscription active
   Tier: pro
   Expires: 2027-03-20
```

### Step 3: Install Email Campaign Manager

```bash
smf install email-campaign
```

### Step 4: Verify Installation

```bash
smf run email-campaign --help
```

Expected output:
```
📧 Email Campaign Manager

Create and send email campaigns with personalization.

Commands:
  create                    Create new campaign (interactive)
  list                      List all campaigns
  edit --campaign ID        Edit campaign body
  send --campaign ID        Send campaign (dry run)
  stats --campaign ID       Show campaign statistics
```

---

## Authentication Setup

### Subscribe to SMF Works Pro

1. Visit https://smf.works/subscribe
2. Choose "Pro" plan ($19.99/mo)
3. Complete checkout via Stripe
4. Get your API token from the dashboard

### Authenticate CLI

```bash
smf login

# Paste your token when prompted
# Token saved to ~/.smf/token
```

### Verify Authentication

```bash
smf status
```

---

## SMTP Configuration

### Option 1: Gmail (Recommended for Testing)

**Create App Password:**

1. Go to https://myaccount.google.com/
2. Security → 2-Step Verification → Turn on
3. Security → App passwords
4. Select "Mail" and your device
5. Generate password (16 characters)

**Set Environment Variables:**

```bash
# Add to your shell profile (~/.bashrc or ~/.zshrc)
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=xxxx-xxxx-xxxx-xxxx  # Your app password
```

**Reload shell:**
```bash
source ~/.bashrc  # or ~/.zshrc
```

**Test:**
```bash
echo $SMTP_HOST
# Should output: smtp.gmail.com
```

### Option 2: SendGrid (Production Recommended)

**Create Account:**
1. Sign up at https://sendgrid.com/
2. Complete verification
3. Create API key (Settings → API Keys)

**Set Environment Variables:**

```bash
export SMTP_HOST=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASS=SG.xxxxxx  # Your SendGrid API key
```

**Verify domain** (recommended):
1. Go to Settings → Sender Authentication
2. Authenticate your domain
3. Add DNS records as instructed

### Option 3: Mailgun

**Create Account:**
1. Sign up at https://www.mailgun.com/
2. Add your domain
3. Verify domain with DNS records

**Set Environment Variables:**

```bash
export SMTP_HOST=smtp.mailgun.org
export SMTP_PORT=587
export SMTP_USER=postmaster@your-domain.com
export SMTP_PASS=your-mailgun-password
```

### Option 4: Other Providers

**Outlook/Office 365:**
```bash
export SMTP_HOST=smtp.office365.com
export SMTP_PORT=587
export SMTP_USER=your-email@company.com
export SMTP_PASS=your-password
```

**Yahoo:**
```bash
export SMTP_HOST=smtp.mail.yahoo.com
export SMTP_PORT=587
export SMTP_USER=your-email@yahoo.com
export SMTP_PASS=your-app-password
```

**Custom SMTP Server:**
```bash
export SMTP_HOST=your-smtp-server.com
export SMTP_PORT=587  # or 465 for SSL
export SMTP_USER=username
export SMTP_PASS=password
```

### Verify SMTP Configuration

```bash
# Test connection
python3 -c "
import smtplib
import os

server = smtplib.SMTP(os.environ['SMTP_HOST'], os.environ['SMTP_PORT'])
server.starttls()
server.login(os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
print('✅ SMTP connection successful')
server.quit()
"
```

---

## Creating Your First Campaign

### Step 1: Create Campaign

```bash
smf run email-campaign create
```

**Interactive prompts:**
```
📧 Email Campaign Manager
========================================

Campaign name: March Newsletter
Email subject: March Updates from Our Team
From email: newsletter@yourcompany.com

Template:
  1. Default (simple)
  2. Newsletter (styled)

Choice [1]: 2

✅ Campaign created: march-newsletter-20260320-143052
   Edit body: smf run email-campaign edit --campaign march-newsletter-20260320-143052
```

**Note the campaign ID** — you'll need it for next steps.

### Step 2: Edit Email Content

```bash
smf run email-campaign edit --campaign march-newsletter-20260320-143052
```

This opens the HTML in your default editor.

**Edit the template:**
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .container { max-width: 600px; margin: 0 auto; }
        .header { background: #2563eb; color: white; padding: 20px; }
        .content { padding: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>March Newsletter</h1>
        </div>
        <div class="content">
            <p>Hello {{FIRST_NAME}},</p>
            
            <p>Welcome to our March newsletter! Here are the latest updates...</p>
            
            <p>Best regards,<br>The Team</p>
        </div>
    </div>
</body>
</html>
```

**Save and exit** the editor.

### Step 3: Create Mailing List

**Create sample list:**
```bash
smf run email-campaign sample-list --output test-list.csv
```

Or create your own:
```bash
cat > my-list.csv << 'EOF'
email,first_name,last_name,company
john@example.com,John,Smith,Acme Corp
jane@example.com,Jane,Doe,Tech Inc
bob@example.com,Bob,Johnson,Startup LLC
EOF
```

### Step 4: Test (Dry Run)

```bash
smf run email-campaign send \
  --campaign march-newsletter-20260320-143052 \
  --list test-list.csv
```

**Review output:**
```
📧 Sending Campaign: March Newsletter
   Recipients: 3
   Subject: March Updates from Our Team
   From: newsletter@yourcompany.com

🔧 DRY RUN MODE - No emails sent
   Would send to: 3 recipients

   First 3 recipients:
     1. john@example.com
     2. jane@example.com
     3. bob@example.com

✅ Dry run complete. To actually send, use --send
```

### Step 5: Send for Real

```bash
smf run email-campaign send \
  --campaign march-newsletter-20260320-143052 \
  --list test-list.csv \
  --send
```

**Output:**
```
📧 Sending Campaign: March Newsletter
   Recipients: 3
   Subject: March Updates from Our Team
   From: newsletter@yourcompany.com

🚀 Sending emails...
  ✅ 1/3: john@example.com
  ✅ 2/3: jane@example.com
  ✅ 3/3: bob@example.com

✅ Campaign sent!
   Sent: 3
   Failed: 0
```

---

## Managing Mailing Lists

### CSV Format

**Required column:** `email`

**Optional columns:** Any fields you want to use

**Example:**
```csv
email,first_name,last_name,company,plan_type,city
john@example.com,John,Smith,Acme Corp,premium,New York
jane@example.com,Jane,Doe,Tech Inc,basic,San Francisco
bob@example.com,Bob,Johnson,Startup LLC,premium,Austin
```

### Creating Lists from Other Sources

**From Google Contacts:**
1. Go to https://contacts.google.com/
2. Export → CSV (Google format)
3. Clean up columns to match required format

**From Mailchimp:**
1. Audience → Export audience
2. Download CSV
3. Rename columns: `Email Address` → `email`, `First Name` → `first_name`

**From Database:**
```bash
# PostgreSQL
psql -d mydb -c "
  COPY (
    SELECT email, first_name, last_name, company
    FROM subscribers
    WHERE subscribed = true
  ) TO STDOUT WITH CSV HEADER
" > mailing-list.csv
```

### Validating Email Lists

Email Campaign Manager automatically:
- ✅ Validates email format
- ✅ Removes duplicates
- ✅ Lowercases all emails
- ✅ Skips empty rows

**Manual validation:**
```bash
# Check for common issues
cat mailing-list.csv | grep -E '^[^@]+@[^@]+\.[^@]+$'

# Count valid emails
cat mailing-list.csv | grep -c '@'
```

### Segmentation

Create targeted lists:

**Premium customers only:**
```bash
# CSV has 'plan_type' column
grep "premium" mailing-list.csv > premium-customers.csv
```

**By location:**
```bash
# CSV has 'city' column
grep "New York" mailing-list.csv > ny-customers.csv
```

---

## Sending Campaigns

### Before You Send

**Checklist:**
- [ ] Campaign content edited and saved
- [ ] Subject line set
- [ ] From email configured
- [ ] Mailing list validated
- [ ] Dry run completed successfully
- [ ] SMTP environment variables set
- [ ] Recipient count looks correct

### Sending Process

**1. Test to yourself:**
```bash
# Create test list with just your email
echo "email,your_email@example.com,your,name" > test.csv

# Send test
smf run email-campaign send --campaign my-campaign --list test.csv --send
```

**2. Check received email:**
- Formatting looks good?
- Images load?
- Links work?
- Personalization correct?

**3. Send to full list:**
```bash
smf run email-campaign send \
  --campaign my-campaign \
  --list full-mailing-list.csv \
  --send
```

**4. Monitor statistics:**
```bash
smf run email-campaign stats --campaign my-campaign
```

### Rate Limiting

Most providers have limits:

| Provider | Limit | Notes |
|----------|-------|-------|
| Gmail | 100/day (personal) | For testing only |
| Gmail Workspace | 2000/day | Business accounts |
| SendGrid | Varies | Check your plan |
| Mailgun | Varies | Check your plan |

**For large lists, consider:**
- Batch sending (pause between batches)
- Dedicated email service
- SMTP provider with higher limits

---

## Automation

### Weekly Newsletter Script

Create `~/newsletter.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

# SMTP credentials
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-app-password

# Generate weekly content
# (Your content generation here)

# Send newsletter
smf run email-campaign send \
  --campaign weekly-newsletter \
  --list ~/subscribers.csv \
  --send

# Log result
echo "Newsletter sent: $(date)" >> ~/newsletter.log
```

Make executable:
```bash
chmod +x ~/newsletter.sh
```

Add to cron:
```bash
crontab -e

# Every Monday at 9 AM
0 9 * * 1 ~/newsletter.sh
```

### Welcome Series Automation

**Day 0 - Welcome:**
```bash
#!/bin/bash
# welcome-day-0.sh

export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=newsletter@company.com
export SMTP_PASS=xxxxx

smf run email-campaign send \
  --campaign welcome-day-0 \
  --list new-subscribers-today.csv \
  --send
```

**Day 1 - Getting Started:**
```bash
#!/bin/bash
# welcome-day-1.sh

export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=newsletter@company.com
export SMTP_PASS=xxxxx

# Get subscribers from yesterday
psql -d mydb -c "
  COPY (
    SELECT email, first_name
    FROM subscribers
    WHERE created_at >= NOW() - INTERVAL '1 day'
    AND created_at < NOW() - INTERVAL '0 day'
  ) TO STDOUT WITH CSV HEADER
" > day-1-subscribers.csv

smf run email-campaign send \
  --campaign welcome-day-1 \
  --list day-1-subscribers.csv \
  --send
```

Add to cron (run daily):
```bash
# Day 0 - immediately (run manually or via webhook)
# Day 1 - at 10 AM next day
0 10 * * * ~/welcome-day-1.sh
```

---

## Troubleshooting

### "SMTP configuration required"

**Problem:** Environment variables not set

**Solution:**
```bash
# Check if set
echo $SMTP_HOST

# Set them
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-password

# Make permanent (add to ~/.bashrc)
```

### "Authentication failed"

**Problem:** Wrong credentials

**Solutions:**

**Gmail:**
- Use App Password (not regular password)
- Enable 2-Step Verification first
- Generate at https://myaccount.google.com/apppasswords

**SendGrid:**
- Use "apikey" as username
- Use API key (starts with SG.xxxxx) as password
- Not your SendGrid login password

**Mailgun:**
- Use postmaster@your-domain.com as user
- Use Mailgun SMTP password
- Not your Mailgun login

### "No valid recipients found"

**Problem:** CSV format incorrect

**Solution:**
```bash
# Check CSV
head mailing-list.csv

# Should have header row:
# email,first_name,last_name
# john@example.com,John,Smith

# Check encoding
file mailing-list.csv

# Fix encoding if needed
iconv -f ISO-8859-1 -t UTF-8 mailing-list.csv > fixed.csv
```

### Emails not sending

**Check:**
1. SMTP credentials correct?
2. Internet connection?
3. Firewall blocking port 587?
4. Rate limit reached?

**Test SMTP:**
```bash
python3 -c "
import smtplib
import os

s = smtplib.SMTP(os.environ['SMTP_HOST'], os.environ['SMTP_PORT'])
s.starttls()
s.login(os.environ['SMTP_USER'], os.environ['SMTP_PASS'])
print('Login successful')
s.quit()
"
```

### Emails going to spam

**Improvements:**
1. **Authenticate your domain** (SPF, DKIM, DMARC)
2. **Use consistent from address**
3. **Include unsubscribe link**
4. **Don't use spammy words** (FREE, ACT NOW, etc.)
5. **Test with spam checker:** https://www.mail-tester.com/

### Campaign not found

**Problem:** Wrong campaign ID

**Solution:**
```bash
# List campaigns to get correct ID
smf run email-campaign list

# Use full ID from list
smf run email-campaign edit --campaign full-campaign-id-here
```

---

## Best Practices

### 1. Always Test First

```bash
# Test to yourself first
echo "email,you@example.com" > test.csv
smf run email-campaign send --campaign my-campaign --list test.csv --send

# Check email, then send to full list
smf run email-campaign send --campaign my-campaign --list full-list.csv --send
```

### 2. Get Permission (Opt-In)

Only email people who:
- Explicitly subscribed
- Can unsubscribe easily
- Haven't unsubscribed

**Legal compliance:**
- CAN-SPAM (US)
- GDPR (EU)
- CASL (Canada)

### 3. Include Unsubscribe

Always include in email template:
```html
<p style="font-size: 12px;">
  <a href="{{UNSUBSCRIBE_URL}}">Unsubscribe</a> |
  <a href="https://yourcompany.com/privacy">Privacy Policy</a>
</p>
```

### 4. Respect Rate Limits

**Don't:**
- Send thousands in one batch (unless using bulk service)
- Send too frequently
- Spam unengaged users

**Do:**
- Space out large campaigns
- Segment and target
- Clean inactive subscribers

### 5. Monitor Metrics

Track:
- Delivery rate
- Open rate
- Click rate
- Unsubscribe rate
- Bounce rate

**Good benchmarks:**
- Open rate: 20-30%
- Click rate: 2-5%
- Unsubscribe: < 1%

### 6. Backup Your Lists

```bash
# Regular backup
cp ~/mailing-list.csv ~/backups/mailing-list-$(date +%Y%m%d).csv

# Add to cron
0 2 * * * cp ~/mailing-list.csv ~/backups/mailing-list-$(date +\%Y\%m\%d).csv
```

---

## Next Steps

1. **Set up SMTP** — Configure Gmail or SendGrid
2. **Create first campaign** — Test with sample list
3. **Build mailing list** — Import your contacts
4. **Send test email** — Verify everything works
5. **Schedule automation** — Weekly newsletter

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
