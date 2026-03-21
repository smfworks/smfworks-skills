# Daily News Digest

**SMF Works OpenClaw Skill**

Get curated news headlines delivered daily — personalized to your interests.

---

## What It Does

Fetches top headlines from NewsAPI.org and formats them into a clean, readable digest. Perfect for your morning briefing or staying informed without the noise.

**Features:**
- Choose your news categories (business, technology, science, health, sports, entertainment)
- Set your country for local news
- Configure how many articles per category
- Clean, formatted output perfect for messaging

---

## Installation

```bash
smf install daily-news-digest
```

---

## Configuration

### Step 1: Get Your API Key

1. Visit **https://newsapi.org/register**
2. Create a free account
3. Copy your API key from the dashboard

**Free Tier:** 100 requests/day (plenty for daily digest)

### Step 2: Configure the Skill

```bash
smf run daily-news-digest --configure
```

You'll be prompted for:
- **API Key:** Your NewsAPI key
- **Categories:** Comma-separated (e.g., `business,technology,science`)
- **Country:** 2-letter code (e.g., `us`, `gb`, `ca`)
- **Articles per category:** Default 5

### Step 3: Test It

```bash
smf run daily-news-digest
```

---

## Usage

### Run Once

```bash
# Use saved configuration
smf run daily-news-digest

# Use different API key (one-time)
smf run daily-news-digest --api-key YOUR_KEY_HERE

# Output as JSON
smf run daily-news-digest --output json
```

### Schedule Daily (via OpenClaw Cron)

Add to your OpenClaw cron for automatic daily delivery:

```bash
# Every day at 6:30 AM
openclaw cron add --name "daily-news" --schedule "0 30 6 * * *" --command "smf run daily-news-digest"
```

Or via OpenClaw's cron tool:

```json
{
  "name": "daily-news-digest",
  "schedule": { "kind": "cron", "expr": "30 6 * * *", "tz": "America/New_York" },
  "payload": { "kind": "systemEvent", "text": "smf run daily-news-digest" }
}
```

---

## Example Output

```
📰 Daily News Digest
📅 Saturday, March 21, 2026

💼 BUSINESS
----------------------------------------
1. Tech Giants Report Strong Q1 Earnings
   📰 Wall Street Journal
   🔗 https://example.com/article1

2. Small Business Lending Reaches Record High
   📰 Bloomberg
   🔗 https://example.com/article2

💻 TECHNOLOGY
----------------------------------------
1. New AI Model Achieves Breakthrough Results
   📰 TechCrunch
   🔗 https://example.com/article3

...

—
Powered by NewsAPI.org | 10 articles
Configure: smf run daily-news-digest --configure
```

---

## Configuration File

Config is stored at:
```
~/.config/smf/skills/daily-news-digest/config.json
```

Example:
```json
{
  "api_key": "your_api_key_here",
  "categories": ["business", "technology", "science"],
  "country": "us",
  "max_articles": 5
}
```

---

## Troubleshooting

### "No API key configured"
Run `smf run daily-news-digest --configure` to set up your API key.

### "Invalid API key"
Double-check your key at https://newsapi.org/account

### "API rate limit exceeded"
Free tier allows 100 requests/day. If you hit this, wait 24 hours or upgrade at NewsAPI.org.

### No articles showing
- Check your category names are valid: `business`, `technology`, `science`, `health`, `sports`, `entertainment`, `general`
- Try a different country code
- Some categories may have limited content on weekends

---

## Data & Privacy

- Your API key is stored locally in `~/.config/smf/skills/`
- Config file has 600 permissions (owner read/write only)
- News content comes from NewsAPI.org
- SMF Works does not store or see your news preferences

---

## Support

- **Documentation:** https://smfworks.com/skills/daily-news-digest
- **Issues:** https://github.com/smfworks/smfworks-skills/issues
- **NewsAPI Docs:** https://newsapi.org/docs

---

*Part of the SMF Works OpenClaw Skills collection*
