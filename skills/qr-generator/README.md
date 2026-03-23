# QR Generator

> Generate QR codes for URLs, WiFi, email, contacts, and more — in PNG or SVG format

---

## What It Does

QR Generator creates scannable QR codes for all kinds of data — website URLs, WiFi network credentials, email addresses, phone numbers, vCard contacts, and SMS messages. Output as PNG or SVG files, ready to print or share.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install qr-generator
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Generate a QR code for a website:

```bash
python main.py url https://smf.works
```

---

## Commands

### `url`

**What it does:** Generate QR code for a URL/website.

**Usage:**
```bash
python main.py url [url] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url` | ✅ Yes | Website URL | `https://smf.works` |
| `output-file` | ❌ No | Output file (default: qr-code.png) | `website.png` |

**Example:**
```bash
python main.py url https://smf.works
python main.py url https://smf.works website-qr.png
```

---

### `wifi`

**What it does:** Generate QR code for WiFi network credentials.

**Usage:**
```bash
python main.py wifi [ssid] [password] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `ssid` | ✅ Yes | Network name | `MyNetwork` |
| `password` | ✅ Yes | WiFi password | `password123` |
| `output-file` | ❌ No | Output file (default: wifi.png) | `wifi-qr.png` |

**Example:**
```bash
python main.py wifi "MyNetwork" "password123"
python main.py wifi "GuestNetwork" "Welcome2024!" guest-wifi.png
```

---

### `email`

**What it does:** Generate QR code for an email address.

**Usage:**
```bash
python main.py email [address] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `address` | ✅ Yes | Email address | `hello@example.com` |
| `output-file` | ❌ No | Output file | `email-qr.png` |

**Example:**
```bash
python main.py email hello@example.com
```

---

### `phone`

**What it does:** Generate QR code for a phone number.

**Usage:**
```bash
python main.py phone [number] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `number` | ✅ Yes | Phone number | `+1234567890` |
| `output-file` | ❌ No | Output file | `phone-qr.png` |

**Example:**
```bash
python main.py phone "+1234567890"
```

---

### `vcard`

**What it does:** Generate QR code for a contact (vCard format).

**Usage:**
```bash
python main.py vcard [name] [phone] [email] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `name` | ✅ Yes | Full name | `John Doe` |
| `phone` | ✅ Yes | Phone number | `+1234567890` |
| `email` | ❌ No | Email address | `john@email.com` |
| `output-file` | ❌ No | Output file | `contact.png` |

**Example:**
```bash
python main.py vcard "Jane Doe" "+15551234567" "jane@email.com"
```

---

### `sms`

**What it does:** Generate QR code for SMS message.

**Usage:**
```bash
python main.py sms [phone] [message] [output-file]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `phone` | ✅ Yes | Phone number | `+1234567890` |
| `message` | ❌ No | Pre-filled message | `Hello!` |
| `output-file` | ❌ No | Output file | `sms-qr.png` |

**Example:**
```bash
python main.py sms "+1234567890" "Call me back!"
```

---

## Use Cases

- **Share WiFi:** Guests scan to connect without typing passwords
- **Contact cards:** Share your info at networking events
- **Business cards:** Include on printed materials
- **Payments:** Link to payment or donation pages
- **Product info:** Link to product pages from catalogs

---

## Tips & Tricks

- Print WiFi QR codes for guests at home or office
- Use vCard for easy contact sharing at events
- Keep QR codes simple — shorter URLs scan faster
- Test your QR codes with multiple scanners before printing

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "qrcode not installed" | Run `pip install qrcode[pil]` |
| QR won't scan | Make sure there's enough contrast |
| WiFi QR doesn't work | Ensure SSID and password are exact |
| Invalid URL | Must include http:// or https:// |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- qrcode library (`pip install qrcode[pil]`)

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/qr-generator)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
