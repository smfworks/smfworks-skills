# Email Campaign — Setup Guide

**Estimated setup time:** 10–15 minutes  
**Difficulty:** Easy to Moderate  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| SMTP credentials | Gmail, SendGrid, Mailgun, or any SMTP provider | Varies |
| Subscriber CSV | List of recipients | Free to create |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

Visit [smfworks.com/subscribe](https://smfworks.com/subscribe).

```bash
openclaw auth status
```

---

## Step 2 — Choose and Configure Your SMTP Provider

You need an SMTP server to send emails. Choose one:

### Option A — Gmail (easiest for personal use)

1. Enable 2-Step Verification on your Google account
2. Generate an App Password: myaccount.google.com/apppasswords → Select "Mail"
3. Copy the 16-character app password

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587
export SMTP_USER=your-email@gmail.com
export SMTP_PASS=your-16-char-app-password
```

**Gmail free tier:** 500 emails/day.

### Option B — SendGrid (better for higher volume)

1. Create account at sendgrid.com (free tier: 100 emails/day)
2. Create an API key (Settings → API Keys)

```bash
export SMTP_HOST=smtp.sendgrid.net
export SMTP_PORT=587
export SMTP_USER=apikey
export SMTP_PASS=your-sendgrid-api-key
```

### Option C — Any SMTP server

```bash
export SMTP_HOST=mail.yourhost.com
export SMTP_PORT=587
export SMTP_USER=your-username
export SMTP_PASS=your-password
```

---

## Step 3 — Make SMTP Credentials Persistent

Add to `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export SMTP_HOST=smtp.gmail.com' >> ~/.bashrc
echo 'export SMTP_PORT=587' >> ~/.bashrc
echo 'export SMTP_USER=your@gmail.com' >> ~/.bashrc
echo 'export SMTP_PASS=your-app-password' >> ~/.bashrc
source ~/.bashrc
```

---

## Step 4 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 5 — Navigate and Verify

```bash
cd ~/smfworks-skills/skills/email-campaign
python3 main.py help
```

---

## Step 6 — Create a Sample List and Test

```bash
python3 main.py sample-list --output /tmp/test-list.csv
cat /tmp/test-list.csv
```

Expected:
```csv
email,name,company
test@example.com,Test User,Test Corp
sample@example.com,Sample User,Sample Inc
```

---

## Step 7 — Create a Test Campaign and Dry Run

```bash
python3 main.py create --name "Test Campaign" --subject "Test Email"
```

```bash
python3 main.py send --campaign test-campaign-$(date +%Y%m%d) --list /tmp/test-list.csv
```

The dry run shows what would be sent without actually sending.

---

## Troubleshooting

**`SMTP Authentication Failed`** — For Gmail, use an App Password (not your regular password). Verify environment variables are set correctly.

**`Connection refused`** — Check your SMTP_HOST and SMTP_PORT. Port 587 (STARTTLS) is standard; port 465 (SSL) is the alternative.

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

---

## Next Steps

Setup complete. See **HOWTO.md** for creating campaigns, sending, and monitoring.
