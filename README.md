# SMF Works Skills

A collection of productivity skills for OpenClaw. Free skills for everyday tasks. Premium skills for business automation.

## 🚀 Quick Start

```bash
# Install SMF CLI (one-time setup)
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash

# Install a free skill
smf install file-organizer

# Run it
smf run file-organizer organize-date ~/Downloads
```

## 📦 Installation

### Option 1: One-Liner Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash
```

Then reload your shell or run:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

### Option 2: Manual Install

```bash
# Clone repository
git clone https://github.com/smfworks/smfworks-skills.git
cd smfworks-skills

# Install CLI
cp cli/smf ~/.local/bin/
chmod +x ~/.local/bin/smf

# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

## 🎁 Free Skills (No Subscription)

Install and use immediately. No account required.

| Skill | Description | Install |
|-------|-------------|---------|
| **file-organizer** | Organize files by date, type, find duplicates | `smf install file-organizer` |
| **pdf-toolkit** | Merge, split, extract, compress PDFs | `smf install pdf-toolkit` |
| **text-formatter** | Case conversion, word count, clean whitespace | `smf install text-formatter` |
| **qr-generator** | QR codes for URLs, WiFi, vCard, email | `smf install qr-generator` |
| **system-monitor** | Disk, memory, CPU monitoring | `smf install system-monitor` |
| **website-checker** | Check site status, SSL certificates | `smf install website-checker` |
| **csv-converter** | CSV↔JSON, CSV↔Excel conversion | `smf install csv-converter` |
| **image-resizer** | Resize, compress, batch images | `smf install image-resizer` |
| **password-generator** | Strong passwords, passphrases | `smf install password-generator` |
| **markdown-converter** | Markdown to HTML, text, TOC | `smf install markdown-converter` |

### Usage Examples

```bash
# Install and run
smf install file-organizer
smf run file-organizer organize-date ~/Downloads

# See skill help
smf run file-organizer --help

# List installed skills
smf list

# Search available skills
smf search
```

## 💎 Premium Skills (Pro Subscription)

This is a paid skill that is part of the SMF Works subscription service. One monthly fee for unlimited access to the growing library of premium SMF Skills and applications.

**Price:** $19.99/month (locked forever at signup rate)

### Install Premium Skill

```bash
# 1. Subscribe at https://smf.works/subscribe
# 2. Login
smf login

# 3. Install premium skill
smf install lead-capture

# 4. Run it
smf run lead-capture capture
```

### Available Premium Skills

| Skill | Description | Docs |
|-------|-------------|------|
| **lead-capture** | Capture, qualify, and manage leads | [Setup Guide](skills/lead-capture/SETUP.md) |

### Coming Soon
- Simple CRM
- Email Campaign Manager
- Social Media Scheduler
- Booking Engine
- Invoice Generator

## 🔧 SMF CLI Commands

```
smf install <skill>       # Install a skill
smf uninstall <skill>    # Remove a skill
smf run <skill> [args]    # Run a skill
smf list                   # List installed skills
smf search                 # Search available skills
smf update                 # Update all skills
smf login                  # Authenticate for Pro
smf logout                 # Remove authentication
smf status                 # Show subscription status
smf help                   # Show help
```

## 🏗️ Architecture

- **Free Skills:** Run locally, no auth required, forever free
- **Pro Skills:** Require SMF Works subscription ($19.99/mo)
- **Auth System:** JWT tokens, local validation, offline support
- **Data:** Stored locally, never leaves your machine

**See:** [docs/AUTH_SYSTEM.md](docs/AUTH_SYSTEM.md) for auth architecture

## 📁 Repository Structure

```
smfworks-skills/
├── cli/
│   ├── smf                      # Main CLI (unified interface)
│   └── smf_login.py             # Authentication helper
├── docs/
│   ├── AUTH_SYSTEM.md           # Auth documentation
│   └── SUBSCRIPTION_ARCHITECTURE.md
├── install.sh                   # One-liner installer
├── shared/
│   └── smf_auth.py              # Shared auth library
├── skills/
│   ├── csv-converter/
│   ├── file-organizer/
│   ├── image-resizer/
│   ├── lead-capture/            # Pro skill
│   ├── markdown-converter/
│   ├── password-generator/
│   ├── pdf-toolkit/
│   ├── qr-generator/
│   ├── system-monitor/
│   ├── text-formatter/
│   └── website-checker/
└── templates/
    └── pro_skill_template.py    # Template for Pro skills
```

## 📝 License

- **Free Skills:** MIT License
- **Pro Skills:** See SMF Works Terms of Service
- **Auth System:** Proprietary (SMF Works)

---

*Built by SMF Works | https://smf.works*
