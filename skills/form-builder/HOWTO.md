# Form Builder — How-To Guide

**Prerequisites:** SMF Works Pro subscription active. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Create a Form](#1-how-to-create-a-form)
2. [How to Serve a Form and Collect Responses](#2-how-to-serve-a-form-and-collect-responses)
3. [How to View and Export Responses](#3-how-to-view-and-export-responses)
4. [How to Add Fields to an Existing Form](#4-how-to-add-fields-to-an-existing-form)
5. [Automating with Cron](#5-automating-with-cron)
6. [Combining with Other Skills](#6-combining-with-other-skills)
7. [Troubleshooting Common Issues](#7-troubleshooting-common-issues)
8. [Tips & Best Practices](#8-tips--best-practices)

---

## 1. How to Create a Form

**What this does:** Creates a form with specified field names and types.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/form-builder
```

**Step 2 — Create the form with quick flags.**

```bash
python3 main.py create --name "Contact Form" --fields name,email,company,message
```

Output:
```
✅ Form created: FORM-A1B2C3
   Name: Contact Form
   Fields: name (text), email (email), company (text), message (textarea)
```

**Step 3 — Or create interactively.**

```bash
python3 main.py create
```

Follow the prompts to name the form and add fields one by one with custom types.

**Step 4 — Verify the form.**

```bash
python3 main.py show FORM-A1B2C3
```

**Result:** Form created and ready to serve.

---

## 2. How to Serve a Form and Collect Responses

**What this does:** Starts a local HTTP server that renders your form and saves submissions.

### Steps

**Step 1 — Start the server.**

```bash
python3 main.py serve FORM-A1B2C3 --port 8080
```

Output:
```
🌐 Form Server Started
   Form: Contact Form (FORM-A1B2C3)
   URL: http://localhost:8080/FORM-A1B2C3
   Press Ctrl+C to stop
```

**Step 2 — Open the form in your browser.**

Navigate to: `http://localhost:8080/FORM-A1B2C3`

You'll see:
```
Contact Form
─────────────────────────────

Name: [text input]
Email: [email input]
Company: [text input]
Message: [textarea]

[Submit]
```

**Step 3 — Submit a test response.**

Fill in the form and click Submit.

The server terminal shows:
```
[09:42:34] POST /FORM-A1B2C3/submit 200 — 1 submission saved
```

**Step 4 — Keep the server running as long as you need to collect submissions.**

Press `Ctrl+C` when you're done collecting.

**Result:** Responses are saved locally and can be viewed or exported.

---

## 3. How to View and Export Responses

**Step 1 — View responses in the terminal.**

```bash
python3 main.py responses FORM-A1B2C3
```

Output:
```
📋 Responses: Contact Form (3 total)

1. 2024-03-15 09:42 — Alice Smith — alice@example.com — Acme Corp — "Interested in..."
2. 2024-03-15 10:15 — Bob Jones — bob@techco.io — TechCo — "Please call me..."
3. 2024-03-15 11:03 — Carol White — carol@startup.io — StartupCo — "Quick question..."
```

**Step 2 — Export to CSV.**

```bash
python3 main.py export FORM-A1B2C3 --format csv --output contacts.csv
```

Output:
```
✅ Exported 3 responses to contacts.csv
```

**Step 3 — Export to JSON.**

```bash
python3 main.py export FORM-A1B2C3 --format json --output responses.json
```

---

## 4. How to Add Fields to an Existing Form

**When to use it:** You forgot a field when creating the form, or want to add more questions.

```bash
python3 main.py add-field FORM-A1B2C3
```

Interactive prompts:
```
Field name: phone
Field type (text/email/number/textarea/select/checkbox/radio/date/tel/url): tel
Required? (y/n): n

✅ Field added: phone (tel)
```

The next time you serve the form, the new field will appear.

---

## 5. Automating with Cron

### Export responses weekly

```bash
0 9 * * 1 python3 /home/yourname/smfworks-skills/skills/form-builder/main.py export FORM-A1B2C3 --format csv --output /home/yourname/Forms/responses-$(date +\%Y-W\%V).csv >> /home/yourname/logs/form-builder.log 2>&1
```

---

## 6. Combining with Other Skills

**Form Builder + CSV Converter:** Export responses and convert to Excel:

```bash
python3 ~/smfworks-skills/skills/form-builder/main.py export FORM-ID --format csv --output responses.csv
python3 ~/smfworks-skills/skills/csv-converter/main.py csv-to-excel responses.csv responses.xlsx
```

**Form Builder + Lead Capture:** Use Form Builder to collect structured data, then log key contacts to Lead Capture:

```bash
# After reviewing form responses:
python3 ~/smfworks-skills/skills/lead-capture/main.py capture
# Enter the lead's details from the form response
```

---

## 7. Troubleshooting Common Issues

### `Address already in use: port 8080`

**Fix:** Another process is using that port. Use a different port: `--port 8081`. Or find and kill the occupying process: `lsof -ti :8080 | xargs kill`

### Form not loading in browser

**Fix:** The server must be running when you access the form. Check the terminal — press Ctrl+C and restart if needed.

### Submissions not appearing in responses

**Fix:** Verify the submission actually posted — the server terminal should show `POST /FORM-ID/submit 200`. If you see a different status code, there may be a validation error.

### Export shows validation errors in CSV

**Fix:** Responses with invalid data are flagged. The export still includes them — review and clean as needed.

---

## 8. Tips & Best Practices

**Name fields clearly.** Use descriptive field names: `first_name` not `field1`. These become column headers in your CSV export.

**Use `email` type for email fields.** The `email` type validates the format on submission. This reduces invalid data in your responses.

**Test the form before sharing it.** Fill it in yourself first and check the response appears correctly in `responses`.

**Keep the server running only while collecting.** The server uses a port while running. Stop it with Ctrl+C when you're done collecting to free the port.

**Export regularly.** Run exports after each collection session so you have backups of responses outside `~/.smf/forms/`.
