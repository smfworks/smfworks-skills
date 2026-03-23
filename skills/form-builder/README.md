# Form Builder

> Create web forms, serve them via a local HTTP server, collect responses, and export submissions — all from your terminal.

**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo at [smfworks.com/subscribe](https://smfworks.com/subscribe))  
**Version:** 1.0  
**Category:** Web / Data Collection

---

## What It Does

Form Builder is an OpenClaw Pro skill for creating simple web forms and collecting submissions. Create a form with fields (text, email, number, textarea, select, checkbox, radio, date, phone, URL), serve it on a local HTTP server with CSRF protection, view submitted responses, and export them to CSV or JSON.

**Security features:** CSRF protection, XSS prevention on submitted data, CSV injection prevention on exports, and input validation on all fields.

**What it does NOT do:** It does not expose forms to the public internet (only local/LAN accessible), send email notifications on submissions, store files from file upload fields, or integrate with third-party services.

---

## Prerequisites

- [ ] **SMF Works Pro subscription** — [smfworks.com/subscribe](https://smfworks.com/subscribe)
- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed and authenticated**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/form-builder
python3 main.py help
```

---

## Quick Start

```bash
# Create a form
python3 main.py create --name "Contact Form" --fields name,email,message

# Serve it
python3 main.py serve FORM-ABC123 --port 8080
# Open http://localhost:8080/FORM-ABC123 in your browser

# View responses
python3 main.py responses FORM-ABC123
```

---

## Command Reference

### `create`

Creates a new form. Interactive or via flags.

```bash
python3 main.py create                                            # Interactive
python3 main.py create --name "Contact Form"                     # With name
python3 main.py create --name "Contact Form" --fields name,email,message
```

**Supported field types:** `text`, `email`, `number`, `textarea`, `select`, `checkbox`, `radio`, `date`, `tel`, `url`

Output:
```
✅ Form created: FORM-A1B2C3
   Name: Contact Form
   Fields: name (text), email (email), message (textarea)
   URL: http://localhost:8080/FORM-A1B2C3
```

---

### `list`

Lists all forms.

```bash
python3 main.py list
```

Output:
```
📋 Forms (3 total):

1. FORM-A1B2C3 — Contact Form — 3 fields — 47 responses
2. FORM-D4E5F6 — Feedback Survey — 5 fields — 12 responses
3. FORM-G7H8I9 — Event Registration — 6 fields — 8 responses
```

---

### `show FORM-ID`

Shows full form details and field list.

```bash
python3 main.py show FORM-A1B2C3
```

---

### `add-field FORM-ID`

Interactive prompt to add a new field to an existing form.

```bash
python3 main.py add-field FORM-A1B2C3
```

---

### `serve FORM-ID`

Starts a local HTTP server and serves the form. Opens to `http://localhost:PORT/FORM-ID`.

```bash
python3 main.py serve FORM-A1B2C3
python3 main.py serve FORM-A1B2C3 --port 8080
```

Output:
```
🌐 Form Server Started
   Form: Contact Form (FORM-A1B2C3)
   URL: http://localhost:8080/FORM-A1B2C3
   Press Ctrl+C to stop

[09:42:11] GET /FORM-A1B2C3 200 — form served
[09:42:34] POST /FORM-A1B2C3/submit 200 — 1 submission saved
```

---

### `responses FORM-ID`

Shows all submissions for a form.

```bash
python3 main.py responses FORM-A1B2C3
```

Output:
```
📋 Responses: Contact Form (47 total)

1. 2024-03-15 09:42 — Alice Smith — alice@example.com — "Love your service..."
2. 2024-03-14 14:21 — Bob Jones — bob@techco.io — "Please contact me re..."
...
```

---

### `export FORM-ID`

Exports responses to CSV or JSON.

```bash
python3 main.py export FORM-A1B2C3
python3 main.py export FORM-A1B2C3 --format csv --output contacts.csv
python3 main.py export FORM-A1B2C3 --format json --output responses.json
```

Output:
```
✅ Exported 47 responses to contacts.csv
```

---

## Use Cases

### 1. Local contact form for testing

Create a contact form, run the server, share the URL with a colleague on your local network for testing.

### 2. Internal data collection

Collect structured data from team members on your local network.

### 3. Event registration on a LAN

At an event, run the server and let attendees register on the local network.

### 4. Lead capture form

Run on a machine at a kiosk or reception desk.

---

## How the Server Works

The `serve` command starts a Python HTTP server. It:
- Renders the form as an HTML page
- Accepts POST submissions
- Validates each field
- Stores responses locally in `~/.smf/forms/FORM-ID/responses/`
- Protects against CSRF attacks

The server is only accessible on your local machine at `localhost`. To share on a LAN, use your machine's local IP address (`192.168.x.x`) in the URL.

---

## Field Types Reference

| Type | Description | Example |
|------|-------------|---------|
| `text` | Single-line text input | Name, company |
| `email` | Email address with validation | Contact email |
| `number` | Numeric input | Age, quantity |
| `textarea` | Multi-line text | Message, comments |
| `select` | Dropdown selection | Country, plan type |
| `checkbox` | Multiple choice checkboxes | Interests |
| `radio` | Single choice radio buttons | Priority |
| `date` | Date picker | Birth date, event date |
| `tel` | Phone number | Contact phone |
| `url` | URL with validation | Website |

---

## Troubleshooting

### `Error: SMF Works Pro subscription required`
**Fix:** Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

### `Address already in use: port 8080`
**Fix:** Another process is using port 8080. Try a different port: `--port 8081`

### `Form not found: FORM-XYZ`
**Fix:** Check exact form IDs with `python3 main.py list`.

### Form is accessible on localhost but not from another device
**Fix:** Use your machine's local IP address, not `localhost`. Find it with `ip addr` (Linux) or `ifconfig` (macOS).

### Responses show validation errors
**Fix:** Required fields must be filled. Check the form's required field settings.

---

## FAQ

**Q: Can the form be accessed from the internet?**  
A: No — the server only binds to localhost by default. For internet-accessible forms, you'd need a reverse proxy (nginx, etc.) which is outside this skill's scope.

**Q: Where are responses stored?**  
A: Locally at `~/.smf/forms/FORM-ID/responses/`. Each submission is a JSON file.

**Q: Can I add conditional fields (show field X only if Y is selected)?**  
A: Not in the current version. All fields are always shown.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| SMF Works Pro | Required ($19.99/mo) |
| External APIs | None |
| Internet | For subscription check only |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/form-builder)
- 🔑 [Subscribe](https://smfworks.com/subscribe)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
