# CSV Converter — Quick Reference

## Install
```bash
smfw install csv-converter
```

## Commands
```bash
python main.py convert input.csv output.json     # CSV to JSON
python main.py convert input.json output.csv     # JSON to CSV
python main.py validate file.csv                # Validate CSV
python main.py stats file.csv                   # Get stats
python main.py merge file1.csv file2.csv        # Merge CSVs
```

## Common Examples
```bash
# Convert CSV to JSON
python main.py convert data.csv data.json

# Convert JSON back to CSV
python main.py convert data.json data.csv

# Validate a CSV file
python main.py validate customers.csv

# See column statistics
python main.py stats sales.csv
```

## Help
```bash
python main.py --help
```
