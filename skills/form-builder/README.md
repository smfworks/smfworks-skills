# Form Builder

> Create web forms with validation — contact forms, surveys, feedback forms, and more

---

## What It Does

Form Builder creates production-ready HTML forms for websites. Define fields, set validation rules, and generate clean HTML you can drop into any website. Supports text inputs, email, phone, dropdowns, checkboxes, radio buttons, and textarea fields with built-in validation.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install form-builder
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Create your first form:

```bash
python main.py create "Contact Form"
```

---

## Commands

### `create`

**What it does:** Create a new form with fields you specify.

**Usage:**
```bash
python main.py create [form-name] [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `form-name` | ✅ Yes | Name for your form | `Contact Form` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--fields` | ❌ No | Comma-separated field list | `--fields name,email,message` |

**Example:**
```bash
python main.py create "Contact Form"
python main.py create "Survey" --fields name,email,rating,comments
python main.py create "Order Form" --fields name,email,address,product,quantity
```

**Output:**
```
✅ Form created: contact-form
   Fields: name, email, message
   Saved to: ~/.smf/forms/contact-form.json

To render HTML:
  python main.py render contact-form
```

---

### `list`

**What it does:** Display all saved forms.

**Usage:**
```bash
python main.py list
```

**Example:**
```bash
python main.py list
```

**Output:**
```
📝 Your Forms:
------------------------------------------------------------
1. contact-form     | 3 fields | Created: 2026-03-20
2. survey           | 4 fields | Created: 2026-03-19
3. order-form       | 5 fields | Created: 2026-03-18
```

---

### `render`

**What it does:** Generate HTML output for a saved form.

**Usage:**
```bash
python main.py render [form-id]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `form-id` | ✅ Yes | ID of form to render | `contact-form` |

**Example:**
```bash
python main.py render contact-form
```

**Output:**
```html
<form id="contact-form" method="POST" action="/submit">
  <div class="form-group">
    <label for="name">Name</label>
    <input type="text" id="name" name="name" required>
  </div>
  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" id="email" name="email" required>
  </div>
  <div class="form-group">
    <label for="message">Message</label>
    <textarea id="message" name="message" required></textarea>
  </div>
  <button type="submit">Submit</button>
</form>
```

---

### `export`

**What it does:** Export a form definition for use in other tools.

**Usage:**
```bash
python main.py export [form-id] --format [json|yaml]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `form-id` | ✅ Yes | ID of form to export | `contact-form` |

**Options:**

| Option | Required | Description | Example |
|--------|----------|-------------|---------|
| `--format` | ❌ No | Output format: `json` or `yaml` | `--format json` |

**Example:**
```bash
python main.py export contact-form --format json
```

---

## Use Cases

- **Contact forms:** Simple website contact forms
- **Surveys:**收集用户反馈和调查回复
- **Order forms:** Product order or request forms
- **Registration:** Event or membership registration
- **Feedback:** Customer feedback and support requests

---

## Tips & Tricks

- Use descriptive form names — they become the form ID
- Available field types: `text`, `email`, `phone`, `textarea`, `select`, `checkbox`, `radio`
- Generated HTML is responsive and works with any CSS framework
- Export forms to JSON to share or backup your form definitions

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Form not found" | Check the form ID with `python main.py list` |
| Wrong field order | Recreate the form with fields in correct order |
| Validation not working | Ensure `required` attribute is present in HTML |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- No external dependencies

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/form-builder)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
