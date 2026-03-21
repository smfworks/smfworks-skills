# Daily News Digest - Setup Guide

## Prerequisites

- OpenClaw installed and running
- SMF CLI installed (`smf` command available)
- Internet connection
- NewsAPI.org account (free)

---

## Quick Setup (5 minutes)

### 1. Get Your API Key

```bash
# Visit the registration page
open https://newsapi.org/register
```

Or manually:
1. Go to **https://newsapi.org/register**
2. Enter your email and create a password
3. Verify your email address
4. Log in to the dashboard
5. Copy your API key (starts with a long string of letters/numbers)

### 2. Install the Skill

```bash
smf install daily-news-digest
```

### 3. Configure

```bash
smf run daily-news-digest --configure
```

Follow the prompts:
- Paste your API key
- Choose categories (e.g., `business,technology`)
- Set country code (e.g., `us`)
- Set articles per category (default: 5)

### 4. Test

```bash
smf run daily-news-digest
```

You should see a formatted news digest in your terminal.

---

## Scheduling Options

### Option A: OpenClaw Cron (Recommended)

Add to your OpenClaw configuration:

```json
{
  "name": "daily-news-digest",
  "schedule": { "kind": "cron", "expr": "30 6 * * *", "tz": "America/New_York" },
  "payload": { "kind": "systemEvent", "text": "smf run daily-news-digest" },
  "sessionTarget": "main"
}
```

Or use the CLI:

```bash
openclaw cron add \
  --name "daily-news-digest" \
  --schedule "30 6 * * *" \
  --command "smf run daily-news-digest"
```

### Option B: System Cron

Add to your crontab:

```bash
# Edit crontab
crontab -e

# Add this line for 6:30 AM daily
30 6 * * * /usr/local/bin/smf run daily-news-digest >> ~/.config/smf/skills/daily-news-digest/cron.log 2>&1
```

### Option C: OpenClaw Heartbeat

Add to your `HEARTBEAT.md`:

```markdown
## Daily Tasks

- [ ] 6:30 AM - Run daily news digest
```

Then configure OpenClaw to check at 6:30 AM.

---

## Verification

### Check Installation

```bash
smf list | grep daily-news-digest
```

### Check Configuration

```bash
cat ~/.config/smf/skills/daily-news-digest/config.json
```

### Test API Key

```bash
smf run daily-news-digest --output json
```

Should return JSON with news articles.

---

## Customization

### Change Categories

Edit the config file:

```bash
nano ~/.config/smf/skills/daily-news-digest/config.json
```

Valid categories:
- `business`
- `technology`
- `science`
- `health`
- `sports`
- `entertainment`
- `general`

### Change Schedule

Update your cron job:

```bash
# List current cron jobs
openclaw cron list

# Update the schedule
openclaw cron update daily-news-digest --schedule "0 7 * * *"
```

---

## Troubleshooting

### Installation Issues

**"Command not found: smf"**
```bash
# Make sure SMF CLI is installed
curl -fsSL https://raw.githubusercontent.com/smfworks/smfworks-skills/main/install.sh | bash
```

**"Permission denied"**
```bash
chmod +x ~/.local/bin/smf
```

### Configuration Issues

**"No API key configured"**
- Run `smf run daily-news-digest --configure` again
- Check the config file exists: `ls ~/.config/smf/skills/daily-news-digest/`

**"Invalid API key"**
- Log in to https://newsapi.org and verify your key
- Copy/paste the key carefully (no extra spaces)

### Runtime Issues

**"No articles found"**
- Check your categories are valid (see list above)
- Try `general` category which always has content
- Check your internet connection

**"API rate limit exceeded"**
- Free tier: 100 requests/day
- Wait 24 hours, or upgrade at NewsAPI.org
- Check if you have multiple scheduled runs

---

## Next Steps

1. **Verify it works:** Run `smf run daily-news-digest`
2. **Set schedule:** Configure cron for automatic delivery
3. **Customize:** Adjust categories to your interests
4. **Integrate:** Pipe output to notifications (see below)

### Send to Notifications

To get the digest via WhatsApp/Telegram:

```bash
# Add to your OpenClaw cron payload
{
  "kind": "systemEvent",
  "text": "smf run daily-news-digest | send-to-whatsapp"
}
```

Or use OpenClaw's messaging integration directly.

---

## Support

- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **Documentation:** https://smfworks.com/skills/daily-news-digest
- **NewsAPI Help:** https://newsapi.org/docs

---

*Setup complete! Enjoy your daily news briefing.*
