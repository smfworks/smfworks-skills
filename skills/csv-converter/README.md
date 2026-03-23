# CSV Converter

> Convert between CSV and JSON formats with validation and data cleaning

---

## What It Does

CSV Converter transforms your data between CSV and JSON formats — the two most common data interchange formats. It automatically detects headers, handles edge cases like quoted fields and escaped characters, and can clean up messy data while converting.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install csv-converter
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Convert a CSV file to JSON in one command:

```bash
python main.py convert data.csv data.json
```

---

## Commands

### `convert`

**What it does:** Convert files between CSV and JSON formats.

**Usage:**
```bash
python main.py convert [input-file] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `input-file` | ✅ Yes | Source file to convert | `data.csv` |
| `output-file` | ✅ Yes | Destination file | `data.json` |

**Example:**
```bash
python main.py convert data.csv data.json
python main.py convert data.json data.csv
```

**Output:**
```
✅ Converted: data.csv → data.json
   Rows: 150
   Columns: 8
   Output: 45.2 KB
```

---

### `validate`

**What it does:** Check a CSV file for common issues like malformed rows or missing headers.

**Usage:**
```bash
python main.py validate [file.csv]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `file.csv` | ✅ Yes | CSV file to validate | `customers.csv` |

**Example:**
```bash
python main.py validate customers.csv
```

**Output:**
```
✅ Validation passed!
   Rows: 150
   Columns: 8
   Headers: name, email, phone, address, city, state, zip, country
   No errors found.
```

---

### `stats`

**What it does:** Show statistics and column information for a CSV file.

**Usage:**
```bash
python main.py stats [file.csv]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `file.csv` | ✅ Yes | CSV file to analyze | `sales.csv` |

**Example:**
```bash
python main.py stats sales.csv
```

**Output:**
```
📊 CSV Statistics for sales.csv:
   Total rows: 1,523
   Columns: 6
   Headers: date, product, quantity, price, total, customer
   
   Column Types:
   - date: date (100% filled)
   - product: text (100% filled)
   - quantity: numeric (100% filled)
   - price: currency (100% filled)
   - total: currency (100% filled)
   - customer: text (95% filled, 5% empty)
```

---

### `merge`

**What it does:** Combine multiple CSV files with the same headers into one.

**Usage:**
```bash
python main.py merge [file1.csv] [file2.csv] [output.csv]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `file1.csv` | ✅ Yes | First CSV file | `january.csv` |
| `file2.csv` | ✅ Yes | Second CSV file | `february.csv` |
| `output.csv` | ✅ Yes | Merged output file | `q1.csv` |

**Example:**
```bash
python main.py merge january.csv february.csv q1.csv
```

---

## Use Cases

- **Data migration:** Convert legacy CSV exports to JSON for modern APIs
- **API prep:** Transform CSV spreadsheets into JSON for API payloads
- **Backup:** Convert JSON to CSV for spreadsheet backup
- **Merging:** Combine multiple CSV exports into one report
- **Validation:** Check CSV quality before importing into a database

---

## Tips & Tricks

- Use `--dry-run` flag to preview conversion without writing output
- For large files, conversion happens in chunks to save memory
- Auto-detects delimiter (comma, semicolon, tab) in CSV files
- Handles quoted fields with embedded commas correctly

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Mismatched columns" | Ensure both CSV files have the same headers |
| "Encoding error" | Convert file to UTF-8 before converting |
| "Empty output" | Check that input file has content and valid format |
| "Memory error on large file" | Process in smaller chunks or use command line tools directly |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies (uses built-in `csv` and `json` modules)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/csv-converter)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
