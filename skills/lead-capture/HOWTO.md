# Lead Capture — Quick Reference

## Install
```bash
smfw install lead-capture
```

## Commands
```bash
python main.py capture --name "John" --email "john@email.com" --phone "555-1234"   # Capture lead
python main.py list                                              # List all leads
python main.py export --format csv                              # Export leads
python main.py search "keyword"                                 # Search leads
python main.py score                                           # Score leads
```

## Common Examples
```bash
# Capture a new lead from a website form
python main.py capture --name "Jane Doe" --email "jane@company.com"

# List all leads with scores
python main.py list

# Export leads to CSV
python main.py export --format csv --output leads.csv

# Find leads by keyword
python main.py search "consulting"
```

## Help
```bash
python main.py --help
python main.py capture --help
```
