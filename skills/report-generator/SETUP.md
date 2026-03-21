# Report Generator - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Report Generator skill.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [Data Preparation](#data-preparation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Automation](#automation)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Topics](#advanced-topics)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Storage:** Space for reports (typically small, text-based)
- **Browser:** For viewing HTML reports (any modern browser)

### Required Python Packages

```bash
# No additional packages required
# Uses only Python standard library
```

### SMF Works Subscription
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

---

## Installation

### Step 1: Install SMF CLI

If you haven't already:

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

### Step 3: Install Report Generator Skill

```bash
smf install report-generator
```

### Step 4: Verify Installation

```bash
smf run report-generator --help
```

Expected output:
```
📊 Report Generator

Create business reports with charts, tables, and statistics.

Commands:
  create                    Create report (interactive)
  create --data FILE        Create from data file
  templates                 List available templates
  help                      Show this help
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

If you see "Subscription active", you're ready!

---

## Data Preparation

### CSV Format

**Requirements:**
- First row must be headers
- Commas as separators
- UTF-8 encoding recommended

**Example:**
```csv
date,product,quantity,price,total
2026-03-01,Widget A,5,29.99,149.95
2026-03-02,Widget B,3,49.99,149.97
2026-03-03,Widget A,2,29.99,59.98
```

**Creating from Spreadsheet:**

**Google Sheets:**
1. File → Download → Comma Separated Values (.csv)
2. Save to your computer

**Microsoft Excel:**
1. File → Save As
2. Choose "CSV UTF-8" format
3. Save

**Apple Numbers:**
1. File → Export To → CSV
2. Choose UTF-8 encoding
3. Export

### JSON Format

**Array of objects:**
```json
[
  {
    "date": "2026-03-01",
    "product": "Widget A",
    "quantity": 5,
    "price": 29.99,
    "total": 149.95
  },
  {
    "date": "2026-03-02",
    "product": "Widget B",
    "quantity": 3,
    "price": 49.99,
    "total": 149.97
  }
]
```

**Single object (also valid):**
```json
{
  "name": "John Smith",
  "revenue": 450.00,
  "orders": 5
}
```

**Creating JSON:**

From command line:
```bash
# Export from database
psql -d mydb -t -c "SELECT json_agg(sales) FROM sales;" > data.json

# Or convert CSV
csvjson data.csv > data.json  # requires csvkit: pip install csvkit
```

### Data Cleaning

**Remove empty lines:**
```bash
sed -i '/^$/d' data.csv
```

**Fix encoding (Latin-1 to UTF-8):**
```bash
iconv -f ISO-8859-1 -t UTF-8 data.csv > data-utf8.csv
```

**Remove BOM (Byte Order Mark):**
```bash
sed -i '1s/^\xEF\xBB\xBF//' data.csv
```

**Quote handling:**
```bash
# Ensure proper quoting
# Good: "John Smith",25,"New York, NY"
# Bad: John Smith,25,New York, NY
```

---

## Configuration

### Report Storage Location

Default location:
```
~/.smf/reports/
```

To change, specify output path:
```bash
smf run report-generator create --data data.csv
# Then move manually or use --output (future feature)
```

### Organizing Reports

Create subdirectories:
```bash
mkdir -p ~/.smf/reports/sales
mkdir -p ~/.smf/reports/marketing
mkdir -p ~/.smf/reports/monthly

# Move reports after generation
mv ~/.smf/reports/report-sales-*.html ~/.smf/reports/sales/
```

### Custom Templates (Advanced)

Currently, Report Generator uses built-in templates. Custom templates coming in future versions.

**Current templates:**
- sales-report
- monthly-summary
- customer-list
- inventory-report
- financial-summary

---

## Usage

### Creating Your First Report

**Interactive Mode (Recommended):**
```bash
smf run report-generator create
```

Step-by-step:
1. **Data file:** Enter path to your CSV or JSON file
   - If file doesn't exist, you'll be asked to create sample data
2. **Report title:** Enter a descriptive title
   - Default: "Report"
3. **Format:** Choose 1 for HTML or 2 for text
   - HTML: Rich formatting, best for viewing
   - Text: Plain text, best for email
4. **Statistics column:** Select a numeric column for statistics
   - Or press Enter to skip
5. **Done!** Report is generated and saved

**Example Session:**
```
📊 Report Generator
========================================

Data file (CSV or JSON): ./sales.csv
Report title [Report]: Q1 Sales Report

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
   Rows: 100
   Size: 12.5 KB

Open the file to view your report!
```

### Using Sample Data

**Quick test without your own data:**

```bash
# Create sample and report in one command
smf run report-generator create --sample sales

# Available samples:
#   sales      - Sales transactions
#   customers  - Customer records
#   inventory  - Product inventory
```

This creates:
- Sample CSV file (e.g., `sample-sales.csv`)
- Report from that data

### Command Line Arguments

**Basic usage:**
```bash
smf run report-generator create --data file.csv
```

**With options:**
```bash
smf run report-generator create \
  --data sales.csv \
  --title "Q1 Sales Report" \
  --format html \
  --value-column total
```

**Available options:**

| Option | Description | Example |
|--------|-------------|---------|
| `--data FILE` | Input data file (CSV or JSON) | `--data sales.csv` |
| `--title TITLE` | Report title | `--title "Sales Report"` |
| `--format FORMAT` | Output format (html or text) | `--format html` |
| `--value-column COL` | Column for statistics | `--value-column revenue` |
| `--sample TYPE` | Create sample data | `--sample sales` |

### Viewing HTML Reports

**Linux:**
```bash
xdg-open ~/.smf/reports/report-20260320-143052.html
```

**macOS:**
```bash
open ~/.smf/reports/report-20260320-143052.html
```

**Windows:**
```cmd
start %USERPROFILE%\.smf\reports\report-20260320-143052.html
```

**Or manually:**
- Open file manager
- Navigate to `~/.smf/reports/`
- Double-click HTML file

### Understanding Report Statistics

When you specify a numeric column, the report includes:

| Statistic | What It Means | Example |
|-----------|---------------|---------|
| **Count** | Number of data rows | 100 transactions |
| **Total** | Sum of all values | $10,450.00 total revenue |
| **Mean** | Average value | $104.50 average per transaction |
| **Median** | Middle value | $98.50 (half above, half below) |
| **Min** | Smallest value | $15.00 minimum |
| **Max** | Largest value | $599.00 maximum |
| **Range** | Spread (Max - Min) | $584.00 spread |

---

## Automation

### Weekly Report by Email

**Create script** `~/email-report.sh`:
```bash
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

# Generate report
smf run report-generator create \
  --data ~/data/weekly-sales.csv \
  --title "Weekly Sales Report - $(date +%Y-%m-%d)" \
  --format html \
  --value-column total

# Get latest report
REPORT=$(ls -t ~/.smf/reports/report-*.html | head -1)

# Email using mutt
mutt -s "Weekly Sales Report" \
     -a "$REPORT" \
     -- manager@example.com <<EOF
Weekly sales report attached.

Generated: $(date)
EOF
```

Make executable:
```bash
chmod +x ~/email-report.sh
```

Add to cron (Mondays at 9 AM):
```bash
crontab -e
```

Add:
```
0 9 * * 1 ~/email-report.sh
```

### Database to Report Pipeline

**PostgreSQL:**
```bash
#!/bin/bash
# Export and report

# Query to CSV
psql -d myapp -c "
  COPY (
    SELECT date, product, quantity, price, total
    FROM sales
    WHERE date >= CURRENT_DATE - INTERVAL '7 days'
  ) TO STDOUT WITH CSV HEADER
" > /tmp/weekly-sales.csv

# Generate report
smf run report-generator create \
  --data /tmp/weekly-sales.csv \
  --title "Weekly Sales Report"

# Cleanup
rm /tmp/weekly-sales.csv
```

**MySQL:**
```bash
#!/bin/bash

# Export to CSV
mysql -u user -p mydb -e "
  SELECT date, product, quantity, price, total
  FROM sales
  WHERE date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
  INTO OUTFILE '/tmp/weekly-sales.csv'
  FIELDS TERMINATED BY ','
  ENCLOSED BY '\"'
  LINES TERMINATED BY '\n'
"

# Generate report
smf run report-generator create \
  --data /tmp/weekly-sales.csv \
  --title "Weekly Sales"
```

### Monthly Report with Systemd

**Service file** `~/.config/systemd/user/monthly-report.service`:
```ini
[Unit]
Description=Monthly Sales Report

[Service]
Type=oneshot
ExecStart=/home/user/.local/bin/smf run report-generator create --data /home/user/data/monthly.csv --title "Monthly Report"
StandardOutput=append:/home/user/.smf/report.log
StandardError=append:/home/user/.smf/report.log
```

**Timer file** `~/.config/systemd/user/monthly-report.timer`:
```ini
[Unit]
Description=Monthly Report on 1st at 8 AM

[Timer]
OnCalendar=*-*-01 08:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

**Enable:**
```bash
systemctl --user daemon-reload
systemctl --user enable monthly-report.timer
systemctl --user start monthly-report.timer
```

---

## Troubleshooting

### "No subscription token found"

**Problem:** Not authenticated

**Solution:**
```bash
smf login
```

### "File not found: data.csv"

**Problem:** Path incorrect or file doesn't exist

**Solution:**
```bash
# Check file exists
ls -la data.csv

# Use absolute path
smf run report-generator create --data /home/user/data/sales.csv

# Or navigate to directory first
cd ~/data
smf run report-generator create --data sales.csv
```

### "No data found in file"

**Problem:** Empty file or wrong format

**Solution:**
```bash
# Check file contents
head data.csv

# Verify CSV format (should have headers)
cat data.csv | head -3

# Check for encoding issues
file data.csv

# Fix encoding if needed
iconv -f ISO-8859-1 -t UTF-8 data.csv > data-fixed.csv
```

### "UnicodeDecodeError"

**Problem:** File encoding issue

**Solution:**
```bash
# Check encoding
file data.csv

# Convert to UTF-8
iconv -f LATIN1 -t UTF-8 data.csv > data-utf8.csv

# Or use sed to remove BOM
sed -i '1s/^\xEF\xBB\xBF//' data.csv
```

### Statistics not calculating

**Problem:** Column contains non-numeric data

**Solution:**
```bash
# Check data types
head data.csv

# Ensure numeric column has no text/symbols
# Bad: $100.00, N/A, ""
# Good: 100.00, 0, 50.5

# Clean with sed
sed -i 's/[$,]//g' data.csv
```

### HTML report opens as text

**Problem:** Browser association or file extension

**Solution:**
```bash
# Verify file extension
ls ~/.smf/reports/*.html

# Open explicitly with browser
firefox ~/.smf/reports/report-*.html
# or
chrome ~/.smf/reports/report-*.html
```

### Reports directory not found

**Problem:** Directory doesn't exist

**Solution:**
```bash
# Create directory
mkdir -p ~/.smf/reports

# Or let skill create it (happens automatically)
smf run report-generator create --sample sales
```

---

## Advanced Topics

### Combining Multiple Data Files

**Merge CSVs:**
```bash
# Combine all monthly reports
cat sales-01.csv sales-02.csv sales-03.csv > sales-q1.csv

# Remove duplicate headers
awk 'NR==1 || FNR>1' sales-*.csv > sales-combined.csv

# Generate report
smf run report-generator create --data sales-combined.csv
```

### Transforming Data

**Using Python for complex transforms:**
```python
import pandas as pd

# Load data
df = pd.read_csv('raw-data.csv')

# Transform
df['total'] = df['quantity'] * df['price']
df['month'] = pd.to_datetime(df['date']).dt.to_period('M')

# Aggregate
monthly = df.groupby('month').agg({
    'total': 'sum',
    'quantity': 'sum'
}).reset_index()

# Save
monthly.to_csv('transformed.csv', index=False)
```

Then:
```bash
smf run report-generator create --data transformed.csv
```

### Custom Styling (Advanced)

Reports use inline CSS. To customize, edit the HTML after generation:

```bash
# Generate report
smf run report-generator create --data data.csv

# Get latest report
REPORT=$(ls -t ~/.smf/reports/*.html | head -1)

# Edit with sed or manually
cp "$REPORT" my-report.html
# Edit my-report.html in your editor
```

---

## Next Steps

1. **Prepare your data** — Export from your systems
2. **Test with samples** — Verify everything works
3. **Generate first report** — See your data visualized
4. **Automate** — Set up scheduled reports
5. **Customize** — Adjust for your needs

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
