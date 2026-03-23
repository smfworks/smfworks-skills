# Email Campaign — How-To Guide

**Prerequisites:** SMF Works Pro active. SMTP credentials configured. Setup complete (see SETUP.md).

---

## Table of Contents

1. [How to Create a Campaign](#1-how-to-create-a-campaign)
2. [How to Write Your Campaign Body](#2-how-to-write-your-campaign-body)
3. [How to Preview Send with Dry Run](#3-how-to-preview-send-with-dry-run)
4. [How to Send a Campaign](#4-how-to-send-a-campaign)
5. [How to Check Campaign Statistics](#5-how-to-check-campaign-statistics)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Create a Campaign

**What this does:** Sets up a new campaign with a name, subject line, and from address.

### Steps

**Step 1 — Navigate to the skill.**

```bash
cd ~/smfworks-skills/skills/email-campaign
```

**Step 2 — Create interactively.**

```bash
python3 main.py create
```

```
Campaign name: March Newsletter
Subject line: Your March Update — What's New This Month
From email: hello@mycompany.com
Template (default/newsletter): newsletter

✅ Campaign created: march-newsletter-20240315
```

**Step 3 — Or create with flags.**

```bash
python3 main.py create --name "March Newsletter" --subject "Your March Update" --from hello@mycompany.com --template newsletter
```

**Result:** Campaign is created. Next step: write the body.

---

## 2. How to Write Your Campaign Body

**What this does:** Edits the campaign's email body text.

**Step 1 — Find the campaign body file.**

```bash
ls ~/.smf/campaigns/
```

**Step 2 — Edit the body.**

```bash
nano ~/.smf/campaigns/march-newsletter-20240315/body.txt
```

Or use any text editor. The body supports personalization placeholders:

| Placeholder | Replaced with |
|-------------|---------------|
| `{{name}}` | Recipient's name |
| `{{email}}` | Recipient's email |
| `{{company}}` | Recipient's company |

Example body:
```
Hi {{name}},

Here's your March update from Acme Corp.

This month we launched our new Pro tier with 14 powerful skills...

Best,
The Acme Team

---
To unsubscribe: [unsubscribe link automatically added]
```

**Step 3 — Save the file.**

The unsubscribe link is added automatically to every email — you don't need to include it manually.

---

## 3. How to Preview Send with Dry Run

**What this does:** Shows exactly what the send would do — recipient count, timing estimate, first few recipients — without sending any actual emails.

### Steps

**Step 1 — Run dry run (no --send flag).**

```bash
python3 main.py send --campaign march-newsletter-20240315 --list ~/subscribers.csv
```

Output:
```
📧 Campaign: March Newsletter
   Subject: Your March Update — What's New This Month
   Recipients: 247
   From: hello@mycompany.com

[DRY RUN] Would send to:
  1. alice@example.com (Alice, Acme Corp)
  2. bob@techco.io (Bob, TechCo)
  3. carol@startup.io (Carol, Startup Inc)
  ... and 244 more

Rate limiting: 1.5s between emails
Estimated send time: 6 min 10 sec
```

**Step 2 — Verify everything looks correct.**

- Correct recipient count?
- Subject line looks right?
- Estimated time acceptable?

**Result:** Zero risk preview — no emails sent.

---

## 4. How to Send a Campaign

**What this does:** Actually sends the campaign to your subscriber list.

**Only run this when you're confident the dry run looked correct.**

```bash
python3 main.py send --campaign march-newsletter-20240315 --list ~/subscribers.csv --send
```

Output:
```
📧 Sending campaign: March Newsletter
   Recipients: 247

   Sending 1/247: alice@example.com... ✅
   Sending 2/247: bob@techco.io... ✅
   Sending 3/247: carol@startup.io... ✅
   ...

✅ Campaign sent!
   Sent: 247
   Errors: 0
   Time: 6m 18s
```

---

## 5. How to Check Campaign Statistics

```bash
python3 main.py stats --campaign march-newsletter-20240315
```

Output:
```
📊 Campaign Statistics: March Newsletter

Sent: 247
Errors: 3
Success rate: 98.8%
Send time: 6m 18s
Campaign ID: march-newsletter-20240315
```

---

## 6. Automating with Cron

### Example: Monthly newsletter on the 1st at 9 AM

```bash
0 9 1 * * cd /home/yourname/smfworks-skills/skills/email-campaign && python3 main.py send --campaign monthly-newsletter-$(date +\%Y\%m) --list /home/yourname/subscribers.csv --send >> /home/yourname/logs/email-campaign.log 2>&1
```

**Note:** You must create the campaign and write the body before the cron job runs.

---

## 7. Combining with Other Skills

**Email Campaign + Report Generator:** Generate a monthly report and include it in an email:

```bash
python3 ~/smfworks-skills/skills/report-generator/main.py create --data ~/Data/sales.csv --format text --title "March Report" > /tmp/report.txt
# Add the text content to your campaign body, then send
python3 main.py send --campaign march-newsletter --list ~/subscribers.csv --send
```

---

## 8. Troubleshooting Common Issues

### `SMTP Authentication Failed`

**Fix:** Verify SMTP credentials are set as environment variables. For Gmail, use an App Password — not your regular Gmail password.

### High error rate during send

Some recipients may have invalid addresses or full mailboxes.  
**Fix:** Run `stats` to see how many errors occurred. Clean your subscriber list periodically — remove bounced addresses.

### Emails going to spam

**Fix:**
1. Ensure your From address is from a real domain you own
2. Verify SPF and DKIM records for your domain
3. Use a reputable SMTP provider (SendGrid, Mailgun)
4. Avoid spam trigger words in your subject line

### `Campaign not found`

**Fix:** Check campaign ID with `python3 main.py list`. IDs are case-sensitive.

---

## 9. Tips & Best Practices

**Always dry run first.** Even for campaigns you've sent before, a dry run confirms the correct recipient count and subject line before the real send.

**Test with yourself first.** Send to a test list containing only your email address before the real send: `python3 main.py send --campaign ID --list test.csv --send`

**Keep subscriber lists clean.** Remove bounced addresses after each campaign. Sending to invalid addresses repeatedly hurts your sender reputation.

**Use descriptive campaign names.** `newsletter-2024-03` is better than `campaign-1`. It makes the `list` output readable and helps with `stats` queries.

**Respect unsubscribes.** The skill adds an unsubscribe notice to every email. Maintain a list of unsubscribed addresses and remove them from your CSV before each send.

**Don't send more than 500 emails/day on Gmail.** Gmail's free SMTP limit is ~500 emails/day. For larger lists, use SendGrid (free: 100/day, paid: higher limits) or Mailgun.
