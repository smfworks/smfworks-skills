# Booking Engine — Quick Reference

## Install
```bash
smfw install booking-engine
```

## Commands
```bash
python main.py book [service] [client] [date] [time]  # Book appointment
python main.py list [date]                             # List bookings
python main.py cancel [booking-id]                     # Cancel booking
python main.py services                                # Show services
python main.py availability [date]                     # Check slots
python main.py configure                              # Setup wizard
```

## Common Examples
```bash
# Book a haircut
python main.py book "Haircut" "Jane Doe" "2026-03-25" "10:00"

# List all bookings for a date
python main.py list 2026-03-25

# Check what's available
python main.py availability 2026-03-25

# Cancel a booking
python main.py cancel BOOK-20260325-001
```

## Help
```bash
python main.py --help
python main.py book --help
```
