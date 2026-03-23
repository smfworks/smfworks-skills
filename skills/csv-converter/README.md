# CSV Converter

> Convert between CSV, JSON, and Excel formats — and preview CSV contents — without opening a spreadsheet app.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Data

---

## What It Does

CSV Converter is an OpenClaw skill for transforming data files between the three most common tabular formats: CSV, JSON, and Excel (.xlsx). You can convert CSV to JSON for use in web apps, JSON to CSV for spreadsheet editing, CSV to Excel for clients who need .xlsx files, Excel to CSV for data pipelines, and preview a CSV file's headers and first few rows without opening it.

All conversions preserve column names (headers) and handle UTF-8 encoding automatically.

**What it does NOT do:** It does not merge files, filter rows, sort data, handle multi-sheet Excel files (it reads the first/default sheet), clean data, or convert to/from formats like TSV, Parquet, or SQL.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **pandas + openpyxl** — required for Excel operations (installed during setup)
- [ ] **No subscription required** — free tier skill
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/csv-converter
pip install pandas openpyxl
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]
Commands:
  csv-to-json <input.csv> <output.json>
  json-to-csv <input.json> <output.csv>
  csv-to-excel <input.csv> <output.xlsx>
  excel-to-csv <input.xlsx> <output.csv>
  preview <input.csv> [rows]
```

---

## Quick Start

Convert a CSV file to JSON:

```bash
python3 main.py csv-to-json ~/Downloads/contacts.csv ~/Downloads/contacts.json
```

Output:
```
✅ Success: {'success': True, 'rows': 142, 'output': '/home/user/Downloads/contacts.json'}
```

---

## Command Reference

### `csv-to-json`

Converts a CSV file to a JSON array of objects. Each row becomes a JSON object with keys matching the CSV column headers.

**Usage:**
```bash
python3 main.py csv-to-json <input.csv> <output.json>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.csv` | ✅ Yes | CSV file to convert | `contacts.csv` |
| `output.json` | ✅ Yes | JSON file to create | `contacts.json` |

**Example:**
```bash
python3 main.py csv-to-json ~/Data/sales.csv ~/Data/sales.json
```

**Output:**
```
✅ Success: {'success': True, 'rows': 1847, 'output': '/home/user/Data/sales.json'}
```

**What the JSON looks like:**

Input CSV:
```csv
name,email,city
Alice,alice@example.com,New York
Bob,bob@example.com,Chicago
```

Output JSON:
```json
[
  {
    "name": "Alice",
    "email": "alice@example.com",
    "city": "New York"
  },
  {
    "name": "Bob",
    "email": "bob@example.com",
    "city": "Chicago"
  }
]
```

---

### `json-to-csv`

Converts a JSON file to CSV. Accepts either a JSON array of objects (`[{...}, {...}]`) or a single JSON object (`{...}`).

**Usage:**
```bash
python3 main.py json-to-csv <input.json> <output.csv>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.json` | ✅ Yes | JSON file to convert | `users.json` |
| `output.csv` | ✅ Yes | CSV file to create | `users.csv` |

**Example:**
```bash
python3 main.py json-to-csv ~/Data/users.json ~/Data/users.csv
```

**Output:**
```
✅ Success: {'success': True, 'rows': 312, 'columns': 6, 'output': '/home/user/Data/users.csv'}
```

---

### `csv-to-excel`

Converts a CSV file to an Excel (.xlsx) workbook. Requires pandas and openpyxl.

**Usage:**
```bash
python3 main.py csv-to-excel <input.csv> <output.xlsx>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.csv` | ✅ Yes | CSV file to convert | `report.csv` |
| `output.xlsx` | ✅ Yes | Excel file to create | `report.xlsx` |

**Example:**
```bash
python3 main.py csv-to-excel ~/Reports/monthly.csv ~/Reports/monthly.xlsx
```

**Output:**
```
✅ Success: {'success': True, 'rows': 523, 'columns': 8, 'output': '/home/user/Reports/monthly.xlsx'}
```

---

### `excel-to-csv`

Converts an Excel (.xlsx or .xls) file to CSV. Reads the default (first) sheet.

**Usage:**
```bash
python3 main.py excel-to-csv <input.xlsx> <output.csv>
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.xlsx` | ✅ Yes | Excel file to convert | `data.xlsx` |
| `output.csv` | ✅ Yes | CSV file to create | `data.csv` |

**Example:**
```bash
python3 main.py excel-to-csv ~/Downloads/budget.xlsx ~/Downloads/budget.csv
```

**Output:**
```
✅ Success: {'success': True, 'rows': 48, 'columns': 12, 'output': '/home/user/Downloads/budget.csv'}
```

---

### `preview`

Shows the column headers and first N rows of a CSV file without converting it. Useful for quickly checking what's in a file before processing it.

**Usage:**
```bash
python3 main.py preview <input.csv> [rows]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input.csv` | ✅ Yes | CSV file to preview | `customers.csv` |
| `rows` | ❌ No | Number of rows to show. Defaults to 5. | `10` |

**Example:**
```bash
python3 main.py preview ~/Downloads/orders.csv 3
```

**Output:**
```
Headers: ['order_id', 'customer_name', 'product', 'quantity', 'price', 'date']
Preview:
   ['1001', 'Alice Smith', 'Widget A', '3', '29.99', '2024-01-15']
   ['1002', 'Bob Jones', 'Widget B', '1', '49.99', '2024-01-15']
   ['1003', 'Carol White', 'Widget A', '5', '29.99', '2024-01-16']
Total rows: 8472
```

---

## Use Cases

### 1. Convert a CSV export for use in a web app

APIs typically expect JSON. Convert your data export:

```bash
python3 main.py csv-to-json ~/exports/customers-export.csv ~/api-data/customers.json
```

---

### 2. Deliver data to a client who needs Excel

Your data is in CSV but the client wants .xlsx:

```bash
python3 main.py csv-to-excel ~/Reports/q4-results.csv ~/Deliverables/q4-results.xlsx
```

---

### 3. Import Excel data into a script or database

Excel files can't be read by most scripts. Convert to CSV first:

```bash
python3 main.py excel-to-csv ~/Downloads/client-data.xlsx ~/Data/client-data.csv
```

---

### 4. Quickly check what's in an unknown CSV

Before converting a file you received, verify its structure:

```bash
python3 main.py preview ~/Downloads/mystery-data.csv 10
```

---

### 5. Round-trip: Excel → CSV → processed CSV → Excel

```bash
python3 main.py excel-to-csv data.xlsx data.csv
# Process data.csv with other tools (sed, awk, Python scripts)
python3 main.py csv-to-excel processed.csv final-report.xlsx
```

---

## Configuration

No configuration file or environment variables needed.

**Security limits:**
- All file paths must be within your home directory or current working directory
- Path traversal (`../`) is blocked

---

## Troubleshooting

### `pandas not installed. Run: pip install pandas openpyxl`
**Fix:** `pip install pandas openpyxl`

### `File not found: /path/to/file.csv`
**Fix:** Check the path with `ls ~/your-folder/`. Use a full absolute path.

### `No data found in JSON`
The JSON file is either empty or doesn't contain an array or object.  
**Fix:** Verify the JSON is valid with `python3 -c "import json; json.load(open('file.json'))"`. Ensure it contains records, not just metadata.

### `Path outside allowed directories`
You tried to read or write a file outside your home directory.  
**Fix:** Use paths within your home directory (`~/`).

### `UnicodeDecodeError`
The CSV file uses a non-UTF-8 encoding.  
**Fix:** Convert to UTF-8 first: `iconv -f latin1 -t utf-8 input.csv > input-utf8.csv`

### Excel file has multiple sheets — only one converts
`excel-to-csv` reads the default (first) sheet only.  
**Fix:** Open in Excel/LibreOffice and save each sheet as a separate file before converting.

---

## FAQ

**Q: What does the JSON output look like?**  
A: A JSON array where each row is an object. Column headers become JSON keys.

**Q: Can I convert a JSON file that's a single object, not an array?**  
A: Yes — `json-to-csv` handles both a single JSON object `{}` and an array `[{}, {}]`.

**Q: Does it preserve number formatting in Excel?**  
A: Numbers in CSV are stored as text. When converting to Excel via pandas, numeric-looking values are converted to numbers automatically.

**Q: Can I convert an .xls file (old Excel format)?**  
A: Yes — `excel-to-csv` uses pandas which supports both .xls and .xlsx. You may need `pip install xlrd` for old .xls files.

**Q: The preview command shows the total row count — is that accurate?**  
A: Yes — it counts all data rows (excluding the header). For very large files, this may take a second.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| pandas | 1.3 or newer |
| openpyxl | 3.0 or newer |
| OpenClaw | Any version |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/csv-converter)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
