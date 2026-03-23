# Invoice Generator

> Create professional invoices and track payments — no accounting software needed

---

## What It Does

Invoice Generator creates clean, professional invoices for freelancers and small businesses. Add line items, apply tax, track payment status, and export to PDF. Everything runs locally — no subscriptions or cloud services.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install invoice-generator
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Create your first invoice:

```bash
python main.py create --client "Acme Corp" --items "Consulting,150,10"
```

---

## Commands

### `create`

**What it does:** Create a new invoice with line items.

**Usage:**
```bash
python main.py create --client [name] --items [items]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--client` | ✅ Yes | Client name | `--client "Acme Corp"` |
| `--items` | ✅ Yes | Items as "name,price,qty" (comma-separated) | `--items "Service,100,1"` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--tax` | ❌ No | Tax rate percentage | `--tax 10` |
| `--due` | ❌ No | Due date (YYYY-MM-DD) | `--due 2026-04-01` |
| `--notes` | ❌ No | Additional notes | `--notes "Thank you!"` |

**Example:**
```bash
python main.py create --client "Acme Corp" --items "Consulting,150,10"
python main.py create --client "Jane Doe" --items "Design,75,20,Web design work" --tax 8.5
```

**Output:**
```
✅ Invoice created: INV-001
   Client: Acme Corp
   Amount: $1,500.00
   Due: 2026-04-01
   Status: pending

To view: python main.py show INV-001
To export PDF: python main.py pdf INV-001
```

---

### `list`

**What it does:** Display all invoices with status.

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
📋 Invoices:
------------------------------------------------------------
INV-001 | Acme Corp    | $1,500.00 | pending  | Due: 2026-04-01
INV-002 | Jane Doe     | $600.00   | paid     | Paid: 2026-03-15
INV-003 | Bob Smith    | $225.00   | overdue  | Due: 2026-03-01
```

---

### `show`

**What it does:** Display full invoice details.

**Usage:**
```bash
python main.py show [invoice-id]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `invoice-id` | ✅ Yes | Invoice ID to display | `INV-001` |

**Example:**
```bash
python main.py show INV-001
```

---

### `pdf`

**What it does:** Export an invoice to PDF format.

**Usage:**
```bash
python main.py pdf [invoice-id] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `invoice-id` | ✅ Yes | Invoice ID to export | `INV-001` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--output` | ❌ No | Output file path | `--output invoice.pdf` |

**Example:**
```bash
python main.py pdf INV-001
python main.py pdf INV-001 --output ~/invoices/INV-001.pdf
```

---

### `mark`

**What it does:** Update invoice payment status.

**Usage:**
```bash
python main.py mark [invoice-id] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `invoice-id` | ✅ Yes | Invoice ID to update | `INV-001` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--paid` | ❌ No | Mark as paid | `--paid` |
| `--overdue` | ❌ No | Mark as overdue | `--overdue` |
| `--pending` | ❌ No | Mark as pending | `--pending` |

**Example:**
```bash
python main.py mark INV-001 --paid
```

---

## Use Cases

- **Freelance billing:** Invoice clients for consulting or contract work
- **Small business:** Generate invoices for products or services
- **Recurring billing:** Track monthly retainer invoices
- **Payment tracking:** Know what's paid, pending, or overdue
- **Record keeping:** Keep digital copies of all invoices

---

## Tips & Tricks

- Use multiple `--items` for multiple line items
- Set `--tax` to add sales tax or VAT automatically
- Set `--due` for net-30 or net-60 payment terms
- Export to PDF before sending to clients

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Client name required" | Make sure to use `--client "Name"` with quotes |
| Items format wrong | Use `"Item Name,price,quantity"` format |
| PDF export fails | Ensure `reportlab` is installed: `pip install reportlab` |
| Invoice not found | Check with `python main.py list` |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- (Optional) `reportlab` for PDF export (`pip install reportlab`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/invoice-generator)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
