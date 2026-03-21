# Report Generator

Create professional business reports from your data. Supports CSV and JSON input, generates HTML and text output with statistics and formatting.

## Features

- ✅ **Data Import** — Load from CSV or JSON files
- ✅ **Multiple Formats** — HTML (rich) or plain text
- ✅ **Statistics** — Automatic calculations (sum, mean, median, min, max)
- ✅ **Sample Data** — Built-in templates for testing
- ✅ **Interactive** — Step-by-step report creation wizard
- ✅ **Command Line** — Scriptable for automation
- ✅ **Professional Styling** — Clean, modern HTML output

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install report-generator
```

## Quick Start

### Create Your First Report

```bash
# Interactive mode (recommended for first time)
smf run report-generator create
```

Follow the prompts:
1. Provide your data file (CSV or JSON)
2. Or create sample data
3. Choose report title
4. Select format (HTML or text)
5. Done!

### Create from Sample Data

```bash
# Create sample sales data and report
smf run report-generator create --sample sales

# Available samples:
#   sales      — Sales transactions with products
#   customers  — Customer list with order history
#   inventory  — Product inventory with stock levels
```

## Usage

### Interactive Mode

```bash
smf run report-generator create
```

Example session:
```
📊 Report Generator
========================================

Data file (CSV or JSON): ./sales.csv
Report title [Sales Report]: Q1 Sales Report

Format:
  1. HTML (rich formatting, charts, tables)
  2. Text (email or terminal)

Choice [1]: 1

Available columns:
  1. date
  2. product
  3. quantity
  4. price
  5. total

Select column for statistics (or press Enter to skip):
Choice: 5

✅ Report created: /home/user/.smf/reports/report-20260320-143052.html
   Format: html
   Rows: 4
   Size: 3.2 KB

Open the file to view your report!
```

### Command Line Mode

```bash
# Basic report from CSV
smf run report-generator create --data sales.csv

# With custom title
smf run report-generator create --data sales.csv --title "Q1 Sales"

# Text format for email
smf run report-generator create --data data.json --format text

# With statistics on specific column
smf run report-generator create --data sales.csv --value-column total
```

### Sample Data Templates

```bash
# List available templates
smf run report-generator templates

# Create sample and report
smf run report-generator create --sample sales
smf run report-generator create --sample customers
smf run report-generator create --sample inventory
```

## Data Format

### CSV Format

```csv
date,product,quantity,price,total
2026-03-01,Widget A,5,29.99,149.95
2026-03-02,Widget B,3,49.99,149.97
2026-03-03,Widget A,2,29.99,59.98
```

### JSON Format

```json
[
  {"date": "2026-03-01", "product": "Widget A", "quantity": 5, "price": 29.99, "total": 149.95},
  {"date": "2026-03-02", "product": "Widget B", "quantity": 3, "price": 49.99, "total": 149.97}
]
```

Or single object:

```json
{"name": "John", "revenue": 450.00, "orders": 5}
```

## Report Output

### HTML Format

Beautiful, styled reports with:
- Clean header with title and timestamp
- Statistics cards (count, total, mean, median, min, max)
- Sortable data table
- Responsive design
- Professional color scheme

**Location:** `~/.smf/reports/report-YYYYMMDD-HHMMSS.html`

**Open with:**
```bash
# Linux
xdg-open ~/.smf/reports/report-*.html

# macOS
open ~/.smf/reports/report-*.html

# Or simply double-click in file manager
```

### Text Format

Plain text reports perfect for:
- Email body
- Terminal viewing
- Quick sharing
- Log files

**Location:** `~/.smf/reports/report-YYYYMMDD-HHMMSS.txt`

## Statistics

When you specify a numeric column, Report Generator calculates:

| Statistic | Description |
|-----------|-------------|
| Count | Number of rows |
| Total | Sum of all values |
| Mean | Average value |
| Median | Middle value |
| Min | Smallest value |
| Max | Largest value |
| Range | Max - Min |

## Sample Data Templates

### Sales Report

```csv
date,product,quantity,price,total
2026-03-01,Widget A,5,29.99,149.95
2026-03-02,Widget B,3,49.99,149.97
...
```

Perfect for: Revenue tracking, product performance

### Customers

```csv
name,email,orders,revenue
John Smith,john@example.com,5,450.00
Jane Doe,jane@example.com,3,275.50
...
```

Perfect for: Customer analysis, loyalty tracking

### Inventory

```csv
sku,name,stock,cost,price
WID-001,Widget A,45,15.00,29.99
WID-002,Widget B,23,25.00,49.99
...
```

Perfect for: Stock levels, profit margins

## Automation

### Weekly Report Script

Create `~/weekly-report.sh`:

```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

# Generate sales report
smf run report-generator create \
  --data ~/data/weekly-sales.csv \
  --title "Weekly Sales Report" \
  --value-column total

# Email the report (requires mutt or similar)
mutt -s "Weekly Sales Report" manager@example.com \
  -a ~/.smf/reports/report-*.html
```

Make executable:
```bash
chmod +x ~/weekly-report.sh
```

Add to cron:
```bash
crontab -e

# Every Monday at 9 AM
0 9 * * 1 ~/weekly-report.sh
```

### Data Pipeline Integration

```bash
# Export from database, generate report
psql -d myapp -c "COPY (SELECT * FROM sales) TO STDOUT WITH CSV HEADER" > /tmp/sales.csv

smf run report-generator create \
  --data /tmp/sales.csv \
  --title "Sales Report $(date +%Y-%m-%d)"
```

## Report Storage

Default location:
```
~/.smf/reports/
```

Organize by project:
```bash
# Create project directories
mkdir -p ~/.smf/reports/sales
mkdir -p ~/.smf/reports/marketing

# Move reports
mv ~/.smf/reports/report-sales-*.html ~/.smf/reports/sales/
```

## Tips & Tricks

### Clean Data Before Import

```bash
# Remove empty lines from CSV
sed -i '/^$/d' data.csv

# Fix encoding issues
iconv -f ISO-8859-1 -t UTF-8 data.csv > data-utf8.csv
```

### Combine Multiple Files

```bash
# Combine CSV files
cat sales-jan.csv sales-feb.csv > sales-q1.csv

# Generate report
smf run report-generator create --data sales-q1.csv
```

### Export from Spreadsheets

**Google Sheets:**
1. File → Download → CSV

**Excel:**
1. File → Save As → CSV UTF-8

**Numbers:**
1. File → Export To → CSV

## Pricing

**Report Generator is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use spreadsheet software or free CLI tools

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
