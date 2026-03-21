# Lead Capture System

Capture, qualify, and manage sales leads for small businesses.

## Features

- ✅ Interactive lead capture
- ✅ Automatic lead scoring (0-100)
- ✅ Status classification (Hot/Warm/Cold/Dormant)
- ✅ JSON/CSV export
- ✅ Lead statistics and analytics
- ✅ Local storage (private, no cloud)

## Usage

```bash
# Capture a new lead (interactive)
python main.py capture

# List all leads
python main.py list
python main.py list 10  # Limit to 10

# Export leads
python main.py export csv
python main.py export json

# Show statistics
python main.py stats
```

## Lead Scoring

Leads are automatically scored based on:

| Factor | Points |
|--------|--------|
| Email provided | 20 |
| Phone provided | 20 |
| Company name | 15 |
| Title/role | 10 |
| Budget: small/medium/large | 10/20/30 |
| Timeline: immediate/1mo/3mo/6mo | 30/20/10/5 |

**Status Thresholds:**
- 🔥 Hot: 80-100 points
- 🌡️ Warm: 60-79 points
- ❄️ Cold: 40-59 points
- 💤 Dormant: 0-39 points

## Data Storage

Leads are stored locally in `~/.smf/leads/` as JSON files:
- Private: Data never leaves your machine
- Portable: Easy to backup or migrate
- Standard format: JSON for easy integration

## Lead Schema

```json
{
  "id": "lead-20260320-143052",
  "captured_at": "2026-03-20T14:30:52",
  "status": "new",
  "name": "John Smith",
  "email": "john@example.com",
  "phone": "555-1234",
  "company": "Acme Corp",
  "title": "CEO",
  "budget": "medium",
  "timeline": "1-month",
  "source": "website",
  "notes": "Interested in AI automation",
  "score": 85
}
```

## Export Format

### CSV Export
```csv
id,name,email,phone,company,score,captured_at
lead-20260320-143052,John Smith,john@example.com,...,Acme Corp,85,2026-03-20T14:30:52
```

### JSON Export
```json
[
  {
    "id": "lead-20260320-143052",
    "name": "John Smith",
    ...
  }
]
```

## Subscription

**Lead Capture System is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, future updates, priority support
- **Free alternative:** Use the 5 free skills (File Organizer, PDF Toolkit, QR Generator, Text Formatter, System Info)

Subscribe at https://smf.works/subscribe

## Setup & Configuration

**New users:** See [SETUP.md](./SETUP.md) for complete installation and configuration instructions.

### Quick Setup

```bash
# 1. Subscribe at https://smf.works/subscribe
# 2. Login
python ../../cli/smf_login.py login
# 3. Start capturing leads
python main.py capture
```

## Documentation

- [SETUP.md](./SETUP.md) - Complete setup, configuration, and troubleshooting guide
- [AUTH_SYSTEM.md](../../docs/AUTH_SYSTEM.md) - Authentication system documentation

## License

SMF Works Pro Skill - See SMF Works Terms of Service
