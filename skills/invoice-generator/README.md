# Invoice Generator

> Create professional invoices, manage clients, record payments, export to HTML, and generate financial reports — from the terminal.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Business / Finance

---

## What It Does

Invoice Generator is an OpenClaw Pro skill for freelancers and small businesses to manage invoicing from the command line. Add clients, create itemized invoices, record payments, export invoices as HTML, and run monthly financial reports. Uses proper Decimal arithmetic for accurate currency calculations.

**What it does NOT do:** It does not send invoices by email automatically, integrate with accounting software (QuickBooks, Xero), accept online payments, or generate PDF files directly (convert HTML output to PDF manually).

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/invoice-generator
python3 main.py help
```

---

## Quick Start

```bash
# Add a client
python3 main.py client add "Acme Corp"

# Create an invoice
python3 main.py create --client "Acme" --item "Web Design:3000" --item "SEO Audit:500"

# List invoices
python3 main.py list

# Export to HTML
python3 main.py export INV-202403-ABC123
```

---

## Command Reference

### `client add "Name"`

Adds a new client.

```bash
python3 main.py client add "Acme Corp"
python3 main.py client add "TechStartup Inc"
```

Output:
```
✅ Client added: Acme Corp (acme-corp)
```

---

### `client list`

Lists all clients.

```bash
python3 main.py client list
```

Output:
```
Clients (3 total):
1. Acme Corp (acme-corp) — 4 invoices, $12,500 total
2. TechStartup Inc (techstartup-inc) — 2 invoices, $6,200 total
3. Freelance Client (freelance-client) — 1 invoice, $1,800 total
```

---

### `create`

Creates an invoice. Interactive if no flags; flags for quick creation.

```bash
python3 main.py create                                    # Interactive
python3 main.py create --client "Acme Corp"              # With client
python3 main.py create --client "Acme" --item "Design:1500" --item "Revisions:300"
```

**`--item` format:** `"Description:Amount"` (amount in USD)

Output:
```
✅ Invoice created: INV-202403-ABC123

   Client: Acme Corp
   Items:
     Web Design         $1,500.00
     Revisions          $  300.00
   ─────────────────────────────────
   Total:               $1,800.00

   Status: unpaid
   Due: 2024-04-14 (30 days)
```

---

### `list`

Lists all invoices, with optional status filter.

```bash
python3 main.py list
python3 main.py list --status unpaid
python3 main.py list --status paid
```

Output:
```
Invoices (8 total):

INV-202403-ABC123 — Acme Corp — $1,800.00 — UNPAID — Due 2024-04-14
INV-202403-DEF456 — TechStartup — $3,500.00 — PAID — 2024-03-20
INV-202402-GHI789 — Acme Corp — $2,400.00 — PAID — 2024-03-01
```

---

### `show INV-ID`

Shows full invoice details.

```bash
python3 main.py show INV-202403-ABC123
```

---

### `pay INV-ID`

Records a payment for an invoice.

```bash
python3 main.py pay INV-202403-ABC123
python3 main.py pay INV-202403-ABC123 --amount 900.00
```

Output:
```
✅ Payment recorded: INV-202403-ABC123
   Amount: $1,800.00
   Status: paid
   Paid date: 2024-03-25
```

---

### `export INV-ID --html`

Exports an invoice as an HTML file, ready to print or convert to PDF.

```bash
python3 main.py export INV-202403-ABC123 --html
```

Output:
```
✅ Invoice exported: INV-202403-ABC123.html
```

---

### `report`

Generates a financial summary report.

```bash
python3 main.py report
python3 main.py report --month 2024-03
```

Output:
```
📊 Financial Report — March 2024

Invoices issued: 6
Total invoiced: $12,400.00
Total collected: $9,100.00
Outstanding: $3,300.00

By client:
  Acme Corp: $6,200.00 invoiced, $4,400.00 collected
  TechStartup: $3,500.00 invoiced, $3,500.00 collected
  Freelance: $2,700.00 invoiced, $1,200.00 collected
```

---

## Use Cases

### 1. Monthly invoicing workflow

Add client → Create invoice with line items → Export HTML → Send to client (manually via email) → Record payment when received.

### 2. Outstanding invoice tracking

```bash
python3 main.py list --status unpaid
```

### 3. End-of-month financial review

```bash
python3 main.py report --month 2024-03
```

---

## Configuration

Data stored at: `~/.smf/invoices/`  
Default currency: USD (configurable)  
Default payment terms: Net 30

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Client not found`
**Fix:** Use the slug (lowercase-hyphenated). Check with `python3 main.py client list`.

### `Invoice not found: INV-XYZ`
**Fix:** IDs are case-sensitive. Use `python3 main.py list` to find exact IDs.

### Amount calculation looks wrong
The skill uses Decimal arithmetic for exact currency math. If you see rounding issues, verify your `--item` amounts use proper decimal notation: `1500.00` not `1500.999`.

---

## FAQ

**Q: Can I convert HTML invoices to PDF?**  
A: Yes — open the HTML file in Chrome, then File → Print → Save as PDF. Or use `wkhtmltopdf invoice.html invoice.pdf`.

**Q: Does it support taxes?**  
A: In the current version, add tax as a separate line item: `--item "Sales Tax (8%):144"`.

**Q: Can I customize invoice styling?**  
A: Edit the HTML template in the skill's source for custom branding.

**Q: What currencies are supported?**  
A: USD is the default. The skill supports formatting for USD, EUR, and GBP.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/invoice-generator)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
