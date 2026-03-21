# SMF Works Skills

A collection of productivity skills for OpenClaw. Free skills for everyday tasks. Premium skills for business automation.

## 🎁 Free Skills (No Subscription Required)

Free forever. No auth needed. Just works.

### 1. File Organizer
Organize files by date, type, and find duplicates.
```bash
python skills/file-organizer/main.py organize-date ~/Downloads
python skills/file-organizer/main.py organize-type ~/Documents
python skills/file-organizer/main.py find-duplicates ~/Pictures
```

### 2. PDF Toolkit
Merge, split, extract, compress, and rotate PDFs.
```bash
python skills/pdf-toolkit/main.py merge output.pdf doc1.pdf doc2.pdf
python skills/pdf-toolkit/main.py split document.pdf ./pages/
python skills/pdf-toolkit/main.py info contract.pdf
```

### 3. Text Formatter
Convert case, clean whitespace, count words and characters.
```bash
python skills/text-formatter/main.py case upper "hello world"
python skills/text-formatter/main.py clean document.txt
python skills/text-formatter/main.py count article.txt
```

### 4. QR Generator
Generate QR codes for URLs, WiFi, email, phone, vCard, and SMS.
```bash
python skills/qr-generator/main.py url "https://smf.works" qr-code.png
python skills/qr-generator/main.py wifi MyNetwork password123 WPA wifi-qr.png
python skills/qr-generator/main.py vcard "John Doe" john@example.com 555-0199 vcard.png
```

### 5. System Monitor
Monitor disk usage, memory, CPU, and find large files.
```bash
python skills/system-monitor/main.py disk
python skills/system-monitor/main.py memory
python skills/system-monitor/main.py health
python skills/system-monitor/main.py large-files ~/Downloads 10
```

### 6. Website Checker
Check website status, response time, and SSL certificates.
```bash
python skills/website-checker/main.py check https://google.com
python skills/website-checker/main.py ssl smf.works
python skills/website-checker/main.py bulk https://google.com https://github.com
```

### 7. CSV Converter
Convert between CSV, JSON, and Excel formats.
```bash
python skills/csv-converter/main.py csv-to-json data.csv output.json
python skills/csv-converter/main.py json-to-csv data.json output.csv
python skills/csv-converter/main.py csv-to-excel data.csv output.xlsx
python skills/csv-converter/main.py preview data.csv 10
```

### 8. Image Resizer
Resize, compress, convert, and batch process images.
```bash
python skills/image-resizer/main.py resize photo.jpg resized.jpg 800
python skills/image-resizer/main.py compress photo.jpg compressed.jpg 85
python skills/image-resizer/main.py convert photo.jpg photo.png
python skills/image-resizer/main.py batch-resize ./photos ./resized 800
```

### 9. Password Generator
Generate strong passwords, memorable passphrases, and check strength.
```bash
python skills/password-generator/main.py password 16
python skills/password-generator/main.py passphrase 4
python skills/password-generator/main.py check mypassword123
```

### 10. Markdown Converter
Convert Markdown to HTML, plain text, and extract table of contents.
```bash
python skills/markdown-converter/main.py to-html document.md output.html
python skills/markdown-converter/main.py to-text document.md output.txt
python skills/markdown-converter/main.py toc document.md
python skills/markdown-converter/main.py stats document.md
```

---

## 💎 Premium Skills (Pro Subscription)

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

**Price:** $19.99/month (locked forever at signup rate)

### 11. Lead Capture System
Capture, qualify, and manage sales leads with automatic scoring.

```bash
# Authenticate first
python cli/smf_login.py login

# Then use the skill
python skills/lead-capture/main.py capture
python skills/lead-capture/main.py list
python skills/lead-capture/main.py export csv
python skills/lead-capture/main.py stats
```

**See full documentation:** [skills/lead-capture/SETUP.md](skills/lead-capture/SETUP.md)

### Coming Soon
- Simple CRM
- Email Campaign Manager
- Social Media Scheduler
- Booking Engine
- Invoice Generator

---

## Installation

### Free Skills
```bash
git clone https://github.com/smfworks/smfworks-skills.git
cd smfworks-skills/skills/<skill-name>
python main.py --help
```

### Premium Skills
```bash
# 1. Subscribe at https://smf.works/subscribe
# 2. Login
python cli/smf_login.py login
# 3. Run premium skill
python skills/lead-capture/main.py capture
```

---

## Architecture

- **Free Skills:** Run locally, no auth required, forever free
- **Pro Skills:** Require SMF Works subscription ($19.99/mo)
- **Auth System:** JWT tokens, local validation, offline support
- **Data:** Stored locally, never leaves your machine

**See:** [docs/AUTH_SYSTEM.md](docs/AUTH_SYSTEM.md) for auth architecture details

---

## Repository Structure

```
smfworks-skills/
├── cli/                          # Authentication CLI
│   └── smf_login.py
├── docs/
│   ├── AUTH_SYSTEM.md             # Auth documentation
│   └── SUBSCRIPTION_ARCHITECTURE.md
├── shared/
│   └── smf_auth.py               # Shared auth library
├── skills/
│   ├── csv-converter/
│   ├── file-organizer/
│   ├── image-resizer/
│   ├── lead-capture/             # Pro skill
│   ├── markdown-converter/
│   ├── password-generator/
│   ├── pdf-toolkit/
│   ├── qr-generator/
│   ├── system-monitor/
│   ├── text-formatter/
│   └── website-checker/
└── templates/
    └── pro_skill_template.py     # Template for Pro skills
```

---

## License

- **Free Skills:** MIT License
- **Pro Skills:** See SMF Works Terms of Service
- **Auth System:** Proprietary (SMF Works)

---

*Built by SMF Works | https://smf.works*
