# Invoice Generator - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Invoice Generator skill.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [Quick Start](#quick-start)
5. [Client Management](#client-management)
6. [Creating Invoices](#creating-invoices)
7. [Managing Payments](#managing-payments)
8. [Financial Reporting](#financial-reporting)
9. [Automation](#automation)
10. [Troubleshooting](#troubleshooting)
11. [Best Practices](#best-practices)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Storage:** Minimal (~100KB per 100 invoices)

### SMF Works Subscription
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

### Business Information
- Company name (for invoice header)
- Business address (optional)
- Tax ID (optional)

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

### Step 3: Install Invoice Generator

```bash
smf install invoice-generator
```

### Step 4: Verify Installation

```bash
smf run invoice-generator --help
```

---

## Quick Start

### Your First Invoice

```bash
# 1. Add a client
smf run invoice-generator client add "Your First Client"

# 2. Create invoice
smf run invoice-generator create --client "Your First Client" --item "Services:500"

# 3. Export as HTML
smf run invoice-generator export INV-202603-ABC123

# 4. Open and review
xdg-open ~/.smf/invoices/INV-202603-ABC123.html
```

### Basic Workflow

```bash
# Monthly billing workflow

# 1. Create invoices
smf run invoice-generator create --client "Client A" --item "Monthly:1000"
smf run invoice-generator create --client "Client B" --item "Services:1500"

# 2. Export all
for inv in ~/.smf/invoices/INV-*.json; do
    id=$(basename $inv .json)
    smf run invoice-generator export $id
done

# 3. Email to clients (manual or scripted)

# 4. Record payments as received
smf run invoice-generator pay INV-... --amount 1000

# 5. Check status
smf run invoice-generator list

# 6. Generate report
smf run invoice-generator report --month 2026-03
```

---

## Client Management

### Adding Clients

**Interactive:**
```bash
smf run invoice-generator client add
# Enter name when prompted
```

**Command line:**
```bash
smf run invoice-generator client add "Company Name"
```

### Client Information

Currently stored:
- Client ID (auto-generated)
- Client name
- Created date

**Future enhancements** (edit `~/.smf/invoices/clients.json`):
```json
{
  "id": "client-abc123",
  "name": "Acme Corp",
  "email": "billing@acme.com",
  "address": "123 Main St\nCity, State 12345",
  "tax_id": "12-3456789",
  "payment_terms": 30
}
```

### Managing Clients

**List all clients:**
```bash
smf run invoice-generator client list
```

**Edit client:**
```bash
# Directly edit the JSON file
nano ~/.smf/invoices/clients.json
```

**Delete client:**
```bash
# Remove from clients.json manually
# (Will not affect existing invoices)
```

---

## Creating Invoices

### Interactive Mode

```bash
smf run invoice-generator create
```

**Step-by-step:**
1. **Client name** — Type or select existing
2. **Items** — Enter description, quantity, price for each
3. **Tax** — Enter tax rate percentage (or 0)
4. **Discount** — Enter discount percentage (or 0)
5. **Notes** — Payment terms, thank you message, etc.

### Command Line Mode

**Simple invoice:**
```bash
smf run invoice-generator create \
  --client "Client Name" \
  --item "Description:100"
```

**Multiple items:**
```bash
smf run invoice-generator create \
  --client "Client Name" \
  --item "Website Design:1500" \
  --item "Logo Design:2:250" \
  --item "Hosting:12:50"
```

**Item format options:**
- `Description:Price` — Single item
- `Description:Qty:Price` — Multiple quantity
- Examples:
  - `Consulting:150` = 1 × $150
  - `Hours:10:150` = 10 × $150 = $1,500
  - `Widget:5:25` = 5 × $25 = $125

**With tax:**
```bash
smf run invoice-generator create \
  --client "Client" \
  --item "Services:1000" \
  --tax 8.5
```

**With discount:**
```bash
smf run invoice-generator create \
  --client "Client" \
  --item "Services:2000" \
  --discount 10
```

**Combined:**
```bash
smf run invoice-generator create \
  --client "Client" \
  --item "Services:1000" \
  --item "Materials:500" \
  --tax 8.5 \
  --discount 5
```

### Invoice Status Workflow

```
Draft → Sent → Paid
   ↓       ↓
Cancelled Overdue
```

**Status meanings:**
- **draft** — Created, not yet sent
- **sent** — Sent to client (manually update)
- **paid** — Fully paid (auto when payments cover total)
- **overdue** — Past due date (manually track)
- **cancelled** — Voided invoice

**Update status:**
```bash
# Currently requires manual JSON edit
# Future: smf run invoice-generator update INV-123 --status sent
```

---

## Managing Payments

### Recording Payments

**Full payment:**
```bash
smf run invoice-generator pay INV-202603-ABC123 \
  --amount 1500.00 \
  --method "bank-transfer"
```

**Partial payment:**
```bash
smf run invoice-generator pay INV-202603-ABC123 \
  --amount 500.00 \
  --method "check" \
  --notes "Deposit received"
```

**Multiple payments:**
```bash
# First payment
smf run invoice-generator pay INV-... --amount 500

# Second payment
smf run invoice-generator pay INV-... --amount 500

# Final payment (marks as paid)
smf run invoice-generator pay INV-... --amount 500
```

### Payment Methods

**Standard methods:**
- `bank-transfer` — ACH, wire transfer
- `check` — Paper check
- `credit-card` — Card payment
- `cash` — Cash payment
- `paypal` — PayPal
- `other` — Other methods

**Track in JSON:**
```json
"payments": [
  {
    "amount": 500.00,
    "method": "check",
    "notes": "Invoice 123",
    "paid_at": "2026-03-25T10:00:00"
  }
]
```

---

## Financial Reporting

### Monthly Report

```bash
smf run invoice-generator report --month 2026-03
```

Output:
```
💰 Financial Report: 2026-03
==================================================

Total Invoices: 12
Total Invoiced: $15,400.00
Total Paid: $12,800.00
Outstanding: $2,600.00
Collection Rate: 83.1%

Top Clients:
  • Acme Corporation: $5,200.00
  • Tech Startup LLC: $3,800.00
```

### All-Time Report

```bash
smf run invoice-generator report
```

### Year-to-Date

```bash
# Filter by year prefix
smf run invoice-generator list | grep "2026-"
```

### Outstanding Balances

```bash
# Unpaid invoices
smf run invoice-generator list --status sent
smf run invoice-generator list --status overdue

# Calculate total outstanding
# (Use report command for total)
```

### Client Reports

```bash
# View all invoices for client
# (Filter list output)
smf run invoice-generator list | grep "Client Name"
```

---

## Automation

### Monthly Billing Script

Create `~/monthly-invoices.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

MONTH=$(date +%B)
YEAR=$(date +%Y)

echo "Generating invoices for ${MONTH} ${YEAR}..."

# Recurring monthly services
smf run invoice-generator create \
  --client "Client A" \
  --item "Monthly Retainer:${MONTH} ${YEAR}:2000" \
  --item "Hosting:${MONTH}:100"

smf run invoice-generator create \
  --client "Client B" \
  --item "Support Plan:${MONTH}:500"

# Export all new invoices
for inv in ~/.smf/invoices/INV-*.json; do
    created=$(stat -c %Y "$inv" 2>/dev/null || stat -f %m "$inv")
    now=$(date +%s)
    # If created in last hour
    if [ $((now - created)) -lt 3600 ]; then
        id=$(basename "$inv" .json)
        smf run invoice-generator export "$id"
        echo "Exported: $id"
    fi
done

echo "Done! Check ~/.smf/invoices/ for HTML files"
```

Make executable:
```bash
chmod +x ~/monthly-invoices.sh
```

**Cron (monthly):**
```bash
# First of month at 9 AM
0 9 1 * * ~/monthly-invoices.sh
```

### Payment Reminder Script

Create `~/payment-reminders.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

# Check for overdue invoices
OVERDUE=$(smf run invoice-generator list --status overdue 2>/dev/null)

if [ -n "$OVERDUE" ]; then
    echo "⚠️  Overdue invoices found:"
    echo "$OVERDUE"
    
    # Email reminder (configure mail)
    # echo "$OVERDUE" | mail -s "Payment Reminder" billing@example.com
fi

# Check for upcoming due (within 7 days)
# (Requires date comparison logic)
```

**Weekly:**
```bash
0 9 * * 1 ~/payment-reminders.sh
```

### Backup Script

```bash
#!/bin/bash
# backup-invoices.sh

DATE=$(date +%Y%m%d)
BACKUP_DIR="$HOME/backups/invoices"

mkdir -p "$BACKUP_DIR"

# Create backup
tar -czf "$BACKUP_DIR/invoices-$DATE.tar.gz" ~/.smf/invoices/

# Keep only last 90 days
find "$BACKUP_DIR" -name "invoices-*.tar.gz" -mtime +90 -delete

echo "Invoices backed up to $BACKUP_DIR/invoices-$DATE.tar.gz"
```

**Daily:**
```bash
0 2 * * * ~/backup-invoices.sh
```

### Accounting Export

```bash
#!/bin/bash
# Export for accounting software

# Generate CSV of all invoices
{
    echo "Invoice Number,Client,Date,Amount,Status"
    for inv in ~/.smf/invoices/INV-*.json; do
        python3 -c "
import json
with open('$inv') as f:
    i = json.load(f)
    print(f\"{i['invoice_number']},{i['client_name']},{i['created_at'][:10]},{i['total']},{i['status']}\")
"
    done
} > invoices-export.csv

echo "Exported to invoices-export.csv"
```

---

## Troubleshooting

### "Client not found"

**Problem:** Client doesn't exist

**Solution:**
```bash
# Check existing clients
smf run invoice-generator client list

# Add client first
smf run invoice-generator client add "Client Name"

# Or check spelling
```

### "Invoice not found"

**Problem:** Wrong invoice ID

**Solution:**
```bash
# List invoices to get ID
smf run invoice-generator list

# Use full ID including INV- prefix
smf run invoice-generator show INV-202603-ABC123
```

### Invoice not showing in list

**Check:**
```bash
# Verify file exists
ls ~/.smf/invoices/INV-*.json

# Check permissions
ls -la ~/.smf/invoices/

# Validate JSON
python3 -m json.tool ~/.smf/invoices/INV-202603-ABC123.json
```

### HTML export fails

**Check:**
```bash
# Invoice exists
smf run invoice-generator show INV-...

# Directory writable
touch ~/.smf/invoices/test 2>&1 || echo "Permission denied"

# Disk space
df -h ~/.smf/invoices/
```

### Payment doesn't update status

**Check:**
```bash
# Verify payment amount
# Status updates to "paid" only when total payments >= invoice total

# Manual check
smf run invoice-generator show INV-...
# Check "payments" array in output
```

### Report shows wrong numbers

**Check date format:**
```bash
# Correct
smf run invoice-generator report --month 2026-03

# Incorrect
smf run invoice-generator report --month March
smf run invoice-generator report --month 03/2026
```

### Storage growing too large

**Archive old invoices:**
```bash
# Move old invoices to archive
mkdir ~/.smf/invoices/archive
cd ~/.smf/invoices

# Move invoices older than 2 years
find . -name "INV-20[12]*.json" -mtime +730 -exec mv {} archive/ \;

# Keep exports
# (Optional) Delete old HTML files
find . -name "INV-*.html" -mtime +365 -delete
```

---

## Best Practices

### 1. Invoice Promptly

- **Within 48 hours** of work completion
- **Weekly** for ongoing projects
- **Monthly** for retainers

**Don't:**
- Wait until end of month
- Batch too many invoices
- Forget to invoice small items

### 2. Use Clear Descriptions

**Good:**
- "Website Design - 10 page custom site"
- "Consulting - March 2026 - 20 hours"
- "Logo Design - 3 revisions included"

**Bad:**
- "Work"
- "Services"
- "Project"

### 3. Set Payment Terms

**Standard:** Net 30

**Adjust for:**
- New clients: Net 15 or 50% upfront
- Large projects: Milestone payments
- Problem clients: Payment before delivery

### 4. Track Everything

- Invoice number
- Date sent
- Payment received date
- Payment method
- Any notes

### 5. Follow Up

**Timeline:**
- 7 days before due: Friendly reminder
- Day after due: First follow-up
- 7 days overdue: Second follow-up
- 30 days overdue: Phone call

### 6. Keep Backups

```bash
# Daily backup
crontab -e
0 2 * * * cp -r ~/.smf/invoices ~/Dropbox/backups/

# Or use git
cd ~/.smf/invoices
git init
git add .
git commit -m "Daily backup"
git push origin main
```

### 7. Reconcile Regularly

**Monthly:**
```bash
# Compare invoice report to bank statement
smf run invoice-generator report --month 2026-03

# Check for discrepancies
```

### 8. Archive Completed

**Year-end:**
```bash
# Archive paid invoices older than 1 year
mkdir ~/.smf/invoices/archive/2025
find ~/.smf/invoices -name "INV-2025*.json" -exec mv {} archive/2025/ \;
```

---

## Next Steps

1. **Add your clients** — Start with top 5
2. **Create first invoice** — Test the workflow
3. **Export and review** — Check HTML format
4. **Set up automation** — Monthly billing script
5. **Establish routine** — Weekly invoicing habit

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
