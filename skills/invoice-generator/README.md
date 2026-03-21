# Invoice Generator

Create professional invoices, track payments, and manage billing for your business.

## Features

- ✅ **Client Management** — Store client details and payment terms
- ✅ **Professional Invoices** — Itemized billing with tax and discounts
- ✅ **Multiple Formats** — Export as HTML or JSON
- ✅ **Payment Tracking** — Record partial and full payments
- ✅ **Status Management** — Draft, sent, paid, overdue, cancelled
- ✅ **Financial Reports** — Monthly and cumulative revenue reports
- ✅ **Local Storage** — All data stays on your machine

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install invoice-generator
```

## Quick Start

### 1. Add a Client

```bash
smf run invoice-generator client add "Acme Corporation"
```

### 2. Create an Invoice

```bash
# Interactive mode
smf run invoice-generator create

# Quick mode
smf run invoice-generator create \
  --client "Acme Corporation" \
  --item "Website Design:1:1500" \
  --item "Hosting:12:50"
```

### 3. Export as HTML

```bash
smf run invoice-generator export INV-202603-ABC123
# Creates: INV-202603-ABC123.html
```

### 4. Record Payment

```bash
smf run invoice-generator pay INV-202603-ABC123 --amount 1500 --method "bank-transfer"
```

## Usage

### Client Management

**Add client:**
```bash
smf run invoice-generator client add "Company Name"
```

**List clients:**
```bash
smf run invoice-generator client list
```

### Creating Invoices

**Interactive mode:**
```bash
smf run invoice-generator create
```

You'll be prompted for:
- Client name
- Invoice items (description, quantity, price)
- Tax rate (optional)
- Discount (optional)
- Notes (optional)

**Quick mode with items:**
```bash
smf run invoice-generator create \
  --client "Acme Corp" \
  --item "Website Design:1500" \
  --item "Logo Design:500" \
  --item "Hosting Setup:1:200"
```

**Item format:**
- `Description:Price` — Single quantity
- `Description:Qty:Price` — Multiple quantity
- Example: `Consulting:10:150` = 10 hours at $150/hour

**With tax and discount:**
```bash
smf run invoice-generator create \
  --client "Acme Corp" \
  --item "Services:2000" \
  --item "Materials:500" \
  --tax 8.5 \
  --discount 10
```

### Listing Invoices

**All invoices:**
```bash
smf run invoice-generator list
```

**Filter by status:**
```bash
smf run invoice-generator list --status paid
smf run invoice-generator list --status overdue
```

**Invoice statuses:**
- `draft` — Created but not sent
- `sent` — Sent to client
- `paid` — Fully paid
- `overdue` — Past due date
- `cancelled` — Voided

### Viewing Invoice Details

```bash
smf run invoice-generator show INV-202603-ABC123
```

Output:
```
📄 Invoice INV-202603-ABC123
============================================================
Status: PAID
Client: Acme Corporation
Date: 2026-03-20
Due: 2026-04-20

Items:
  • Website Design: 1 x $1500.00 = $1500.00
  • Hosting Setup: 1 x $200.00 = $200.00

Subtotal: $1700.00
Tax: $144.50
Total: $1844.50
```

### Recording Payments

**Full payment:**
```bash
smf run invoice-generator pay INV-202603-ABC123 --amount 1844.50 --method "bank-transfer"
```

**Partial payment:**
```bash
smf run invoice-generator pay INV-202603-ABC123 --amount 1000 --method "check"
```

**Payment methods:**
- bank-transfer
- check
- credit-card
- cash
- paypal
- other

### Exporting Invoices

**Export as HTML (for email/print):**
```bash
smf run invoice-generator export INV-202603-ABC123 --html
```

**Export as JSON (for integration):**
```bash
smf run invoice-generator export INV-202603-ABC123 --json
```

Open HTML invoice:
```bash
# Linux
xdg-open ~/.smf/invoices/INV-202603-ABC123.html

# macOS
open ~/.smf/invoices/INV-202603-ABC123.html
```

### Financial Reports

**All-time report:**
```bash
smf run invoice-generator report
```

**Monthly report:**
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
  • Consulting Inc: $2,400.00
```

## Invoice Format

### HTML Invoice Includes:

- Professional header with your company name
- Client billing information
- Invoice number and dates
- Itemized line items with quantities
- Subtotal, discount, tax calculations
- Grand total with status badge
- Payment terms and thank you message

**Status badges:**
- ✅ **PAID** (green)
- 📤 **SENT** (blue)
- 📝 **DRAFT** (gray)
- ⚠️ **OVERDUE** (red)
- ❌ **CANCELLED** (gray)

### Sample Invoice Structure

```
YOUR COMPANY NAME

INVOICE                                               [STATUS BADGE]

Bill To:                              Invoice Number: INV-202603-ABC123
Acme Corporation                      Date: 2026-03-20
contact@acme.com                      Due Date: 2026-04-20
123 Main St

------------------------------------------------------------
Description              Qty    Unit Price    Total
------------------------------------------------------------
Website Design           1      $1,500.00     $1,500.00
Logo Design              1      $500.00       $500.00
------------------------------------------------------------

Subtotal:                              $2,000.00
Discount (10%):                         -$200.00
Tax (8.5%):                           $153.00
------------------------------------------------------------
Total:                                 $1,953.00

Notes:
Payment terms: Net 30 days

Thank you for your business!
```

## Storage Structure

```
~/.smf/invoices/
├── clients.json                    # Client database
├── INV-202603-ABC123.json          # Invoice data
├── INV-202603-ABC123.html          # HTML export
├── INV-202603-DEF456.json
└── ...
```

### Invoice JSON Format

```json
{
  "id": "INV-202603-ABC123",
  "invoice_number": "INV-202603-ABC123",
  "client_id": "client-a1b2c3d4",
  "client_name": "Acme Corporation",
  "client_email": "billing@acme.com",
  "items": [
    {
      "description": "Website Design",
      "quantity": 1,
      "unit_price": 1500.00,
      "total": 1500.00
    }
  ],
  "subtotal": 1500.00,
  "discount_percent": 0,
  "discount_amount": 0,
  "tax_percent": 8.5,
  "tax_amount": 127.50,
  "total": 1627.50,
  "currency": "USD",
  "status": "paid",
  "created_at": "2026-03-20T14:30:00",
  "due_date": "2026-04-20",
  "paid_at": "2026-03-25T10:00:00",
  "payments": [
    {
      "amount": 1627.50,
      "method": "bank-transfer",
      "paid_at": "2026-03-25T10:00:00"
    }
  ]
}
```

## Workflows

### Monthly Billing Cycle

**Week 1:**
```bash
# Review outstanding invoices
smf run invoice-generator list --status sent
smf run invoice-generator list --status overdue

# Send reminders for overdue
```

**Week 2:**
```bash
# Create new invoices
smf run invoice-generator create --client "Client A" --item "Monthly Services:1000"
smf run invoice-generator create --client "Client B" --item "Retainer:2500"

# Export and send
smf run invoice-generator export INV-202603-...
# Email HTML files to clients
```

**Week 3:**
```bash
# Record payments as they come in
smf run invoice-generator pay INV-202603-... --amount 1000 --method "bank-transfer"
```

**Week 4:**
```bash
# Generate monthly report
smf run invoice-generator report --month 2026-03
```

### Project-Based Billing

**Milestone 1 - Deposit:**
```bash
smf run invoice-generator create \
  --client "Tech Startup" \
  --item "Project Deposit:5000"
```

**Milestone 2 - Development:**
```bash
smf run invoice-generator create \
  --client "Tech Startup" \
  --item "Development Phase:15000"
```

**Milestone 3 - Final:**
```bash
smf run invoice-generator create \
  --client "Tech Startup" \
  --item "Final Delivery:5000"
```

## Automation

### Monthly Invoice Generation

Create `~/monthly-billing.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

MONTH=$(date +%B)
YEAR=$(date +%Y)

# Generate invoices for recurring clients
smf run invoice-generator create \
  --client "Client A" \
  --item "Monthly Retainer:2000" \
  --item "Hosting:${MONTH} ${YEAR}:100"

smf run invoice-generator create \
  --client "Client B" \
  --item "Support Plan:${MONTH}:500"

# Export all draft invoices
for inv in ~/.smf/invoices/INV-*.json; do
    id=$(basename $inv .json)
    smf run invoice-generator export $id --html
done

# Email to clients (requires mail setup)
echo "Monthly invoices generated" | mail -s "Invoices ${MONTH} ${YEAR}" you@example.com
```

**Cron:**
```bash
# First of every month
0 9 1 * * ~/monthly-billing.sh
```

### Payment Reminders

```bash
#!/bin/bash
# check-overdue.sh

export PATH="$HOME/.local/bin:$PATH"

OVERDUE=$(smf run invoice-generator list --status overdue 2>/dev/null | wc -l)

if [ "$OVERDUE" -gt 0 ]; then
    echo "⚠️  $OVERDUE overdue invoices:"
    smf run invoice-generator list --status overdue
fi
```

**Weekly check:**
```bash
0 9 * * 1 ~/check-overdue.sh
```

## Best Practices

### 1. Invoice Promptly

- Bill within 24-48 hours of work completion
- Don't wait until end of month

### 2. Clear Descriptions

**Good:**
- "Website Design - 10 pages"
- "Consulting - March 2026 - 20 hours"

**Bad:**
- "Services"
- "Work"

### 3. Net 30 Terms

Standard payment terms, but adjust for:
- New clients: Net 15 or payment upfront
- Large projects: Milestone payments
- Late payers: Require deposit

### 4. Track Everything

- Always record payments immediately
- Note partial payments
- Keep payment method for records

### 5. Follow Up

- Send reminder 7 days before due
- Send reminder 7 days after due
- Call after 30 days overdue

### 6. Keep Backups

```bash
# Backup invoices weekly
tar -czf ~/backups/invoices-$(date +%Y%m%d).tar.gz ~/.smf/invoices/

# Keep in cloud
dropbox upload ~/backups/invoices-*.tar.gz /backups/
```

## Pricing

**Invoice Generator is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use Wave, Invoice Ninja, or spreadsheet

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
