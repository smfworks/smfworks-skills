# Lead Capture System - Setup & Configuration Guide

Complete setup instructions for installing, configuring, and using the Lead Capture System.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Authentication Setup](#authentication-setup)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [Data Backup](#data-backup)

---

## Prerequisites

### System Requirements
- **OS:** Linux, macOS, or Windows with Python
- **Python:** 3.8 or higher
- **Storage:** ~10MB for skill + data

### Required Python Packages
```bash
# No additional packages required
# Uses only Python standard library
```

### SMF Works Subscription
- **Required:** SMF Works Pro subscription ($19.99/mo)
- **Sign up:** https://smf.works/subscribe

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/smfworks/smfworks-skills.git
cd smfworks-skills/skills/lead-capture
```

### Step 2: Verify Installation
```bash
python3 main.py --help
```

Expected output:
```
Usage: python main.py <command> [options]

Commands:
  capture              - Capture a new lead (interactive)
  list [limit]         - List all leads
  export [csv|json]    - Export leads to file
  stats                - Show lead statistics
```

---

## Authentication Setup

### Step 1: Subscribe to SMF Works Pro
1. Visit https://smf.works/subscribe
2. Choose "Pro" plan ($19.99/mo)
3. Complete checkout via Stripe
4. Save your customer ID (starts with `cus_`)

### Step 2: Install CLI Tool
```bash
# Navigate to CLI directory
cd ../../cli

# Copy CLI to your PATH (optional but recommended)
cp smf_login.py ~/.local/bin/smf
chmod +x ~/.local/bin/smf
```

### Step 3: Authenticate
```bash
# Run login command
python smf_login.py login

# Or if you added to PATH:
smf login
```

**What happens:**
1. CLI prompts for your SMF token
2. You paste token from https://smf.works/dashboard
3. Token is saved to `~/.smf/token`
4. Ready to use Pro skills

### Step 4: Verify Authentication
```bash
python smf_login.py status
```

Expected output:
```
🔐 SMF Works Subscription Status
========================================
✅ Active subscription
   Tier: pro
   Expires: 1741632000
```

---

## Configuration

### Data Directory
Lead Capture stores data in:
```
~/.smf/
├── token              # Your auth token (keep secret!)
├── leads/             # Lead JSON files
│   ├── lead-20260320-143052.json
│   ├── lead-20260320-145511.json
│   └── ...
└── revoke_cache.json  # Revocation list cache
```

### Changing Data Location (Advanced)
To use a custom data directory, set environment variable:

```bash
export SMF_DATA_DIR="/path/to/custom/location"
```

Then modify `main.py` line 17:
```python
LEADS_DIR = Path(os.environ.get("SMF_DATA_DIR", Path.home() / ".smf")) / "leads"
```

### Custom Scoring Weights
To customize lead scoring, edit these values in `main.py`:

```python
# Line 45-60: Adjust these weights
def calculate_lead_score(lead: Dict) -> int:
    score = 0
    
    # Contact completeness
    if lead.get("email"):
        score += 20  # Change this value
    if lead.get("phone"):
        score += 20  # Change this value
    
    # Business info
    if lead.get("company"):
        score += 15  # Change this value
    if lead.get("title"):
        score += 10  # Change this value
    
    # Qualification
    budget_scores = {
        "small": 10,   # Change these values
        "medium": 20,
        "large": 30
    }
    
    timeline_scores = {
        "immediate": 30,  # Change these values
        "1-month": 20,
        "3-months": 10,
        "6-months": 5
    }
    
    return min(score, 100)
```

### Status Thresholds
Change lead status thresholds in `main.py`:

```python
# Line 78-84
def get_lead_status(score: int) -> str:
    if score >= 80:        # Change threshold
        return "🔥 Hot"
    elif score >= 60:      # Change threshold
        return "🌡️ Warm"
    elif score >= 40:      # Change threshold
        return "❄️ Cold"
    else:
        return "💤 Dormant"
```

---

## Usage

### Quick Start
```bash
# 1. Capture your first lead
python main.py capture

# 2. View all leads
python main.py list

# 3. Check statistics
python main.py stats
```

### Capture Workflow
```bash
$ python main.py capture

🎯 Lead Capture
========================================

Enter lead information (press Enter to skip):
Name: Jane Smith
Email: jane@example.com
Phone: 555-0199
Company: Acme Corporation
Title/Role: VP of Operations

Qualification:
  Budget: small/medium/large
Budget: medium
  Timeline: immediate/1-month/3-months/6-months
Timeline: 1-month
  Source: website/referral/social/cold-outreach/other
Source: website
Notes: Interested in AI automation for customer service

✅ Lead captured: lead-20260320-213956
   Score: 85/100 (🔥 Hot)
   Saved to: /home/user/.smf/leads/lead-20260320-213956.json
```

### Viewing Leads
```bash
# List all leads
python main.py list

# List top 10 leads
python main.py list 10

# Example output:
📊 15 Lead(s)
--------------------------------------------------------------------------------
ID                   Name                 Score    Status       Source
--------------------------------------------------------------------------------
lead-20260320-213956 Jane Smith           85       🔥 Hot        website
lead-20260320-184411 John Doe             72       🌡️ Warm       referral
lead-20260320-162233 Alice Johnson        45       ❄️ Cold        cold-outreach
--------------------------------------------------------------------------------
```

### Exporting Data
```bash
# Export to CSV (opens in Excel, Google Sheets)
python main.py export csv

# Export to JSON (for API integration)
python main.py export json

# Specify output file
python main.py export csv my-leads-backup.csv
```

### Statistics Dashboard
```bash
$ python main.py stats

📈 Lead Statistics
========================================
Total Leads: 15

Qualification:
  🔥 Hot (80-100):     3 (20.0%)
  🌡️ Warm (60-79):     7 (46.7%)
  ❄️ Cold (40-59):     4 (26.7%)
  💤 Dormant (0-39):   1 (6.7%)

Sources:
  website: 8
  referral: 4
  social: 2
  cold-outreach: 1
```

---

## Troubleshooting

### "No subscription token found"
**Problem:** Not authenticated

**Solution:**
```bash
python ../../cli/smf_login.py login
```

### "Token expired"
**Problem:** Subscription lapsed or token expired

**Solution:**
1. Visit https://smf.works/subscribe
2. Check subscription status
3. Re-run `smf login` if renewed

### "Skill 'lead-capture' not in subscription"
**Problem:** Wrong subscription tier

**Solution:**
- Free tier: Upgrade to Pro ($19.99/mo)
- Pro tier: Contact support@smf.works

### Permission Denied on `~/.smf`
**Problem:** File permissions issue

**Solution:**
```bash
# Fix permissions
chmod 700 ~/.smf
chmod 600 ~/.smf/token
chmod 755 ~/.smf/leads
```

### Leads Not Saving
**Problem:** Disk space or permissions

**Solution:**
```bash
# Check disk space
df -h ~/.smf

# Check directory exists
mkdir -p ~/.smf/leads

# Verify write permissions
touch ~/.smf/leads/test && rm ~/.smf/leads/test
```

### Module Not Found Error
**Problem:** `smf_auth` not found

**Solution:**
```bash
# Run from correct directory
cd smfworks-skills/skills/lead-capture
python main.py capture

# Or install shared module
export PYTHONPATH="$PYTHONPATH:/path/to/smfworks-skills/shared"
```

---

## Data Backup

### Manual Backup
```bash
# Backup all leads
cp -r ~/.smf/leads ~/backups/smf-leads-$(date +%Y%m%d)

# Backup with token (for transfer to new machine)
cp ~/.smf/token ~/backups/smf-token-backup
```

### Automated Backup Script
Create `backup-leads.sh`:
```bash
#!/bin/bash
BACKUP_DIR="$HOME/backups/smf-leads"
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/leads-$DATE.tar.gz" -C "$HOME" .smf/leads

# Keep only last 10 backups
ls -t "$BACKUP_DIR"/*.tar.gz | tail -n +11 | xargs rm -f

echo "Backup complete: $BACKUP_DIR/leads-$DATE.tar.gz"
```

Make it run daily:
```bash
chmod +x backup-leads.sh

# Add to crontab
crontab -e

# Add line:
0 2 * * * /path/to/backup-leads.sh
```

### Restore from Backup
```bash
# Extract backup
tar -xzf leads-20260320-120000.tar.gz

# Copy to SMF directory
cp -r .smf/leads/* ~/.smf/leads/
```

---

## Next Steps

1. **Try it out:** Run `python main.py capture` to add your first lead
2. **Explore:** Check out other Pro skills in the repository
3. **Integrate:** Export CSV and import into your CRM
4. **Customize:** Modify scoring weights to match your business
5. **Automate:** Set up daily backups

---

## Support

- **Documentation:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Email:** support@smf.works

---

*Last updated: March 20, 2026*
