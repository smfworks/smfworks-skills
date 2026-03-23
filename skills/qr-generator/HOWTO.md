# QR Generator — Quick Reference

## Install
```bash
smfw install qr-generator
```

## Commands
```bash
python main.py url https://smf.works                # URL QR code
python main.py wifi "Network" "password123"         # WiFi QR code
python main.py email hello@example.com              # Email QR
python main.py phone "+1234567890"                  # Phone QR
python main.py vcard "John Doe" "+1234567890"      # Contact card
python main.py sms "+1234567890" "Hello!"          # SMS QR
```

## Common Examples
```bash
# Generate QR code for a website
python main.py url https://smf.works

# WiFi credentials QR
python main.py wifi "MyNetwork" "password123"

# Share contact info
python main.py vcard "Jane Doe" "+15551234567" "jane@email.com"

# Quick SMS
python main.py sms "+15551234567" "Call me!"
```

## Help
```bash
python main.py --help
python main.py url --help
```
