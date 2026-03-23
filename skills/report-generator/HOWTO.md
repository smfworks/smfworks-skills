# Report Generator — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. pandas installed. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Create a Report from CSV Data](#1-how-to-create-a-report-from-csv-data)
2. [How to Create a Report from JSON Data](#2-how-to-create-a-report-from-json-data)
3. [How to Generate a Text Report for Email](#3-how-to-generate-a-text-report-for-email)
4. [How to Use Sample Data for Testing](#4-how-to-use-sample-data-for-testing)
5. [How to View Available Templates](#5-how-to-view-available-templates)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Create a Report from CSV Data

**What this does:** Reads a CSV file, detects column types, calculates statistics, and generates a formatted HTML report.

**When to use it:** You have a CSV export from your CRM, sales tool, or spreadsheet and want a professional-looking report.

### Steps

**Step 1 — Preview your CSV first (optional but recommended).**

```bash
python3 ~/smfworks-skills/skills/csv-converter/main.py preview ~/Data/monthly-sales.csv 5
```

```
Headers: ['date', 'rep', 'product', 'quantity', 'revenue']
Total rows: 523
```

**Step 2 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/report-generator
```

**Step 3 — Create the report.**

```bash
python3 main.py create --data ~/Data/monthly-sales.csv --title "March 2024 Sales Report"
```

Output:
```
✅ Report generated: march-2024-sales-report.html
   Rows: 523
   Columns: 5
   Format: HTML
```

**Step 4 — Open the report in your browser.**

```bash
# macOS:
open march-2024-sales-report.html

# Linux:
xdg-open march-2024-sales-report.html
```

**Result:** A formatted HTML report with summary statistics, data table, and charts for numeric columns.

---

## 2. How to Create a Report from JSON Data

**When to use it:** Your data is in JSON format from an API or script output.

```bash
python3 main.py create --data ~/Data/customers.json --title "Customer Analysis Q1"
```

The JSON file should be a top-level array of objects:
```json
[
  {"name": "Acme Corp", "revenue": 15000, "plan": "pro"},
  {"name": "TechCo", "revenue": 8500, "plan": "free"}
]
```

---

## 3. How to Generate a Text Report for Email

**When to use it:** You need to paste or email a report as plain text (no HTML rendering).

```bash
python3 main.py create --data ~/Data/inventory.csv --format text --title "March Inventory Report"
```

Output file is a `.txt` file. Contents:
```
March Inventory Report
Generated: 2024-03-15 09:00

Summary:
  Items: 284
  Total Value: $847,234.00
  Average Price: $2,983.92

  Product      | Quantity | Unit Price | Total Value
  ─────────────────────────────────────────────────
  Widget A     | 142      | $29.99     | $4,258.58
  Widget B     | 87       | $49.99     | $4,349.13
  ...
```

---

## 4. How to Use Sample Data for Testing

**When to use it:** Demonstrating the skill to someone, testing templates, or learning the output format.

Available sample types: `sales`, `customers`, `inventory`

```bash
python3 main.py create --sample sales
python3 main.py create --sample customers
python3 main.py create --sample inventory
```

Each generates a realistic demo report from built-in data.

---

## 5. How to View Available Templates

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

Templates affect the report layout, chart types, and which statistics are emphasized.

---

## 6. Automating with Cron

### Open crontab

```bash
crontab -e
```

### Example: Generate weekly sales report every Monday at 8 AM

```bash
0 8 * * 1 python3 /home/yourname/smfworks-skills/skills/report-generator/main.py create --data /home/yourname/Data/weekly-sales.csv --title "Weekly Sales $(date +\%Y-W\%V)" >> /home/yourname/logs/report-generator.log 2>&1
```

### Example: Monthly inventory report on the 1st at 6 AM

```bash
0 6 1 * * python3 /home/yourname/smfworks-skills/skills/report-generator/main.py create --data /home/yourname/Data/inventory.csv --title "Inventory $(date +\%B\ \%Y)" --format text >> /home/yourname/logs/report-generator.log 2>&1
```

---

## 7. Combining with Other Skills

**Report Generator + CSV Converter:** Convert Excel to CSV, then generate report:

```bash
python3 ~/smfworks-skills/skills/csv-converter/main.py excel-to-csv ~/Data/budget.xlsx ~/Data/budget.csv
python3 ~/smfworks-skills/skills/report-generator/main.py create --data ~/Data/budget.csv --title "Q1 Budget"
```

**Report Generator + Email Campaign:** Generate a report, then include it in a campaign:

```bash
python3 main.py create --data ~/Data/sales.csv --format text --title "Monthly Report" > /tmp/report.txt
# Reference the report content in your email campaign
```

---

## 8. Troubleshooting Common Issues

### `File not found: data.csv`

**Fix:** Use an absolute path: `--data /home/yourname/Data/sales.csv`

### `pandas not installed`

**Fix:** `pip install pandas`

### HTML report shows raw HTML in browser (doesn't render)

**Fix:** You're opening the file with a text editor. Use a web browser: `open report.html` (macOS) or `xdg-open report.html` (Linux).

### `--value-column 'revenue' not found`

**Fix:** Column name must match exactly. Check headers with: `python3 ~/smfworks-skills/skills/csv-converter/main.py preview data.csv`

### Report has too many columns and looks cramped

**Fix:** For wide datasets, use `--format text` for a cleaner, linearized view.

---

## 9. Tips & Best Practices

**Preview your CSV before generating a report.** Running `csv-converter preview` on your data first confirms the column names are correct, saving you from a failed report generation.

**Use the `--title` flag for meaningful report names.** A title like "Q1 2024 Sales Analysis" makes the report file identifiable — especially useful when generating reports via cron.

**Use `--format text` for reports that will be emailed.** HTML reports look great in a browser but email clients render HTML unpredictably. Plain text is safe for email content.

**The `--value-column` option improves chart quality.** If your data has a primary numeric metric (revenue, quantity, score), specifying it with `--value-column` ensures the report charts focus on that metric.

**For large datasets, use `--format text`.** HTML reports with tens of thousands of rows can be slow to load in a browser. Text format generates faster and is more practical for large datasets.
