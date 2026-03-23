# Invoice Generator — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Add a Client and Create an Invoice](#1-how-to-add-a-client-and-create-an-invoice)
2. [How to Export an Invoice as HTML](#2-how-to-export-an-invoice-as-html)
3. [How to Record a Payment](#3-how-to-record-a-payment)
4. [How to Track Outstanding Invoices](#4-how-to-track-outstanding-invoices)
5. [How to Generate a Monthly Financial Report](#5-how-to-generate-a-monthly-financial-report)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Add a Client and Create an Invoice

**What this does:** Registers a client and creates an itemized invoice for them.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/invoice-generator
```

**Step 2 — Add the client.**

```bash
python3 main.py client add "Acme Corporation"
```

Output:
```
✅ Client added: Acme Corporation (acme-corporation)
```

**Step 3 — Create an invoice for them.**

```bash
python3 main.py create --client "Acme" --item "Website Design:3000" --item "SEO Audit:500" --item "Monthly Hosting:150"
```

Output:
```
✅ Invoice created: INV-202403-A1B2C3

   Client: Acme Corporation
   Items:
     Website Design      $3,000.00
     SEO Audit           $  500.00
     Monthly Hosting     $  150.00
   ────────────────────────────────────
   Total:                $3,650.00

   Status: unpaid
   Due: 2024-04-14 (30 days)
```

**Step 4 — Show the full invoice.**

```bash
python3 main.py show INV-202403-A1B2C3
```

**Result:** Invoice is created and ready to export.

---

## 2. How to Export an Invoice as HTML

**What this does:** Creates an HTML file of the invoice — ready to send to the client or print as PDF.

### Steps

**Step 1 — Export the invoice.**

```bash
python3 main.py export INV-202403-A1B2C3 --html
```

Output:
```
✅ Invoice exported: INV-202403-A1B2C3.html
```

**Step 2 — Open it to review.**

```bash
# macOS:
open INV-202403-A1B2C3.html

# Linux:
xdg-open INV-202403-A1B2C3.html
```

**Step 3 — Convert to PDF for sending.**

In Chrome: File → Print → Save as PDF

Or via command line:
```bash
# If wkhtmltopdf is installed:
wkhtmltopdf INV-202403-A1B2C3.html INV-202403-A1B2C3.pdf
```

**Step 4 — Email to client manually.**

Attach the PDF or HTML to an email and send.

**Result:** A professional invoice the client can open in any browser or PDF reader.

---

## 3. How to Record a Payment

**What this does:** Marks an invoice as paid and records the payment date.

### Steps

**Step 1 — Record full payment.**

```bash
python3 main.py pay INV-202403-A1B2C3
```

Output:
```
✅ Payment recorded: INV-202403-A1B2C3
   Amount: $3,650.00
   Status: paid
   Paid date: 2024-03-25
```

**Step 2 — Record partial payment.**

```bash
python3 main.py pay INV-202403-A1B2C3 --amount 1825.00
```

**Result:** Invoice status updated. It will no longer appear in unpaid invoice lists.

---

## 4. How to Track Outstanding Invoices

**What this does:** Shows only unpaid invoices so you know what money is owed to you.

```bash
python3 main.py list --status unpaid
```

Output:
```
Unpaid Invoices (3 total):

INV-202403-A1B2C3 — Acme Corporation — $3,650.00 — UNPAID — Due 2024-04-14 ⚠️ OVERDUE
INV-202403-D4E5F6 — TechStartup Inc — $2,000.00 — UNPAID — Due 2024-04-20
INV-202402-G7H8I9 — Freelance Client — $800.00 — UNPAID — Due 2024-03-28 ⚠️ OVERDUE
```

Action on overdue invoices: Follow up with the client and record payment when received with `pay`.

---

## 5. How to Generate a Monthly Financial Report

**What this does:** Summarizes all invoicing activity for a month — issued, collected, outstanding.

```bash
python3 main.py report --month 2024-03
```

Output:
```
📊 Financial Report — March 2024

Invoices issued: 6
Total invoiced: $12,400.00
Total collected: $9,100.00
Outstanding: $3,300.00

Paid on time: 4
Late: 1
Pending: 1

By client:
  Acme Corporation: $6,200.00 invoiced, $4,400.00 collected
  TechStartup Inc: $3,500.00 invoiced, $3,500.00 collected
  Freelance Client: $2,700.00 invoiced, $1,200.00 collected
```

---

## 6. Automating with Cron

### Example: Monthly reminder to review outstanding invoices

```bash
0 9 1 * * python3 /home/yourname/smfworks-skills/skills/invoice-generator/main.py list --status unpaid >> /home/yourname/logs/invoices.log 2>&1
```

### Example: Monthly report on the 1st

```bash
0 8 1 * * python3 /home/yourname/smfworks-skills/skills/invoice-generator/main.py report --month $(date +\%Y-\%m) >> /home/yourname/Reports/monthly-finance.txt 2>&1
```

---

## 7. Combining with Other Skills

**Invoice Generator + Report Generator:** Generate a detailed financial report from invoice data:

```bash
python3 main.py export INV-202403-ABC123 --json > /tmp/invoice.json
python3 ~/smfworks-skills/skills/report-generator/main.py create --data /tmp/invoices.csv --title "Q1 Revenue"
```

**Invoice Generator + CSV Converter:** Export all invoices to Excel for your accountant:

```bash
# After exporting invoices list as CSV
python3 ~/smfworks-skills/skills/csv-converter/main.py csv-to-excel invoices.csv invoices.xlsx
```

---

## 8. Troubleshooting Common Issues

### `Client not found`

**Fix:** Client lookup is by partial name match. Check exact client names with `python3 main.py client list`.

### `Invoice not found: INV-XYZ`

**Fix:** IDs are case-sensitive. Run `python3 main.py list` to find the exact ID.

### Amount shows as incorrect

**Fix:** Ensure `--item` amounts use decimal notation: `1500.00` not `1500`. The skill uses Decimal arithmetic for accuracy.

---

## 9. Tips & Best Practices

**Create invoices immediately after completing work.** Memory fades — invoice on the day you finish, while you remember all the line items.

**Always export and keep a copy.** Even if the client has the PDF, keep your own copy of every invoice HTML file. Store them in `~/Invoices/YYYY/` organized by year.

**Follow up on overdue invoices.** Run `list --status unpaid` weekly. For invoices more than 7 days past due, send a friendly reminder. For 30+ days overdue, send a firmer follow-up.

**Use descriptive line item names.** "Consulting: 3 hours" is better than "Services" — it helps clients understand what they're paying for and reduces payment disputes.

**Run monthly reports consistently.** The `report --month YYYY-MM` command gives you a clear financial picture. Run it on the 1st of each month to close out the previous month.
