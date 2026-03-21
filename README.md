# SMF Works Skills

A curated collection of productivity skills for OpenClaw — from everyday utilities to business automation tools.

**21 Skills Total:** 11 Free (forever) + 10 Pro (subscription)

---

## 🚀 Quick Start

```bash
# Install SMF CLI (one-time setup)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Install any skill
smf install file-organizer        # Free
smf install lead-capture          # Pro (requires subscription)

# Run it
smf run file-organizer organize-date ~/Downloads
```

---

## 🎁 Free Skills (11)

No subscription required. No auth needed. Just works.

| # | Skill | Description | Install |
|---|-------|-------------|---------|
| 1 | **File Organizer** | Organize files by date, type, find duplicates | `smf install file-organizer` |
| 2 | **PDF Toolkit** | Merge, split, extract, compress, rotate PDFs | `smf install pdf-toolkit` |
| 3 | **Text Formatter** | Case conversion, word count, clean whitespace | `smf install text-formatter` |
| 4 | **QR Generator** | Generate QR codes for URLs, WiFi, vCard, email | `smf install qr-generator` |
| 5 | **System Monitor** | Monitor disk, memory, CPU, find large files | `smf install system-monitor` |
| 6 | **Website Checker** | Check site status, SSL certificates, response time | `smf install website-checker` |
| 7 | **CSV Converter** | Convert between CSV, JSON, Excel formats | `smf install csv-converter` |
| 8 | **Image Resizer** | Resize, compress, convert, batch process images | `smf install image-resizer` |
| 9 | **Password Generator** | Strong passwords, passphrases, strength check | `smf install password-generator` |
| 10 | **Markdown Converter** | Convert Markdown to HTML, text, extract TOC | `smf install markdown-converter` |
| 11 | **Daily News Digest** | Curated news delivered daily to your interests | `smf install daily-news-digest` |

---

## 💎 Pro Skills (10)

Premium skills for business automation. Requires SMF Works subscription ($19.99/mo, price locked at signup).

| # | Skill | Description | Install |
|---|-------|-------------|---------|
| 11 | **Lead Capture** | Capture, qualify, and manage sales leads | `smf install lead-capture` |
| 12 | **Database Backup** | Backup SQLite, PostgreSQL, MySQL with compression | `smf install database-backup` |
| 13 | **Report Generator** | Create business reports from CSV/JSON data | `smf install report-generator` |
| 14 | **Email Campaign** | Create and send email campaigns with tracking | `smf install email-campaign` |
| 15 | **Task Manager** | Kanban project management with deadlines | `smf install task-manager` |
| 16 | **Self-Improvement** | Log errors and learnings for continuous improvement | `smf install self-improvement` |
| 17 | **Invoice Generator** | Create professional invoices, track payments | `smf install invoice-generator` |
| 18 | **Form Builder** | Create forms, collect responses, export data | `smf install form-builder` |
| 19 | **Booking Engine** | Appointment scheduling with availability management | `smf install booking-engine` |
| 20 | **OpenClaw Optimizer** | Audit workspace for cost and performance optimization | `smf install openclaw-optimizer` |

---

## 📦 Installation

### One-Liner Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash
```

### Manual Install

```bash
# Clone repository
git clone https://github.com/smfworks/smfworks-skills.git

# Install CLI
cp smfworks-skills/cli/smf ~/.local/bin/
chmod +x ~/.local/bin/smf

# Add to PATH
export PATH="$HOME/.local/bin:$PATH"
```

---

## 🔐 Pro Subscription

Unlock all premium skills with one monthly fee.

**Price:** $19.99/month (locked forever at signup rate)

**Includes:**
- All 10 Pro skills
- Future Pro skill updates
- Priority support
- Business automation suite

**Subscribe:** https://smf.works/subscribe

**Login:**
```bash
smf login
# Paste your token from https://smf.works/dashboard
```

---

## 🛠️ SMF CLI Commands

```bash
smf install <skill>              # Install a skill
smf uninstall <skill>            # Remove a skill
smf run <skill> [args]           # Run a skill
smf list                         # List installed skills
smf search                       # Search available skills
smf login                        # Authenticate for Pro skills
smf logout                       # Remove authentication
smf status                       # Show subscription status
smf update                       # Update all skills
smf help                         # Show help
```

---

## 📂 Repository Structure

```
smfworks-skills/
├── cli/
│   ├── smf                      # Main CLI (unified interface)
│   └── smf_login.py             # Authentication helper
├── docs/
│   ├── AUTH_SYSTEM.md           # Authentication documentation
│   └── SUBSCRIPTION_ARCHITECTURE.md
├── install.sh                   # One-liner installer
├── shared/
│   └── smf_auth.py              # Shared auth library (Pro skills)
├── skills/
│   ├── booking-engine/
│   ├── csv-converter/
│   ├── database-backup/
│   ├── email-campaign/
│   ├── file-organizer/
│   ├── form-builder/
│   ├── image-resizer/
│   ├── invoice-generator/
│   ├── lead-capture/
│   ├── markdown-converter/
│   ├── openclaw-optimizer/
│   ├── password-generator/
│   ├── pdf-toolkit/
│   ├── qr-generator/
│   ├── report-generator/
│   ├── self-improvement/
│   ├── system-monitor/
│   ├── task-manager/
│   ├── text-formatter/
│   ├── website-checker/
│   └── ...                      # Each skill has main.py + README.md
└── templates/
    └── pro_skill_template.py    # Template for building Pro skills
```

---

## 🎯 Skill Categories

### File Operations
- **File Organizer** — Organize by date/type, find duplicates
- **PDF Toolkit** — Merge, split, extract, compress, rotate
- **Image Resizer** — Resize, compress, convert, batch
- **Markdown Converter** — Convert to HTML, text

### Data & Conversion
- **CSV Converter** — CSV ↔ JSON ↔ Excel
- **QR Generator** — URLs, WiFi, vCard, email, SMS
- **Text Formatter** — Case, whitespace, word count
- **Password Generator** — Strong passwords, passphrases

### System & Web
- **System Monitor** — Disk, memory, CPU, health
- **Website Checker** — Status, SSL, response time
- **OpenClaw Optimizer** — Workspace audit, performance

### Business & Productivity (Pro)
- **Lead Capture** — Qualify and manage leads
- **Task Manager** — Kanban project management
- **Invoice Generator** — Professional invoicing
- **Form Builder** — Create forms, collect data
- **Booking Engine** — Appointment scheduling
- **Report Generator** — Business reports with charts
- **Email Campaign** — Send newsletters, track opens
- **Database Backup** — Automated DB backups
- **Self-Improvement** — Log errors and learnings

### News & Information
- **Daily News Digest** — Curated news delivered daily (requires NewsAPI key)

---

## 🔧 Skill Usage Examples

### File Organizer
```bash
smf run file-organizer organize-date ~/Downloads
smf run file-organizer organize-type ~/Documents
smf run file-organizer find-duplicates ~/Pictures
```

### PDF Toolkit
```bash
smf run pdf-toolkit merge output.pdf doc1.pdf doc2.pdf
smf run pdf-toolkit split document.pdf ./pages/
smf run pdf-toolkit compress large.pdf small.pdf
```

### Lead Capture (Pro)
```bash
smf run lead-capture capture
smf run lead-capture list
smf run lead-capture export csv
smf run lead-capture stats
```

### Task Manager (Pro)
```bash
smf run task-manager project add "Website Redesign"
smf run task-manager task add "Fix bug" --project Website --priority high
smf run task-manager board --project Website
smf run task-manager task move TASK-ABC --to done
```

### Form Builder (Pro)
```bash
smf run form-builder create --name "Contact Form" --fields name,email,message
smf run form-builder serve FORM-ABC --port 8080
smf run form-builder responses FORM-ABC
smf run form-builder export FORM-ABC --format csv
```

---

## 🏗️ Architecture

### Free Skills
- Run locally, no auth required
- Forever free
- Self-contained Python scripts
- Use standard libraries where possible

### Pro Skills
- Require SMF Works subscription ($19.99/mo)
- JWT token validation
- Offline-capable with cached validation
- Import `smf_auth` for subscription checking

### Authentication Flow
1. User subscribes at https://smf.works/subscribe
2. JWT token issued via Stripe webhook
3. User runs `smf login` → token saved to `~/.smf/token`
4. Pro skills validate token locally (RS256)
5. Token expires → renewal required

---

## 🤝 Contributing

SMF Works builds and maintains all skills. No external contributors (keeps quality high, support manageable).

**Report issues:** https://github.com/smfworks/smfworks-skills/issues

---

## 📜 License

- **Free Skills:** MIT License
- **Pro Skills:** See SMF Works Terms of Service
- **Auth System:** Proprietary (SMF Works)

---

## 🔗 Links

- **Website:** https://smf.works
- **Subscribe:** https://smf.works/subscribe
- **Repository:** https://github.com/smfworks/smfworks-skills
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Support:** support@smf.works

---

*Built by SMF Works | 20 Skills | Free + Pro | Local-First*
