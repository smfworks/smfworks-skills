# Email Campaign — Quick Reference

## Install
```bash
smfw install email-campaign
```

## Commands
```bash
python main.py send --list contacts.csv --template template.html   # Send campaign
python main.py preview --template template.html                     # Preview email
python main.py validate --list contacts.csv                         # Validate contacts
python main.py stats                                                # Show campaign stats
python main.py schedule --template template.html --list contacts.csv --time "2026-03-25 10:00"
```

## Common Examples
```bash
# Send an email campaign
python main.py send --list contacts.csv --template newsletter.html

# Preview before sending
python main.py preview --template newsletter.html

# Validate your contact list
python main.py validate --list contacts.csv

# Schedule a campaign for later
python main.py schedule --template newsletter.html --list contacts.csv --time "2026-03-25 10:00"
```

## Help
```bash
python main.py --help
python main.py send --help
```
