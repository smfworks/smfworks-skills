# Form Builder

Create forms, serve them via HTTP, collect responses, and export data. Perfect for contact forms, surveys, registrations, and feedback collection.

## Features

- ✅ **Form Creation** — Interactive builder with multiple field types
- ✅ **10 Field Types** — Text, email, number, textarea, select, checkbox, radio, date, tel, url
- ✅ **HTTP Server** — Built-in server to serve forms locally
- ✅ **Response Collection** — Automatic saving of submissions
- ✅ **Data Export** — Export to CSV or JSON
- ✅ **Form Management** — List, view, and organize forms
- ✅ **Local Storage** — All data stays on your machine

## Installation

```bash
# Install SMF CLI (if not already)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Login (Pro skill requires subscription)
smf login

# Install the skill
smf install form-builder
```

## Quick Start

### 1. Create a Form

```bash
# Interactive mode (recommended)
smf run form-builder create

# Quick mode
smf run form-builder create --name "Contact Form" --fields name,email,message
```

### 2. Serve the Form

```bash
smf run form-builder serve FORM-ABC123 --port 8080
```

### 3. Access and Submit

Open browser to: `http://localhost:8080/FORM-ABC123`

Fill out and submit — responses are saved automatically.

### 4. View Responses

```bash
smf run form-builder responses FORM-ABC123
```

### 5. Export Data

```bash
smf run form-builder export FORM-ABC123 --format csv
```

## Usage

### Creating Forms

**Interactive mode:**
```bash
smf run form-builder create
```

You'll be prompted for:
- Form name
- Description (optional)
- Fields (name, label, type, required, options)

**Field types:**
- `text` — Single line text
- `email` — Email address with validation
- `number` — Numeric input
- `textarea` — Multi-line text
- `select` — Dropdown menu
- `checkbox` — Single checkbox
- `radio` — Radio button group
- `date` — Date picker
- `tel` — Telephone number
- `url` — URL input

**Quick mode:**
```bash
smf run form-builder create --name "Survey" --fields name,email,rating,feedback
```

**Adding fields to existing form:**
```bash
smf run form-builder add-field FORM-ABC123
```

### Serving Forms

**Start server:**
```bash
smf run form-builder serve FORM-ABC123
# Serves on http://localhost:8080/FORM-ABC123
```

**Custom port:**
```bash
smf run form-builder serve FORM-ABC123 --port 3000
# Serves on http://localhost:3000/FORM-ABC123
```

**Access the form:**
- Open browser
- Navigate to `http://localhost:8080/FORM-ABC123`
- Fill out and submit
- Success message displayed

**Stop server:**
- Press `Ctrl+C` in terminal

### Managing Forms

**List all forms:**
```bash
smf run form-builder list
```

Output:
```
📝 Forms (3)
--------------------------------------------------------------------------------
ID                   Name                           Status       Responses
--------------------------------------------------------------------------------
FORM-ABC123          Contact Form                   ✅ active    12
FORM-DEF456          Customer Survey                ✅ active    45
FORM-GHI789          Event Registration             ⏸️ paused   0
--------------------------------------------------------------------------------
```

**View form details:**
```bash
smf run form-builder show FORM-ABC123
```

Output:
```
📝 Form Details
============================================================
ID: FORM-ABC123
Name: Contact Form
Status: active
Responses: 12
Created: 2026-03-20

Description: General contact form for website

Fields:
  1. Name [text] (required)
  2. Email [email] (required)
  3. Message [textarea] (required)
  4. Newsletter [checkbox]
```

### Collecting Responses

**View responses:**
```bash
smf run form-builder responses FORM-ABC123
```

Output:
```
📊 Responses for 'Contact Form' (12)
--------------------------------------------------------------------------------

1. Response RESP-A1B2C3D4
   Submitted: 2026-03-20T14:30:00
   name: John Smith
   email: john@example.com
   message: Interested in your services
   newsletter: on

2. Response RESP-E5F6G7H8
   Submitted: 2026-03-20T15:45:00
   name: Jane Doe
   email: jane@example.com
   message: Quick question about pricing
   newsletter: 

... and 10 more responses
--------------------------------------------------------------------------------
```

### Exporting Data

**Export to CSV:**
```bash
smf run form-builder export FORM-ABC123 --format csv
```

Creates: `FORM-ABC123-responses.csv`

**Export to JSON:**
```bash
smf run form-builder export FORM-ABC123 --format json
```

Creates: `FORM-ABC123-responses.json`

**Custom output file:**
```bash
smf run form-builder export FORM-ABC123 --format csv --output my-data.csv
```

### CSV Format

```csv
name,email,message,newsletter,submitted_at
John Smith,john@example.com,Interested in services,on,2026-03-20T14:30:00
Jane Doe,jane@example.com,Question about pricing,,2026-03-20T15:45:00
```

### JSON Format

```json
[
  {
    "id": "RESP-A1B2C3D4",
    "form_id": "FORM-ABC123",
    "data": {
      "name": "John Smith",
      "email": "john@example.com",
      "message": "Interested in services",
      "newsletter": "on"
    },
    "submitted_at": "2026-03-20T14:30:00"
  }
]
```

## Form Examples

### Contact Form

```bash
smf run form-builder create --name "Contact Form" --fields name,email,message
```

Fields:
- Name (text, required)
- Email (email, required)
- Message (textarea, required)

### Customer Survey

```bash
smf run form-builder create --name "Customer Survey" --fields name,email,rating,feedback
```

Fields:
- Name (text)
- Email (email)
- Rating (number)
- Feedback (textarea)

### Event Registration

```bash
smf run form-builder create --name "Event Registration"
# Then add fields:
smf run form-builder add-field FORM-XXX
# - full_name (text, required)
# - email (email, required)
# - company (text)
# - dietary_requirements (textarea)
# - attending (select: Yes/No/Maybe)
```

### Job Application

```bash
smf run form-builder create --name "Job Application"
# Fields:
# - full_name (text, required)
# - email (email, required)
# - phone (tel)
# - position (select)
# - resume_url (url)
# - cover_letter (textarea)
```

## Storage Structure

```
~/.smf/
├── forms/
│   ├── FORM-ABC123.json       # Form definition
│   ├── FORM-DEF456.json
│   └── ...
└── form-responses/
    ├── RESP-A1B2C3D4.json     # Individual response
    ├── RESP-E5F6G7H8.json
    └── ...
```

### Form JSON Format

```json
{
  "id": "FORM-ABC123",
  "name": "Contact Form",
  "description": "General contact",
  "fields": [
    {
      "id": "field-0",
      "name": "name",
      "label": "Name",
      "type": "text",
      "required": true,
      "placeholder": "Your name"
    },
    {
      "id": "field-1",
      "name": "email",
      "label": "Email",
      "type": "email",
      "required": true
    }
  ],
  "created_at": "2026-03-20T14:30:00",
  "status": "active",
  "response_count": 12
}
```

### Response JSON Format

```json
{
  "id": "RESP-A1B2C3D4",
  "form_id": "FORM-ABC123",
  "data": {
    "name": "John Smith",
    "email": "john@example.com"
  },
  "submitted_at": "2026-03-20T14:30:00"
}
```

## Workflows

### Website Contact Form

```bash
# 1. Create form
smf run form-builder create --name "Website Contact" --fields name,email,message

# 2. Start server (in background or separate terminal)
smf run form-builder serve FORM-XXX --port 8080

# 3. Embed form in website
# Add iframe or link to http://localhost:8080/FORM-XXX

# 4. Check responses daily
smf run form-builder responses FORM-XXX

# 5. Export weekly for CRM
smf run form-builder export FORM-XXX --format csv
```

### Event Registration

```bash
# 1. Create registration form
smf run form-builder create --name "Conference 2026 Registration"
# Add fields for name, email, company, dietary needs, etc.

# 2. Serve form
smf run form-builder serve FORM-XXX --port 3000

# 3. Share link with attendees
# http://your-server:3000/FORM-XXX

# 4. Monitor registrations
smf run form-builder responses FORM-XXX | wc -l

# 5. Export attendee list
smf run form-builder export FORM-XXX --format csv --output attendees.csv
```

### Customer Feedback Survey

```bash
# 1. Create survey
smf run form-builder create --name "Post-Purchase Survey"

# 2. Add fields for rating, feedback, NPS, etc.

# 3. Include link in order confirmation email
# Thank you! Please rate your experience: http://server/FORM-XXX

# 4. Analyze responses
smf run form-builder export FORM-XXX --format csv
# Import into spreadsheet for analysis
```

## Integration Ideas

### With Email

```bash
# Export responses
smf run form-builder export FORM-XXX --format csv

# Email to team
mutt -s "New Form Responses" team@example.com -a FORM-XXX-responses.csv
```

### With Spreadsheet

```bash
# Export to CSV
smf run form-builder export FORM-XXX --format csv

# Open in LibreOffice Calc or Excel
libreoffice FORM-XXX-responses.csv
```

### With Database

```bash
# Export to JSON
smf run form-builder export FORM-XXX --format json

# Import to database
psql -d mydb -c "COPY responses FROM 'FORM-XXX-responses.json';"
```

### Automation

```bash
# Daily export script
#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"

for form in $(smf run form-builder list | grep FORM- | awk '{print $1}'); do
    smf run form-builder export $form --format csv --output "/var/www/exports/$form.csv"
done
```

## Best Practices

### 1. Keep Forms Focused

**Good:**
- Contact form: name, email, message
- Survey: 5-10 questions max

**Bad:**
- 50-question mega form
- Asking for unnecessary info

### 2. Use Required Fields Wisely

**Should be required:**
- Contact email
- Key identifiers

**Should be optional:**
- Phone number
- Additional comments
- Marketing opt-in

### 3. Test Before Sharing

```bash
# 1. Create form
smf run form-builder create

# 2. Serve locally
smf run form-builder serve FORM-XXX

# 3. Submit test response
# Open browser, fill out, submit

# 4. Verify response saved
smf run form-builder responses FORM-XXX

# 5. Check export works
smf run form-builder export FORM-XXX --format csv

# 6. Share with users
```

### 4. Clear Naming

**Good:**
- "Website Contact Form"
- "Q1 Customer Survey"
- "Event Registration - March 2026"

**Bad:**
- "Form 1"
- "Test"
- "New Form"

### 5. Regular Backups

```bash
# Backup forms and responses
tar -czf ~/backups/forms-$(date +%Y%m%d).tar.gz ~/.smf/forms/ ~/.smf/form-responses/

# Weekly cron
0 2 * * 0 tar -czf ~/backups/forms-$(date +\%Y\%m\%d).tar.gz ~/.smf/forms/ ~/.smf/form-responses/
```

### 6. Data Privacy

- Don't collect more data than needed
- Store responses locally (✓)
- Consider data retention policy
- Delete old responses if needed

## Pricing

**Form Builder is a premium SMF Works skill.**

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

- **Price:** $19.99/month (locked forever at signup rate)
- **Includes:** All premium skills, updates, priority support
- **Free alternative:** Use Google Forms, Typeform, or manual HTML

Subscribe at https://smf.works/subscribe

## See Also

- [SETUP.md](./SETUP.md) — Complete setup and configuration guide
- `smf help` — CLI documentation
- `smf status` — Check subscription status

## License

SMF Works Pro Skill — See SMF Works Terms of Service
