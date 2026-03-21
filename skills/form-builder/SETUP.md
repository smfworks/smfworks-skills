# Form Builder - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Form Builder skill.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Creating Forms](#creating-forms)
5. [Serving Forms](#serving-forms)
6. [Managing Responses](#managing-responses)
7. [Automation](#automation)
8. [Troubleshooting](#troubleshooting)
9. [Best Practices](#best-practices)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Network:** Local network access for serving forms
- **Browser:** Any modern web browser for viewing forms

### SMF Works Subscription
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

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

### Step 3: Install Form Builder

```bash
smf install form-builder
```

### Step 4: Verify Installation

```bash
smf run form-builder --help
```

Expected output:
```
📝 Form Builder

Create forms, collect responses, and export data.

Commands:
  create                       Create form (interactive)
  list                         List all forms
  show FORM-ID                 Show form details
  serve FORM-ID                Serve form via HTTP
  responses FORM-ID            Show responses
  export FORM-ID               Export to CSV/JSON
```

---

## Quick Start

### Your First Form

```bash
# 1. Create a simple form
smf run form-builder create --name "Contact Form" --fields name,email,message

# 2. Serve it
smf run form-builder serve FORM-ABC123 --port 8080

# 3. Open browser to http://localhost:8080/FORM-ABC123
# Fill out and submit

# 4. Stop server (Ctrl+C)

# 5. View responses
smf run form-builder responses FORM-ABC123

# 6. Export to CSV
smf run form-builder export FORM-ABC123 --format csv
```

---

## Creating Forms

### Interactive Mode (Recommended)

```bash
smf run form-builder create
```

**Step-by-step:**

1. **Form Name**
   ```
   Form name: Website Contact Form
   ```

2. **Description** (optional)
   ```
   Description: General inquiries from website visitors
   ```

3. **Add Fields**
   
   For each field, you'll enter:
   - **Field name** — Machine name (no spaces): `first_name`
   - **Label** — Display label: "First Name"
   - **Type** — Select from list
   - **Required** — y/n
   - **Placeholder** — Optional hint text

4. **Finish**
   - Leave field name blank to finish

**Example session:**
```
📝 Create New Form
----------------------------------------

Form name: Newsletter Signup
Description: Collect emails for newsletter

Add fields (leave name blank to finish):

Field 1:
Field name (or blank to finish): email
Label (or blank to use name): Email Address
Field type:
  1. text
  2. email
  3. number
  ...
Choice [2]: 2
Required? (y/n) [n]: y
Placeholder (optional): your@email.com

Field 2:
Field name (or blank to finish): first_name
Label: First Name
Choice [1]: 1
Required? (y/n) [n]: n

Field 3:
Field name (or blank to finish):

✅ Form created: FORM-20260320-A1B2C3D4
   Name: Newsletter Signup
   Fields: 2

Serve: smf run form-builder serve FORM-20260320-A1B2C3D4
```

### Quick Mode

**Single command:**
```bash
smf run form-builder create --name "Quick Survey" --fields name,rating,feedback
```

**All fields default to:**
- Type: text
- Required: false
- Label: Capitalized field name

**Add more fields later:**
```bash
smf run form-builder add-field FORM-XXX
```

### Field Types Reference

| Type | Use For | Example |
|------|---------|---------|
| `text` | Short text | Name, subject |
| `email` | Email addresses | contact@example.com |
| `number` | Numeric values | Age, quantity |
| `textarea` | Long text | Comments, description |
| `select` | Dropdown choices | Country, status |
| `checkbox` | True/false | Subscribe, agree to terms |
| `radio` | Single choice from many | Gender, priority |
| `date` | Date picker | Birth date, event date |
| `tel` | Phone numbers | +1-555-0199 |
| `url` | Web addresses | https://example.com |

**Select/Radio with options:**
```
Field type:
  ...
Choice: 5  (select)

Enter options (comma-separated):
Options: Small,Medium,Large,X-Large
```

---

## Serving Forms

### Basic Usage

```bash
smf run form-builder serve FORM-ABC123
```

**Output:**
```
🌐 Serving form 'Contact Form'
   URL: http://localhost:8080/FORM-ABC123
   Press Ctrl+C to stop
```

**Access:**
- Open browser
- Go to: `http://localhost:8080/FORM-ABC123`

### Custom Port

```bash
# Use port 3000
smf run form-builder serve FORM-ABC123 --port 3000

# URL becomes: http://localhost:3000/FORM-ABC123
```

**Common ports:**
- `8080` — Default
- `3000` — Development
- `8000` — Alternative

### Making Available on Network

**Local only (default):**
```bash
# Only accessible on your machine
smf run form-builder serve FORM-ABC123
```

**Network accessible:**
```bash
# Find your IP
hostname -I

# Server runs on all interfaces
# Access via: http://YOUR-IP:8080/FORM-ABC123
```

**Behind firewall/router:**
- Port forwarding required
- Or use reverse proxy (nginx)
- Consider security implications

### Stopping the Server

**Method 1: Ctrl+C**
- Focus terminal
- Press `Ctrl+C`
- Server stops

**Method 2: Background process**
```bash
# Start in background
smf run form-builder serve FORM-ABC123 &

# Find process
ps aux | grep "form-builder serve"

# Stop process
kill <PID>
```

### Production Deployment

**For public forms, consider:**

1. **Reverse proxy** (nginx)
```nginx
server {
    listen 80;
    server_name forms.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8080;
    }
}
```

2. **Systemd service**
```ini
[Unit]
Description=Form Builder

[Service]
ExecStart=/usr/bin/smf run form-builder serve FORM-XXX
Restart=always

[Install]
WantedBy=multi-user.target
```

3. **Tunnel services** (ngrok, localtunnel)
```bash
# Expose local server publicly
npx localtunnel --port 8080
```

---

## Managing Responses

### Viewing Responses

```bash
smf run form-builder responses FORM-ABC123
```

**Output:**
```
📊 Responses for 'Contact Form' (5)
--------------------------------------------------------------------------------

1. Response RESP-A1B2C3D4
   Submitted: 2026-03-20T14:30:00
   name: John Smith
   email: john@example.com
   message: Interested in your services

2. Response RESP-E5F6G7H8
   Submitted: 2026-03-20T15:45:00
   name: Jane Doe
   email: jane@example.com
   message: Quick question about pricing

... and 3 more responses
--------------------------------------------------------------------------------
```

### Exporting Responses

**CSV (for spreadsheets):**
```bash
smf run form-builder export FORM-ABC123 --format csv
```

Creates: `FORM-ABC123-responses.csv`

**JSON (for integrations):**
```bash
smf run form-builder export FORM-ABC123 --format json
```

Creates: `FORM-ABC123-responses.json`

**Custom filename:**
```bash
smf run form-builder export FORM-ABC123 --format csv --output leads-march.csv
```

### Importing to Spreadsheet

**LibreOffice Calc:**
```bash
localc FORM-ABC123-responses.csv
```

**Excel (Windows):**
```cmd
start FORM-ABC123-responses.csv
```

**Google Sheets:**
1. File → Import
2. Upload CSV
3. Configure columns

### Automated Processing

**Daily export script:**
```bash
#!/bin/bash
# daily-form-export.sh

export PATH="$HOME/.local/bin:$PATH"
DATE=$(date +%Y%m%d)

for form in FORM-ABC123 FORM-DEF456; do
    smf run form-builder export $form --format csv --output "/var/www/data/${form}-${DATE}.csv"
done
```

**Email new responses:**
```bash
#!/bin/bash
# check-new-responses.sh

export PATH="$HOME/.local/bin:$PATH"

FORM="FORM-ABC123"
COUNT=$(smf run form-builder responses $FORM 2>/dev/null | grep -c "Response")

if [ "$COUNT" -gt 0 ]; then
    smf run form-builder export $FORM --format csv
    echo "New responses available" | mail -s "Form Responses" -a "${FORM}-responses.csv" you@example.com
fi
```

---

## Automation

### Daily Response Report

**Create script:**
```bash
#!/bin/bash
# form-report.sh

export PATH="$HOME/.local/bin:$PATH"

echo "📊 Daily Form Report"
echo "=================="
echo ""

# Check all forms
for form_file in ~/.smf/forms/FORM-*.json; do
    form_id=$(basename "$form_file" .json)
    smf run form-builder show "$form_id" | grep -E "(Name|Responses)"
    echo ""
done
```

**Cron:**
```bash
# Daily at 9 AM
0 9 * * * ~/form-report.sh | mail -s "Daily Form Report" you@example.com
```

### Weekly Export

```bash
#!/bin/bash
# weekly-export.sh

export PATH="$HOME/.local/bin:$PATH"
WEEK=$(date +%Y-W%U)

mkdir -p "/var/www/exports/week-${WEEK}"

for form in $(smf run form-builder list | grep FORM- | awk '{print $1}'); do
    smf run form-builder export $form --format csv --output "/var/www/exports/week-${WEEK}/${form}.csv"
done
```

### Backup Forms

```bash
#!/bin/bash
# backup-forms.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="$HOME/backups/forms"

mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/forms-${DATE}.tar.gz" ~/.smf/forms/ ~/.smf/form-responses/

# Keep last 90 days
find "$BACKUP_DIR" -name "forms-*.tar.gz" -mtime +90 -delete

echo "Forms backed up to $BACKUP_DIR/forms-${DATE}.tar.gz"
```

**Daily backup:**
```bash
0 2 * * * ~/backup-forms.sh
```

---

## Troubleshooting

### "Form not found"

**Problem:** Wrong form ID

**Solution:**
```bash
# List all forms
smf run form-builder list

# Check spelling
# Form ID format: FORM-YYYYMMDD-XXXXXXXX
```

### "Port already in use"

**Problem:** Another service using port 8080

**Solution:**
```bash
# Use different port
smf run form-builder serve FORM-XXX --port 3000

# Or find and stop process
lsof -i :8080
kill <PID>
```

### "Cannot access form from another device"

**Problem:** Server bound to localhost only

**Solution:**
```bash
# Check your IP
hostname -I

# Server should be accessible on all interfaces
# Form Builder serves on 0.0.0.0 by default

# Check firewall
sudo ufw allow 8080
```

### "No responses showing"

**Check:**
```bash
# Verify form exists
smf run form-builder show FORM-XXX

# Check response files
ls ~/.smf/form-responses/

# Look for files matching RESP-*.json
```

### "Export creates empty file"

**Check:**
```bash
# Verify responses exist
smf run form-builder responses FORM-XXX

# Check permissions
ls -la ~/.smf/form-responses/

# Try export with verbose
smf run form-builder export FORM-XXX --format json
```

### Server crashes on submit

**Check logs:**
```bash
# Run in foreground to see errors
smf run form-builder serve FORM-XXX

# Check for:
# - Permission issues
# - Disk space
# - Malformed form data
```

### "Permission denied"

**Fix:**
```bash
# Check directory permissions
ls -la ~/.smf/

# Fix if needed
chmod 700 ~/.smf
chmod 700 ~/.smf/forms
chmod 700 ~/.smf/form-responses

# Check ownership
chown -R $USER:$USER ~/.smf/
```

---

## Best Practices

### 1. Test Forms Before Sharing

**Always test:**
```bash
# Create form
smf run form-builder create

# Serve locally
smf run form-builder serve FORM-XXX

# Submit test response
# Open browser, fill out, submit

# Verify
smf run form-builder responses FORM-XXX

# Then share
```

### 2. Use Descriptive Names

**Good:**
- "Website Contact Form - March 2026"
- "Customer Satisfaction Survey Q1"
- "Event Registration - Tech Conference"

**Bad:**
- "Form 1"
- "Test"
- "New Form"

### 3. Limit Required Fields

**Only require what's essential:**
- Contact form: email (required), name (optional)
- Survey: key question (required), demographics (optional)

**Don't require:**
- Phone number (unless necessary)
- Address (unless shipping)
- Optional comments

### 4. Keep Forms Short

**Optimal lengths:**
- Contact form: 3-5 fields
- Survey: 5-10 questions
- Registration: 5-8 fields

**Long forms = abandoned forms**

### 5. Clear Field Labels

**Good:**
- "Email Address" not "Email"
- "First Name" not "Name"
- "How can we help?" not "Message"

### 6. Validate Data

**Use appropriate field types:**
- Email addresses → `email` type
- Phone numbers → `tel` type
- Numbers only → `number` type

### 7. Regular Backups

```bash
# Daily backup
crontab -e
0 2 * * * tar -czf ~/backups/forms-$(date +\%Y\%m\%d).tar.gz ~/.smf/forms/ ~/.smf/form-responses/
```

### 8. Data Retention

**Consider privacy:**
- Delete old responses after processing
- Anonymize data when possible
- Comply with GDPR/CCPA if applicable

### 9. Monitor Response Quality

**Watch for:**
- Spam submissions
- Test data in production
- Incomplete responses

### 10. Secure Sensitive Forms

**For sensitive data:**
- Use HTTPS (reverse proxy)
- Limit access (IP whitelist)
- Encrypt data at rest
- Clear responses after processing

---

## Integration Examples

### With Email Notifications

```bash
#!/bin/bash
# notify-on-response.sh

export PATH="$HOME/.local/bin:$PATH"

FORM="FORM-ABC123"
LAST_COUNT_FILE="/tmp/form-${FORM}-count"

# Get current count
CURRENT=$(smf run form-builder responses $FORM 2>/dev/null | grep -c "Response")

# Get last count
LAST=$(cat "$LAST_COUNT_FILE" 2>/dev/null || echo "0")

# If new responses
if [ "$CURRENT" -gt "$LAST" ]; then
    NEW=$((CURRENT - LAST))
    echo "📧 $NEW new response(s) for form $FORM"
    
    # Export and email
    smf run form-builder export $FORM --format csv
    echo "New form responses" | mail -s "Form Alert" -a "${FORM}-responses.csv" you@example.com
fi

# Save count
echo "$CURRENT" > "$LAST_COUNT_FILE"
```

### With Slack Notifications

```bash
#!/bin/bash
# slack-notify.sh

WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

export PATH="$HOME/.local/bin:$PATH"

FORM="FORM-ABC123"
RESPONSES=$(smf run form-builder responses $FORM 2>/dev/null | wc -l)

curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"📊 Form $FORM has $RESPONSES responses\"}" \
  "$WEBHOOK_URL"
```

### With Database Import

```bash
#!/bin/bash
# import-to-postgres.sh

export PATH="$HOME/.local/bin:$PATH"

FORM="FORM-ABC123"

# Export to JSON
smf run form-builder export $FORM --format json --output /tmp/responses.json

# Import to PostgreSQL
psql -d mydb -c "
  CREATE TEMP TABLE temp_responses (data jsonb);
  \\copy temp_responses FROM '/tmp/responses.json';
  INSERT INTO form_responses SELECT * FROM temp_responses;
"
```

---

## Next Steps

1. **Create your first form** — Start simple
2. **Test thoroughly** — Before sharing
3. **Monitor responses** — Regular check-ins
4. **Set up backups** — Protect your data
5. **Explore integrations** — Connect to your workflow

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
