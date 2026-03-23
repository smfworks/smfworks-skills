# CSV Converter — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). pandas and openpyxl installed.

---

## Table of Contents

1. [How to Convert CSV to JSON](#1-how-to-convert-csv-to-json)
2. [How to Convert JSON to CSV](#2-how-to-convert-json-to-csv)
3. [How to Convert CSV to Excel](#3-how-to-convert-csv-to-excel)
4. [How to Convert Excel to CSV](#4-how-to-convert-excel-to-csv)
5. [How to Preview a CSV File](#5-how-to-preview-a-csv-file)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Convert CSV to JSON

**What this does:** Takes a CSV file with headers and converts it to a JSON array of objects.

**When to use it:** A web app or API needs JSON input but your data is in a spreadsheet export.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/csv-converter
```

**Step 2 — Preview the CSV to understand its structure.**

```bash
python3 main.py preview ~/Downloads/customers.csv 3
```

Output:
```
Headers: ['customer_id', 'name', 'email', 'plan', 'signup_date']
Preview:
   ['C001', 'Alice Smith', 'alice@example.com', 'pro', '2024-01-10']
   ['C002', 'Bob Jones', 'bob@example.com', 'free', '2024-01-11']
   ['C003', 'Carol White', 'carol@example.com', 'pro', '2024-01-12']
Total rows: 1,248
```

**Step 3 — Convert to JSON.**

```bash
python3 main.py csv-to-json ~/Downloads/customers.csv ~/Downloads/customers.json
```

Output:
```
✅ Success: {'success': True, 'rows': 1248, 'output': '/home/user/Downloads/customers.json'}
```

**Step 4 — Verify the output.**

```bash
head -20 ~/Downloads/customers.json
```

```json
[
  {
    "customer_id": "C001",
    "name": "Alice Smith",
    "email": "alice@example.com",
    "plan": "pro",
    "signup_date": "2024-01-10"
  },
  ...
]
```

**Result:** A JSON file ready for import into any web app, API, or database script.

---

## 2. How to Convert JSON to CSV

**What this does:** Converts a JSON array of objects to a CSV file, with column headers matching the JSON keys.

**When to use it:** You received data from an API in JSON format and need to open it in Excel or Google Sheets.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/csv-converter
```

**Step 2 — Verify the JSON structure.**

```bash
head -20 ~/Downloads/api-response.json
```

Your JSON should look like an array of objects:
```json
[
  {"id": 1, "name": "Product A", "price": 29.99},
  {"id": 2, "name": "Product B", "price": 49.99}
]
```

**Step 3 — Convert to CSV.**

```bash
python3 main.py json-to-csv ~/Downloads/api-response.json ~/Downloads/products.csv
```

Output:
```
✅ Success: {'success': True, 'rows': 284, 'columns': 6, 'output': '/home/user/Downloads/products.csv'}
```

**Step 4 — Verify the CSV.**

```bash
python3 main.py preview ~/Downloads/products.csv 3
```

**Result:** A CSV file you can open in any spreadsheet application.

---

## 3. How to Convert CSV to Excel

**What this does:** Converts a CSV file to an .xlsx Excel workbook.

**When to use it:** A client or colleague needs an Excel file, not a CSV.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/csv-converter
```

**Step 2 — Convert to Excel.**

```bash
python3 main.py csv-to-excel ~/Reports/monthly-sales.csv ~/Reports/monthly-sales.xlsx
```

Output:
```
✅ Success: {'success': True, 'rows': 523, 'columns': 8, 'output': '/home/user/Reports/monthly-sales.xlsx'}
```

**Step 3 — Verify by opening the file.**

```bash
# On macOS:
open ~/Reports/monthly-sales.xlsx

# On Linux with LibreOffice:
libreoffice ~/Reports/monthly-sales.xlsx
```

**Result:** An Excel workbook with all your CSV data, headers intact, ready to email or deliver.

---

## 4. How to Convert Excel to CSV

**What this does:** Extracts data from the first (default) sheet of an Excel file into a CSV.

**When to use it:** You have data in an Excel file but need to process it with a Python script, database import, or another tool that requires CSV.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/csv-converter
```

**Step 2 — Convert the Excel file.**

```bash
python3 main.py excel-to-csv ~/Downloads/inventory.xlsx ~/Downloads/inventory.csv
```

Output:
```
✅ Success: {'success': True, 'rows': 1024, 'columns': 15, 'output': '/home/user/Downloads/inventory.csv'}
```

**Step 3 — Preview the CSV result.**

```bash
python3 main.py preview ~/Downloads/inventory.csv 5
```

**Result:** A clean CSV you can import into any tool that accepts CSV data.

---

## 5. How to Preview a CSV File

**What this does:** Shows the column headers and first N rows without converting the file or opening a spreadsheet app.

**When to use it:** You received a CSV file and want to understand its structure before processing it.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/csv-converter
```

**Step 2 — Run preview.**

```bash
python3 main.py preview ~/Downloads/unknown-data.csv 10
```

Output:
```
Headers: ['transaction_id', 'date', 'merchant', 'amount', 'category', 'notes']
Preview:
   ['TXN-001', '2024-01-02', 'Amazon', '34.99', 'Shopping', '']
   ['TXN-002', '2024-01-03', 'Uber', '18.50', 'Transport', '']
   ['TXN-003', '2024-01-05', 'Whole Foods', '87.23', 'Groceries', '']
   ...
Total rows: 342
```

**Step 3 — Use the information to plan your next step.**

Now you know it has 342 rows and 6 columns. You can decide whether to convert to JSON, Excel, or process it with another tool.

**Result:** You understand the file's structure in seconds without opening Excel.

---

## 6. Automating with Cron

Schedule automatic conversions — for example, converting a daily CSV export to Excel each morning.

### Open the cron editor

```bash
crontab -e
```

### Example: Convert daily CSV report to Excel every morning at 7 AM

```bash
0 7 * * * python3 /home/yourname/smfworks-skills/skills/csv-converter/main.py csv-to-excel /home/yourname/Reports/daily.csv /home/yourname/Reports/daily-$(date +\%Y-\%m-\%d).xlsx >> /home/yourname/logs/csv-converter.log 2>&1
```

### Example: Convert weekly JSON export to CSV every Monday at 6 AM

```bash
0 6 * * 1 python3 /home/yourname/smfworks-skills/skills/csv-converter/main.py json-to-csv /home/yourname/exports/weekly.json /home/yourname/exports/weekly.csv >> /home/yourname/logs/csv-converter.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 7 * * *` | Every day at 7 AM |
| `0 6 * * 1` | Every Monday at 6 AM |
| `0 8 1 * *` | First day of each month at 8 AM |

### Create the log directory

```bash
mkdir -p ~/logs
```

---

## 7. Combining with Other Skills

**CSV Converter + Report Generator:** Convert raw CSV data to Excel, then generate a formatted report:

```bash
python3 ~/smfworks-skills/skills/csv-converter/main.py csv-to-excel ~/data/raw.csv ~/data/raw.xlsx
python3 ~/smfworks-skills/skills/report-generator/main.py generate ~/data/raw.xlsx
```

**CSV Converter + File Organizer:** Convert files, then organize the outputs:

```bash
python3 ~/smfworks-skills/skills/csv-converter/main.py csv-to-json ~/data/export.csv ~/data/export.json
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-type ~/data/
```

---

## 8. Troubleshooting Common Issues

### `pandas not installed. Run: pip install pandas openpyxl`

The Excel conversion library is missing.  
**Fix:** `pip install pandas openpyxl`

---

### `File not found: /path/to/file`

The input file doesn't exist at the specified path.  
**Fix:** Run `ls ~/your-folder/` to verify. Use full absolute paths.

---

### `No data found in JSON`

The JSON file is empty or doesn't contain records.  
**Fix:** Verify the file is valid JSON containing an array `[...]` or object `{...}`.

---

### Output has garbled characters

The CSV uses a non-UTF-8 encoding.  
**Fix:** Convert encoding first: `iconv -f latin1 -t utf-8 input.csv > input-utf8.csv`

---

### Excel has multiple sheets but only one converted

The skill reads only the first (default) sheet.  
**Fix:** Save each sheet as a separate Excel file, then convert each one separately.

---

## 9. Tips & Best Practices

**Always preview before converting.** Run `preview` on any unknown CSV before conversion to confirm it has the structure you expect. This takes 1 second and can save you from converting the wrong file.

**CSV → JSON preserves values as strings.** Numbers in CSV become string values in JSON (`"42"` not `42`). If you need proper numeric types, post-process the JSON with a script.

**Name outputs with dates when automating.** In cron jobs, include the date in the output filename so you build an archive rather than overwriting the same file: `output-$(date +%Y-%m-%d).xlsx`

**For large files, check disk space first.** Converting a 50,000-row CSV to Excel can produce a file several times larger. Check available disk space with System Monitor before converting large files.

**Use the same directory for input and output unless you have a reason not to.** Keeping converted files next to their source makes them easy to find and clean up.

**For ongoing pipelines, prefer CSV.** CSV is universally supported, human-readable, and version-control friendly. Convert to Excel only for the final deliverable, not as an intermediate format.
