# QR Generator

> Create QR codes for URLs, WiFi networks, email addresses, phone numbers, contacts, and SMS — in seconds from your terminal.

**Tier:** Free — no subscription required  
**Version:** 1.0  
**Category:** Productivity / Utilities

---

## What It Does

QR Generator is an OpenClaw skill that creates QR code images for six common use cases: web URLs, WiFi credentials, email addresses, phone numbers, vCard contacts, and SMS messages. Output is a PNG file by default, with SVG also supported.

The generated QR codes can be scanned by any smartphone camera or QR reader. WiFi QR codes let guests join your network instantly without typing a password. vCard QR codes let anyone scan to add a contact directly to their phone.

**What it does NOT do:** It does not read or decode existing QR codes, batch-generate multiple codes in one command, add logos or images inside the QR code, or create QR codes for binary data.

---

## Prerequisites

- [ ] **Python 3.8 or newer** — run `python3 --version` to check
- [ ] **OpenClaw installed** — run `openclaw --version` to check
- [ ] **qrcode[pil] Python package** — installed during setup
- [ ] **No subscription required** — free tier skill
- [ ] **No API keys required**

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/qr-generator
pip install "qrcode[pil]"
python3 main.py
```

Expected output:
```
Usage: python main.py <command> [options]

Commands:
  url <url> [output.png]              - Generate URL QR code
  wifi <ssid> <password> [output.png]  - Generate WiFi QR code
  email <email> [output.png]          - Generate email QR code
  phone <number> [output.png]        - Generate phone QR code
  vcard <name> <phone> [email] [output.png] - Generate vCard
  sms <number> [message] [output.png] - Generate SMS QR
```

---

## Quick Start

Generate a QR code for your website:

```bash
python3 main.py url https://yourwebsite.com qr-website.png
```

Output:
```
✅ QR code generated: qr-website.png
   Data: https://yourwebsite.com
   Size: 29x29
```

Scan `qr-website.png` with your phone to verify.

---

## Command Reference

### `url`

Generates a QR code that opens a URL when scanned. Supports `http://`, `https://`, `mailto:`, and `tel:` URLs.

**Usage:**
```bash
python3 main.py url <url> [output.png]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `url` | ✅ Yes | URL to encode | `https://smfworks.com` |
| `output.png` | ❌ No | Output filename. Defaults to `qr-code.png` | `website-qr.png` |

**Example:**
```bash
python3 main.py url https://smfworks.com ~/Desktop/smfworks-qr.png
```

**Output:**
```
✅ QR code generated: /home/user/Desktop/smfworks-qr.png
   Data: https://smfworks.com
   Size: 25x25
```

---

### `wifi`

Generates a QR code that connects a phone to your WiFi network when scanned — no password typing required.

**Usage:**
```bash
python3 main.py wifi <ssid> <password> [output.png]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `ssid` | ✅ Yes | WiFi network name | `MyHomeNetwork` |
| `password` | ✅ Yes | WiFi password | `secretpassword123` |
| `output.png` | ❌ No | Output filename. Defaults to `wifi.png` | `guest-wifi.png` |

**Example:**
```bash
python3 main.py wifi 'GuestNetwork' 'welcome2024' ~/Desktop/guest-wifi.png
```

**Output:**
```
✅ WiFi QR code generated: /home/user/Desktop/guest-wifi.png
   Network: GuestNetwork
   Size: 33x33
```

Print this QR code and post it by your router so guests can connect instantly.

---

### `email`

Generates a QR code that opens a pre-addressed email when scanned.

**Usage:**
```bash
python3 main.py email <email_address> [output.png]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `email_address` | ✅ Yes | Email address to encode | `hello@example.com` |
| `output.png` | ❌ No | Output filename. Defaults to `email.png` | `contact-qr.png` |

**Example:**
```bash
python3 main.py email contact@mycompany.com ~/Desktop/contact-email.png
```

**Output:**
```
✅ Email QR code generated: /home/user/Desktop/contact-email.png
   Email: contact@mycompany.com
```

---

### `phone`

Generates a QR code that initiates a phone call when scanned.

**Usage:**
```bash
python3 main.py phone <number> [output.png]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `number` | ✅ Yes | Phone number. Digits, `+`, `-`, spaces, and parentheses allowed. | `+12125551234` |
| `output.png` | ❌ No | Output filename. Defaults to `phone.png` | `call-us.png` |

**Example:**
```bash
python3 main.py phone '+1 (212) 555-1234' ~/Desktop/call-us.png
```

**Output:**
```
✅ Phone QR code generated: /home/user/Desktop/call-us.png
   Phone: +1 (212) 555-1234
```

---

### `vcard`

Generates a vCard QR code that adds a contact (name, phone, and optional email) to the scanner's phone when scanned.

**Usage:**
```bash
python3 main.py vcard <name> <phone> [email] [output.png]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `name` | ✅ Yes | Full name | `Jane Smith` |
| `phone` | ✅ Yes | Phone number | `+12125551234` |
| `email` | ❌ No | Email address | `jane@company.com` |
| `output.png` | ❌ No | Output filename. Defaults to `vcard.png` | `jane-contact.png` |

**Example:**
```bash
python3 main.py vcard 'Jane Smith' '+1 212 555 1234' 'jane@company.com' ~/Desktop/jane-contact.png
```

**Output:**
```
✅ vCard QR code generated: /home/user/Desktop/jane-contact.png
   Name: Jane Smith
```

---

### `sms`

Generates a QR code that opens an SMS message to a phone number, with optional pre-filled text.

**Usage:**
```bash
python3 main.py sms <number> [message] [output.png]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `number` | ✅ Yes | Destination phone number | `+12125551234` |
| `message` | ❌ No | Pre-filled message text (max 500 characters) | `"Hi, I found you via QR"` |
| `output.png` | ❌ No | Output filename. Defaults to `sms.png` | `text-us.png` |

**Example:**
```bash
python3 main.py sms '+12125551234' 'Hello from the QR code!' ~/Desktop/text-us.png
```

**Output:**
```
✅ SMS QR code generated: /home/user/Desktop/text-us.png
   Phone: +12125551234
```

---

## Use Cases

### 1. Print a WiFi QR code for guests

```bash
python3 main.py wifi 'MyGuestNetwork' 'guestpass123' ~/Desktop/wifi-qr.png
```

Print the image and post it on your wall. Guests scan it to connect without you spelling out the password.

---

### 2. Add your contact info to marketing materials

```bash
python3 main.py vcard 'Alex Johnson' '+1 415 555 0001' 'alex@mybusiness.com' ~/Desktop/alex-contact.png
```

Add the QR to your business card. Anyone who scans it gets your contact saved immediately.

---

### 3. Put a QR code on a flyer that links to your website

```bash
python3 main.py url https://myevent.com/rsvp flyer-qr.png
```

Include `flyer-qr.png` in your flyer design file.

---

### 4. Create a "text us" QR for a storefront

```bash
python3 main.py sms '+12125550000' 'I saw your store — can I ask a question?' storefront-sms.png
```

Post it at your storefront. Customers scan it and get a pre-written SMS ready to send.

---

### 5. Put your email on a printed handout

```bash
python3 main.py email hello@mycompany.com handout-email.png
```

Anyone scanning opens a new email pre-addressed to you.

---

## Configuration

No configuration file or environment variables required.

**Built-in limits (not configurable):**

| Setting | Value |
|---------|-------|
| Max data length | 2,000 characters |
| Max QR box size | 40 pixels |
| Max border size | 10 boxes |
| Allowed URL schemes | http, https, mailto, tel |
| Phone number characters | Digits, +, -, spaces, parentheses |

---

## Troubleshooting

### `qrcode not installed. Run: pip install qrcode[pil]`
**Fix:** Run `pip install "qrcode[pil]"` (note the quotes around the package name).

### `Error: Data too long (max 2000 characters)`
**Fix:** Shorten the URL or text. For long URLs, use a URL shortener first (bit.ly, etc.).

### `Error: Data contains invalid characters`
**Fix:** The data contains shell special characters (`;`, `|`, `&`, `$`, newlines). Avoid these in QR data, or encode them first.

### `Error: Only http, https, mailto, and tel URLs are allowed`
**Fix:** Only these four URL schemes are accepted for security. Use `https://` for web URLs.

### `Error: Phone number contains invalid characters`
**Fix:** Phone numbers may only contain digits, `+`, `-`, spaces, and parentheses. Remove letters and symbols.

### `Error: Invalid email address`
**Fix:** The email address must contain `@`. Check for typos.

### `Error: WiFi data contains invalid characters`
**Fix:** Your WiFi SSID or password contains a control character. Most common WiFi passwords are fine.

---

## FAQ

**Q: Can I generate SVG instead of PNG?**  
A: Yes — name the output file with `.svg` extension: `python3 main.py url https://example.com output.svg`

**Q: What error correction level do the QR codes use?**  
A: The skill uses High (`ERROR_CORRECT_H`) — up to 30% of the code can be damaged and still be readable. This is the highest level available.

**Q: Can I scan the QR code to verify it?**  
A: Yes — open the PNG in any image viewer, then scan it with your phone's camera to confirm it contains the right data.

**Q: What if my WiFi password has special characters like `#` or `!`?**  
A: The skill handles most passwords correctly. Characters like `;` and `:` are escaped automatically in the WiFi format. If you run into issues, try quoting the password: `'my;password'`

**Q: Can I customize the QR code colors or add a logo?**  
A: Not in the current version. The skill generates standard black-on-white QR codes.

**Q: Does the output depend on internet access?**  
A: No. QR codes are generated entirely locally. No data is sent anywhere.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| qrcode[pil] | 7.0 or newer |
| OpenClaw | Any version |
| Operating System | Linux, macOS |
| Subscription Tier | Free |
| External APIs | None |
| Internet Connection | Not required |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/qr-generator)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
