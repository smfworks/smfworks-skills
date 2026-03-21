# CSV Converter

A data conversion skill for OpenClaw. Convert between CSV, JSON, and Excel formats.

## Features

- **CSV ↔ JSON**: Convert between CSV and JSON formats
- **CSV ↔ Excel**: Convert between CSV and Excel (.xlsx)
- **Data Preview**: Preview CSV contents before conversion
- **Path Security**: Validates paths to prevent directory traversal

## Installation

```bash
# For Excel support
pip install pandas openpyxl
```

## Usage

### CSV to JSON
```bash
python main.py csv-to-json input.csv output.json
```

### JSON to CSV
```bash
python main.py json-to-csv input.json output.csv
```

### CSV to Excel
```bash
python main.py csv-to-excel input.csv output.xlsx
```

### Excel to CSV
```bash
python main.py excel-to-csv input.xlsx output.csv
```

### Preview CSV
```bash
python main.py preview input.csv
python main.py preview input.csv 10  # Preview 10 rows
```

## Input Validation Limits

| Parameter | Limit |
|-----------|-------|
| File size | Limited by available memory |
| Path traversal | Blocked (paths outside working directory rejected) |
| File types | CSV, JSON, XLSX only |

## Security Considerations

- **Path Traversal Protection**: Resolves and validates all paths to prevent directory escape
- **Restricted Directories**: Only allows access within current working directory or home directory
- **Suspicious Pattern Detection**: Rejects paths containing `..` sequences
- **File Validation**: Checks file existence before operations

## Error Handling

Errors are categorized by type:
- **FileNotFoundError**: Input file doesn't exist
- **PermissionError**: Insufficient file permissions
- **ValueError**: Invalid paths or data
- **ImportError**: Missing required dependencies

## Known Limitations

- Large files may require significant memory
- Excel conversion requires pandas and openpyxl dependencies
- JSON arrays must have consistent keys for CSV conversion
- Binary/invalid UTF-8 files are not supported

## Examples

```bash
# Convert customer data
python main.py csv-to-json customers.csv customers.json

# Convert to Excel for reporting
python main.py csv-to-excel sales.csv sales.xlsx

# Preview data before conversion
python main.py preview large_file.csv 5
```
