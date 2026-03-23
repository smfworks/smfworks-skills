# QR Generator — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). qrcode[pil] installed.

---

## Table of Contents

1. [How to Create a URL QR Code](#1-how-to-create-a-url-qr-code)
2. [How to Create a WiFi QR Code for Guests](#2-how-to-create-a-wifi-qr-code-for-guests)
3. [How to Create a Contact (vCard) QR Code](#3-how-to-create-a-contact-vcard-qr-code)
4. [How to Create a Phone or SMS QR Code](#4-how-to-create-a-phone-or-sms-qr-code)
5. [How to Create an Email QR Code](#5-how-to-create-an-email-qr-code)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Create a URL QR Code

**What this does:** Generates a PNG image containing a QR code that opens a URL when scanned.

**When to use it:** Adding a QR code to a flyer, business card, poster, or email that links to your website, event page, or any URL.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/qr-generator
```

**Step 2 — Run the url command with your URL and desired output filename.**

```bash
python3 main.py url https://mycompany.com ~/Desktop/website-qr.png
```

Output:
```
✅ QR code generated: /home/user/Desktop/website-qr.png
   Data: https://mycompany.com
   Size: 25x25
```

**Step 3 — Verify by scanning.**  
Open `~/Desktop/website-qr.png` in an image viewer, then scan it with your phone's camera. It should navigate to your URL.

**Step 4 — Include in your design.**  
The PNG file is ready to insert into Canva, Word, Photoshop, or any design tool.

**Result:** A `website-qr.png` file at `~/Desktop` ready to use in any design or printout.

---

## 2. How to Create a WiFi QR Code for Guests

**What this does:** Encodes your WiFi credentials into a QR code. When a guest scans it, their phone connects to your network immediately — no typing required.

**When to use it:** Home, Airbnb, cafe, office, or any location where you want guests to connect quickly without reading out a password.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/qr-generator
```

**Step 2 — Create the WiFi QR code.**  
Replace `GuestNetwork` with your network name and `welcome2024` with your actual password.

```bash
python3 main.py wifi 'GuestNetwork' 'welcome2024' ~/Desktop/guest-wifi.png
```

Output:
```
✅ WiFi QR code generated: /home/user/Desktop/guest-wifi.png
   Network: GuestNetwork
   Size: 33x33
```

**Step 3 — Test it yourself.**  
Scan the PNG with your own phone to verify it connects to the right network.

**Step 4 — Print and display it.**  
Print the PNG at any standard size (4x4 inches is easy to scan). Frame it or laminate it near your router.

**Result:** A printable WiFi QR code that guests can scan to connect without you spelling out your password.

**Security note:** Only put WiFi QR codes in private or semi-private locations. Anyone who photographs the printed code can use it to connect.

---

## 3. How to Create a Contact (vCard) QR Code

**What this does:** Encodes a contact card — name, phone number, and optionally email — into a QR code. Scanning it prompts the phone to add the contact directly.

**When to use it:** Business cards, name badges, conference booths, or email signatures where you want people to save your contact with one scan.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/qr-generator
```

**Step 2 — Generate the vCard QR code.**

```bash
python3 main.py vcard 'Jane Smith' '+1 415 555 0001' 'jane@mycompany.com' ~/Desktop/jane-contact.png
```

Output:
```
✅ vCard QR code generated: /home/user/Desktop/jane-contact.png
   Name: Jane Smith
```

**Step 3 — Test the contact scan.**  
Open the PNG and scan it with your phone. You should see a contact prompt with Jane's name, phone, and email.

**Step 4 — Add to your business card or email signature.**  
Include the PNG in your business card design, or embed it in a Canva/Word template.

**Result:** Anyone who scans your QR code immediately gets a prompt to save your contact info — no typing, no typos.

---

## 4. How to Create a Phone or SMS QR Code

**What this does:** `phone` creates a QR that initiates a call. `sms` creates a QR that opens a pre-addressed text message (with optional pre-filled text).

**When to use it:** Customer service signs, storefront displays, or any place where you want people to reach you with one scan.

### Steps — Phone QR

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/qr-generator
```

**Step 2 — Generate a call QR code.**

```bash
python3 main.py phone '+12125550001' ~/Desktop/call-us.png
```

Output:
```
✅ Phone QR code generated: /home/user/Desktop/call-us.png
   Phone: +12125550001
```

Scanning this opens the phone dialer with your number pre-entered.

---

### Steps — SMS QR

**Step 1 — Generate an SMS QR code with a pre-filled message.**

```bash
python3 main.py sms '+12125550001' 'Hi, I have a question about your product.' ~/Desktop/text-us.png
```

Output:
```
✅ SMS QR code generated: /home/user/Desktop/text-us.png
   Phone: +12125550001
```

**Step 2 — Test it.**  
Scan with your phone — it should open Messages (or your default SMS app) with the number pre-filled and the message already typed.

**Result:** A QR code for instant phone or SMS contact.

---

## 5. How to Create an Email QR Code

**What this does:** Generates a QR code that opens a new email pre-addressed to a specific email address.

**When to use it:** Conference badges, contact forms on printed materials, "email us" QR codes on packaging.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/qr-generator
```

**Step 2 — Generate the email QR.**

```bash
python3 main.py email support@mycompany.com ~/Desktop/email-us.png
```

Output:
```
✅ Email QR code generated: /home/user/Desktop/email-us.png
   Email: support@mycompany.com
```

**Step 3 — Verify by scanning.**  
Should open your phone's email app with `support@mycompany.com` in the To field.

**Result:** A QR code that lets anyone send you an email with a single scan.

---

## 6. Automating with Cron

You can schedule QR code generation automatically — for example, regenerating a QR code each month if your URL changes (like a monthly calendar link).

### Open the cron editor

```bash
crontab -e
```

### Example: Regenerate a monthly link QR code on the 1st

```bash
0 8 1 * * python3 /home/yourname/smfworks-skills/skills/qr-generator/main.py url "https://mycompany.com/calendar/$(date +\%Y-\%m)" /home/yourname/Desktop/monthly-qr.png >> /home/yourname/logs/qr-generator.log 2>&1
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 8 1 * *` | First day of each month at 8 AM |
| `0 9 * * 1` | Every Monday at 9 AM |
| `0 7 * * *` | Every day at 7 AM |

### Create the log directory

```bash
mkdir -p ~/logs
```

---

## 7. Combining with Other Skills

**QR Generator + File Organizer:** Generate multiple QR codes and then organize them by date:

```bash
python3 ~/smfworks-skills/skills/qr-generator/main.py url https://event1.com ~/QR-codes/event1.png
python3 ~/smfworks-skills/skills/qr-generator/main.py url https://event2.com ~/QR-codes/event2.png
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-date ~/QR-codes/
```

---

## 8. Troubleshooting Common Issues

### `qrcode not installed. Run: pip install qrcode[pil]`

The package is missing.  
**Fix:** `pip install "qrcode[pil]"` (quotes are important in some shells).

---

### `Error: Data too long (max 2000 characters)`

Your URL or data exceeds 2,000 characters.  
**Fix:** Use a URL shortener (bit.ly, tinyurl.com) to shorten the URL before passing it to the command.

---

### `Error: Data contains invalid characters`

Your input contains shell special characters (`;`, `|`, `&`, `$`, newlines).  
**Fix:** Use single quotes around arguments: `python3 main.py wifi 'My;Network' 'pass&word'`

---

### `Error: Only http, https, mailto, and tel URLs are allowed`

You used a URL scheme other than the four supported ones.  
**Fix:** Only `http://`, `https://`, `mailto:`, and `tel:` are accepted. For other schemes, use the `url` command with the data as text.

---

### `Error: Phone number contains invalid characters`

The phone number has letters or symbols other than `+`, `-`, spaces, and parentheses.  
**Fix:** Strip non-numeric characters: `+1 (212) 555-1234` is fine; `extension:4` is not.

---

### The QR code won't scan

Possible causes: the image is too small when printed, or the error correction level isn't enough for the print quality.  
**Fix:** Print at least 2×2 cm. Ensure good contrast (black on white). If scanning from a screen, try zooming in on the image.

---

## 9. Tips & Best Practices

**Use single quotes for arguments with spaces or special characters.** `python3 main.py wifi 'My Network' 'p@ssw0rd'` — double quotes work too, but single quotes are safer for special characters.

**Always test by scanning before printing.** Generate the QR, scan it on your phone, confirm it does what you expect. Printing and distributing an untested QR code is a common mistake.

**For WiFi QR codes, print large enough to scan from a comfortable distance.** 3–4 inches square is ideal for wall-mounted use.

**For business card QR codes, use vcard not url.** The vCard format prompts the phone to add a contact, which is more useful than just opening a website.

**For URL QR codes, prefer short URLs.** Shorter URLs produce smaller QR codes with fewer dots, making them easier to scan at small sizes. Use a URL shortener for long links.

**PNG works for most uses; SVG is better for print design.** PNGs can get pixelated when scaled up. If you're inserting the QR code into a design that might be resized, use `.svg` output:
```bash
python3 main.py url https://mysite.com mysite-qr.svg
```

**Store your QR codes in a named folder.** If you generate QR codes regularly, keep them organized:
```bash
mkdir -p ~/QR-codes
python3 main.py wifi 'HomeNet' 'pass123' ~/QR-codes/home-wifi.png
```
