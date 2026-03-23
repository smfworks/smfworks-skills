# Invoice Generator — Setup Guide

**Estimated setup time:** 5 minutes  
**Difficulty:** Easy  
**Tier:** Pro — requires SMF Works Pro subscription ($19.99/mo)

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| SMF Works Pro subscription | [smfworks.com/subscribe](https://smfworks.com/subscribe) | $19.99/mo |
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| OpenClaw | Installed and authenticated | Free |
| smfworks-skills repository | Cloned via git | Included |

---

## Step 1 — Subscribe and Authenticate

```bash
openclaw auth status
```

If not subscribed: [smfworks.com/subscribe](https://smfworks.com/subscribe)

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Navigate and Verify

```bash
cd ~/smfworks-skills/skills/invoice-generator
python3 main.py help
```

---

## Verify Your Setup

Add a test client and create an invoice:

```bash
python3 main.py client add "Test Client"
python3 main.py create --client "Test Client" --item "Test Service:100"
python3 main.py list
```

You should see your invoice listed with status `unpaid`.

---

## Data Storage

Invoices and client data are stored at: `~/.smf/invoices/`

This directory is created automatically on first use.

---

## Typical Invoicing Workflow

```
1. client add          → Add the client
2. create              → Create the invoice
3. export --html       → Export HTML to send
4. pay INV-ID          → Record payment when received
5. report --month      → Monthly financial review
```

---

## Troubleshooting

**`Error: SMF Works Pro subscription required`** — Subscribe at [smfworks.com/subscribe](https://smfworks.com/subscribe).

**`python3: command not found`** — Install Python 3.8+.

---

## Pro Subscription Benefits

Your $19.99/mo Pro subscription includes access to all 14 Pro skills including Invoice Generator. Manage all your Pro skills with the Skill Manager skill.

---

## Item Format Reference

When using `--item` to add line items to an invoice, the format is:

```
--item "Description:Amount"
```

Examples:
```
--item "Web Design:3000"
--item "Hourly Consulting (5 hrs):500"
--item "Monthly Retainer:1500.00"
--item "Expedite Fee:200"
```

Multiple `--item` flags can be used in one command:
```bash
python3 main.py create --client "Acme" --item "Design:3000" --item "SEO:500" --item "Hosting:150"
```

## Next Steps

Setup complete. See **HOWTO.md** for a complete invoicing walkthrough from client creation to financial reporting.
