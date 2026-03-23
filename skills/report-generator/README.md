# Report Generator

> Turn CSV or JSON data into formatted HTML or text business reports — with charts, tables, statistics, and multiple templates.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Business / Reporting

---

## What It Does

Report Generator is an OpenClaw Pro skill that converts tabular data (CSV or JSON) into professionally formatted reports. It automatically detects column types (numeric, currency, date, text), calculates statistics, and produces styled HTML or plain text output.

Generate reports interactively, from a data file, or from built-in sample data for testing.

**What it does NOT do:** It does not connect to databases directly, send reports by email, generate charts as image files (charts are HTML/SVG inline), or export to PDF.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**
- [ ] **pandas** Python package (for CSV/JSON reading)

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/report-generator
pip install pandas
python3 main.py help
```

---

## Quick Start

Generate a sample sales report:

```bash
python3 main.py create --sample sales
```

Output:
```
✅ Report generated: sales-report-2024-03-15.html
   Rows: 120
   Columns: 6
   Format: HTML
   Template: sales
```

Open the file in your browser to view the formatted report.

---

## Command Reference

### `create`

Creates a report. Can be used interactively (no arguments), from a data file, or from sample data.

**Usage:**
```bash
python3 main.py create                             # Interactive mode
python3 main.py create --data FILE                 # From data file
python3 main.py create --sample TYPE              # From sample data
python3 main.py create --data FILE --title "Title"  # With custom title
python3 main.py create --data FILE --format text    # Plain text output
python3 main.py create --data FILE --value-column revenue  # Specify value column
```

**Arguments:**

| Option | Description | Example |
|--------|-------------|---------|
| `--data FILE` | Input CSV or JSON file | `--data sales.csv` |
| `--sample TYPE` | Generate from built-in sample: `sales`, `customers`, `inventory` | `--sample sales` |
| `--title TEXT` | Report title | `--title "Q1 Sales Report"` |
| `--format` | Output format: `html` (default) or `text` | `--format text` |
| `--value-column COL` | Column to use as the primary value metric | `--value-column revenue` |

**Example — from CSV file:**
```bash
python3 main.py create --data ~/Data/monthly-sales.csv --title "March Sales Report"
```

Output:
```
✅ Report generated: march-sales-report-2024-03-15.html
   Rows: 523
   Columns: 8
   Format: HTML
   Template: default
```

**Example — plain text format:**
```bash
python3 main.py create --data ~/Data/inventory.csv --format text --title "Inventory Report"
```

Output:
```
✅ Report generated: inventory-report-2024-03-15.txt
   Rows: 284
   Format: text
```

---

### `templates`

Lists available report templates.

```bash
python3 main.py templates
```

Output:
```
Available Templates:
  • default   — General purpose data report
  • sales     — Revenue-focused with trend analysis
  • customers — Customer data with segmentation
  • inventory — Stock levels and valuation
```

---

### `create --sample TYPE`

Generates a report from built-in sample data. Great for testing and demonstrations.

Available sample types: `sales`, `customers`, `inventory`

```bash
python3 main.py create --sample customers
```

Output:
```
✅ Report generated: customers-report-2024-03-15.html
   Rows: 150
   Format: HTML
```

---

## Use Cases

### 1. Weekly sales report

```bash
python3 main.py create --data ~/Reports/weekly-sales.csv --title "Week 12 Sales Report"
```

### 2. Monthly inventory report in plain text for email

```bash
python3 main.py create --data ~/Data/inventory.csv --format text --title "March Inventory"
```

### 3. Customer analysis report

```bash
python3 main.py create --data ~/Data/customers.csv --title "Q1 Customer Analysis" --value-column revenue
```

### 4. Demonstrate report format to a client

```bash
python3 main.py create --sample sales
# Open the HTML file in a browser
```

### 5. Automated weekly report via cron

Schedule weekly report generation — see HOWTO.md for the full cron setup.

---

## Report Structure

Every generated HTML report includes:
- **Header:** Title, generation date, row/column counts
- **Summary statistics:** Min, max, average, total for numeric columns
- **Data table:** Sortable, with formatting based on detected column type
- **Charts:** Inline SVG bar charts for key numeric columns (HTML format only)
- **Footer:** Generation timestamp

Text reports include the header, statistics, and a formatted data table.

---

## Supported Data Formats

| Format | Extensions | Notes |
|--------|------------|-------|
| CSV | `.csv` | Standard comma-separated values |
| JSON | `.json` | Array of objects format |

Column type detection:
- **Numeric:** Automatic statistics (min/max/avg/total)
- **Currency:** Formatted with `$` and thousands separator
- **Date:** Formatted in human-readable form
- **Text:** Shown as-is

---

## Configuration

No configuration file needed. All options are passed as command arguments.

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `pandas not installed`
**Fix:** `pip install pandas`

### `File not found: data.csv`
**Fix:** Check the file path. Use absolute paths: `~/Data/file.csv`

### Report HTML looks unstyled
**Fix:** Open the HTML file in a web browser, not a text editor.

### `--value-column 'revenue' not found`
**Fix:** Check exact column names in your data: `python3 ~/smfworks-skills/skills/csv-converter/main.py preview data.csv`

---

## FAQ

**Q: Can I customize the report template/styling?**  
A: The templates have built-in styling. For custom templates, edit the template files in the skill's `templates/` directory.

**Q: How do I generate a PDF?**  
A: The skill generates HTML. To convert to PDF: open the HTML file in Chrome, then File → Print → Save as PDF.

**Q: Does it support multi-sheet Excel?**  
A: Use CSV Converter to convert Excel to CSV first, then pass the CSV to Report Generator.

**Q: What's the maximum file size?**  
A: Limited by available RAM. Files with 100,000+ rows may be slow.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| pandas | 1.3 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| External APIs | None |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/report-generator)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
