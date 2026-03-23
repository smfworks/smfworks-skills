# Daily News Digest

> Get a curated daily news briefing with top headlines from your chosen categories — delivered straight to your terminal.

**Tier:** Free — no subscription required  
**Requires:** Free NewsAPI key from [newsapi.org](https://newsapi.org/register)  
**Version:** 1.0  
**Category:** Productivity / News

---

## What It Does

Daily News Digest is an OpenClaw skill that fetches today's top headlines from NewsAPI.org and prints them in a clean, readable digest format. Choose from seven news categories (business, technology, science, health, sports, entertainment, general), set your country, and control how many articles per category you see.

Run it once to read your morning news in the terminal. Schedule it via cron for an automatic daily briefing.

**What it does NOT do:** It does not provide full article text (only headlines, sources, and URLs), archive previous digests, send email notifications, or work without a NewsAPI key.

---

## Prerequisites

- [ ] **Python 3.8 or newer**
- [ ] **OpenClaw installed**
- [ ] **Free NewsAPI key** — get yours at [newsapi.org/register](https://newsapi.org/register) (free, no credit card)
- [ ] **No subscription required** — free tier skill
- [ ] **Internet connection required** to fetch news

---

## Installation

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
cd ~/smfworks-skills/skills/daily-news-digest
```

No additional packages needed — uses Python stdlib only.

---

## Getting Your Free NewsAPI Key

1. Go to [newsapi.org/register](https://newsapi.org/register)
2. Enter your name, email, and password
3. Confirm your email
4. Your API key is shown on your dashboard — it looks like: `a1b2c3d4e5f67890a1b2c3d4e5f67890`

The free plan allows 100 requests per day — plenty for daily personal use.

---

## Quick Start

Run the configuration wizard once to save your API key and preferences:

```bash
python3 main.py --configure
```

Then fetch your daily digest:

```bash
python3 main.py
```

Output:
```
📰 Daily News Digest — Friday, March 15, 2024
══════════════════════════════════════════════

💻 Technology
─────────────
1. Apple Announces New M3 Ultra Chip for Mac Pro
   Source: TechCrunch | techcrunch.com/...

2. OpenAI Releases GPT-5 with Improved Reasoning
   Source: The Verge | theverge.com/...

3. Google DeepMind Achieves New AI Benchmark
   Source: Wired | wired.com/...

💼 Business
────────────
1. Fed Signals Rate Hold Through Mid-2024
   Source: Reuters | reuters.com/...

2. Amazon Reports Record Q4 Earnings
   Source: Bloomberg | bloomberg.com/...
...

Configure: smf run daily-news-digest --configure
```

---

## Command Reference

### Default (no arguments)

Fetches and prints the news digest using your saved configuration.

**Usage:**
```bash
python3 main.py
```

**Requires:** Configuration saved via `--configure`, or API key in the `NEWSAPI_KEY` environment variable.

---

### `--configure` / `-c`

Interactive setup wizard. Prompts for your API key, categories, country, and article count. Saves everything to `~/.config/smf/skills/daily-news-digest/config.json`.

**Usage:**
```bash
python3 main.py --configure
```

**Walkthrough:**

```
Step 1: API Key
Enter your NewsAPI key: [enter your key]

Step 2: News Categories
Available: business, technology, science, health, sports, entertainment, general
Enter categories (comma-separated) [business,technology]: technology,science,health

Step 3: Country
Enter 2-letter country code (e.g., us, gb, ca, au)
Country [us]: us

Step 4: Articles per Category
Max articles per category [5]: 5

✅ Configuration saved to: /home/user/.config/smf/skills/daily-news-digest/config.json
Your Daily News Digest is ready!
Run: smf run daily-news-digest
```

---

### `--api-key KEY` / `-k KEY`

Pass your API key directly on the command line without saving it to a config file. Useful for one-off runs or testing.

**Usage:**
```bash
python3 main.py --api-key YOUR_API_KEY_HERE
```

---

### `--output` / `-o`

Choose output format: `text` (default) or `json`.

**Usage:**
```bash
python3 main.py --output json
```

**JSON output:**
```json
{
  "success": true,
  "timestamp": "2024-03-15T09:00:12.345678",
  "content": "...",
  "categories": ["technology", "business"]
}
```

---

## Use Cases

### 1. Morning news briefing in the terminal

```bash
python3 main.py
```

---

### 2. Get tech and science news only

Configure with `technology,science` as categories and run.

---

### 3. Pipe output to a file for later reading

```bash
python3 main.py > ~/today-news.txt
```

---

### 4. Get JSON output for piping to another script

```bash
python3 main.py --output json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['content'][:500])"
```

---

### 5. Automated daily briefing via cron (saves to file)

Schedule it via cron — see HOWTO.md for the full automation walkthrough.

---

## Configuration

Config file location: `~/.config/smf/skills/daily-news-digest/config.json`  
The file is chmod 600 (readable only by you) when created via `--configure`.

**Configuration options:**

| Setting | Description | Default | Options |
|---------|-------------|---------|---------|
| `api_key` | NewsAPI.org API key | — | Your free key |
| `categories` | News categories to fetch | `["business","technology"]` | business, technology, science, health, sports, entertainment, general |
| `country` | Country for top headlines | `"us"` | us, gb, ca, au, in, de, fr, etc. |
| `max_articles` | Articles per category | `5` | 1–20 |

**Alternative: environment variable**

Instead of the config file, set:
```bash
export NEWSAPI_KEY="your-api-key-here"
```

---

## Troubleshooting

### `Error: No API key configured.`
**Fix:** Run `python3 main.py --configure` to save your key, or set `export NEWSAPI_KEY=yourkey`.

### `HTTP Error 401: Unauthorized`
**Fix:** Your API key is invalid or expired. Double-check it at [newsapi.org/account](https://newsapi.org/account).

### `HTTP Error 429: Too Many Requests`
**Fix:** You've exceeded the free plan's 100 requests/day limit. Wait until tomorrow or upgrade your NewsAPI plan.

### `HTTP Error 426: Upgrade Required`
**Fix:** On the free NewsAPI plan, you can only use `/v2/top-headlines` with a country or sources parameter. The skill uses this endpoint correctly. If you see this error, verify your key is a free-tier key, not an expired trial.

### No articles returned for a category
Some categories have fewer articles available for certain countries.  
**Fix:** Try `country: us` or change to a category with more coverage (technology, business tend to have the most).

### `SSL: CERTIFICATE_VERIFY_FAILED`
**Fix:** Your system's SSL certificates may need updating. On macOS: `brew install ca-certificates`. On Ubuntu: `sudo update-ca-certificates`.

---

## FAQ

**Q: Does this require payment?**  
A: No. NewsAPI.org offers a free tier with 100 requests/day — more than enough for once-daily personal use.

**Q: What countries are supported?**  
A: Most major countries. Use 2-letter ISO codes: `us`, `gb`, `ca`, `au`, `in`, `de`, `fr`, `jp`, etc.

**Q: Does the free NewsAPI plan give full article text?**  
A: No. The free plan returns headlines, descriptions, source names, and URLs — not full article text. Click through to read the full article.

**Q: Is my API key stored securely?**  
A: The config file is saved with `chmod 600` (owner read/write only). It is not encrypted at rest.

**Q: Can I use multiple API keys?**  
A: One key per config. Use `--api-key` to override the saved key for a specific run.

---

## Requirements

| Requirement | Value |
|-------------|-------|
| Python | 3.8 or newer |
| NewsAPI key | Free from newsapi.org |
| OpenClaw | Any version |
| Subscription Tier | Free |
| Internet Connection | Required |
| External Packages | None (stdlib only) |

---

## Support

- 📖 [Documentation](https://smfworks.com/skills/daily-news-digest)
- 🔑 [Get NewsAPI Key](https://newsapi.org/register)
- 🐛 [Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [Discord](https://discord.gg/smfworks)
