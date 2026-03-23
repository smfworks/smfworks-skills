# CSV Converter — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Free — no subscription, no API keys required

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| pip | Python package manager | Free |
| pandas | Data analysis library | Free |
| openpyxl | Excel file library | Free |
| smfworks-skills repository | Cloned via git | Free |

The `pandas` and `openpyxl` packages are only needed for Excel operations. CSV ↔ JSON conversions work with Python's stdlib (no packages needed), but install them both to use all features.

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.9.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Install Required Packages

```bash
pip install pandas openpyxl
```

Expected output:
```
Collecting pandas
  Downloading pandas-2.1.4-cp311-cp311-linux_x86_64.whl (11.3 MB)
Collecting openpyxl
  Downloading openpyxl-3.1.2-py2.py3-none-any.whl (249 kB)
Installing collected packages: openpyxl, pandas
Successfully installed openpyxl-3.1.2 pandas-2.1.4
```

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/csv-converter
```

---

## Step 5 — Verify

```bash
python3 main.py
```

Expected:
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

## Verify Your Setup

Create a quick test CSV and convert it:

```bash
echo "name,age,city
Alice,30,New York
Bob,25,Chicago" > /tmp/test.csv

python3 main.py csv-to-json /tmp/test.csv /tmp/test.json
cat /tmp/test.json
```

Expected output:
```
✅ Success: {'success': True, 'rows': 2, 'output': '/tmp/test.json'}
[
  {
    "name": "Alice",
    "age": "30",
    "city": "New York"
  },
  {
    "name": "Bob",
    "age": "25",
    "city": "Chicago"
  }
]
```

If you see the JSON array, setup is complete.

Clean up:
```bash
rm /tmp/test.csv /tmp/test.json
```

---

## Configuration Options

No configuration file or environment variables needed.

---

## Troubleshooting

**`pandas not installed`** — Run `pip install pandas openpyxl`.

**`pip: command not found`** — Try `pip3` or `python3 -m pip install pandas openpyxl`.

**Old Excel format (.xls) fails** — Install xlrd: `pip install xlrd`

---

## Next Steps

Setup complete. See **HOWTO.md** for conversion walkthroughs and cron automation examples.
