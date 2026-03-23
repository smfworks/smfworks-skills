# Daily News Digest — Setup Guide

**Estimated setup time:** 10 minutes  
**Difficulty:** Easy  
**Tier:** Free — skill is free; requires a free NewsAPI.org API key

---

## What You'll Need

| Requirement | Details | Cost |
|-------------|---------|------|
| Python 3.8+ | Built into macOS 12+, available on Linux | Free |
| smfworks-skills repository | Cloned via git | Free |
| NewsAPI.org account | Free, no credit card required | Free |
| NewsAPI key | Generated after account creation | Free (100 requests/day) |
| Internet connection | Required to fetch news | — |

---

## Step 1 — Verify Python

```bash
python3 --version
```

Expected: `Python 3.9.x` or newer.

---

## Step 2 — Get the Repository

```bash
git clone https://github.com/smfworks/smfworks-skills ~/smfworks-skills
```

---

## Step 3 — Get a Free NewsAPI Key

The skill requires a free API key from NewsAPI.org. Here's how to get one:

**3a — Go to the registration page:**  
Open your browser and visit: [https://newsapi.org/register](https://newsapi.org/register)

**3b — Fill out the form:**
- First name / Last name
- Email address
- Password

**3c — Confirm your email:**  
Check your inbox for a confirmation email from NewsAPI. Click the verification link.

**3d — Find your API key:**  
After confirming, log in and go to your dashboard at [newsapi.org/account](https://newsapi.org/account). Your API key is displayed there. It looks like this:
```
YOUR_NEWSAPI_KEY_HERE
```

**3e — Save your key somewhere temporarily** (you'll paste it into the configuration wizard in Step 6).

**Free plan limits:**
- 100 API requests per day
- Top headlines only (no full article text)
- No commercial use

This is more than sufficient for daily personal use with one or two runs per day.

---

## Step 4 — Navigate to the Skill

```bash
cd ~/smfworks-skills/skills/daily-news-digest
```

---

## Step 5 — Verify the Skill

```bash
python3 main.py --help
```

Expected output:
```
usage: main.py [-h] [--configure] [--api-key API_KEY] [--output {text,json}]

Daily News Digest - Get curated news delivered daily

optional arguments:
  -h, --help            show this help message and exit
  --configure, -c       Run configuration wizard
  --api-key API_KEY, -k API_KEY
                        NewsAPI key (overrides saved config)
  --output {text,json}, -o {text,json}
                        Output format (default: text)
```

---

## Step 6 — Configure the Skill

Run the setup wizard:

```bash
python3 main.py --configure
```

You'll be guided through four steps:

```
Step 1: API Key
Enter your NewsAPI key: [paste your key here and press Enter]

Step 2: News Categories
Available: business, technology, science, health, sports, entertainment, general
Enter categories (comma-separated) [business,technology]: technology,science

Step 3: Country
Enter 2-letter country code (e.g., us, gb, ca, au)
Country [us]: us

Step 4: Articles per Category
Max articles per category [5]: 5

✅ Configuration saved to: /home/yourname/.config/smf/skills/daily-news-digest/config.json
Your Daily News Digest is ready!
Run: smf run daily-news-digest
```

**Choose your categories wisely:** Start with 2–3 categories at 5 articles each. More categories = more API requests. With the free plan's 100 requests/day limit, 3 categories × 5 articles = well within the free limit for multiple daily runs.

---

## Verify Your Setup

Run the digest for the first time:

```bash
python3 main.py
```

Expected output:
```
📰 Daily News Digest — Friday, March 15, 2024
══════════════════════════════════════════════

💻 Technology
─────────────
1. Apple Announces New M3 Ultra Chip for Mac Pro
   Source: TechCrunch | techcrunch.com/...

2. OpenAI Releases GPT-5 with Improved Reasoning
   Source: The Verge | theverge.com/...
...
```

If you see headlines with sources, your setup is complete.

---

## Configuration File Location

Your settings are saved at:
```
~/.config/smf/skills/daily-news-digest/config.json
```

You can view or edit it directly:
```bash
cat ~/.config/smf/skills/daily-news-digest/config.json
```

Sample content:
```json
{
  "api_key": "YOUR_NEWSAPI_KEY_HERE",
  "categories": ["technology", "science"],
  "country": "us",
  "max_articles": 5
}
```

The file is saved with restricted permissions (readable only by you).

---

## Alternative: Environment Variable

If you prefer not to save the key to a file:

```bash
export NEWSAPI_KEY="your-api-key-here"
python3 main.py
```

Add the export to your `~/.bashrc` or `~/.zshrc` to make it permanent.

---

## Troubleshooting Setup Issues

**`Error: No API key configured.`**  
You haven't run `--configure` yet, or the config file doesn't exist.  
**Fix:** `python3 main.py --configure`

**`HTTP Error 401: Unauthorized`**  
API key is wrong or not yet active.  
**Fix:** Double-check your key at newsapi.org/account. New keys may take a minute to activate.

**`HTTP Error 429: Too Many Requests`**  
You've used all 100 free requests today.  
**Fix:** Wait until midnight UTC for the limit to reset.

**No internet access**  
The skill requires internet to fetch news.  
**Fix:** Check your connection: `curl https://newsapi.org`

---

## Understanding the NewsAPI Free Plan

The free NewsAPI plan is designed for developers and personal projects:

| Feature | Free Plan | Developer Plan ($449/mo) |
|---------|-----------|--------------------------|
| Requests/day | 100 | Unlimited |
| Article history | Current + 1 month | Complete archive |
| Full article text | ❌ No | ✅ Yes |
| Commercial use | ❌ No | ✅ Yes |
| Sources | All | All |

For personal daily briefings, the free plan is perfect. 100 requests/day allows 3–5 categories × 5 articles × multiple daily runs.

---

## Available News Categories

When configuring, choose from these categories:

| Category | What it covers |
|----------|---------------|
| `business` | Business news, market updates, company announcements |
| `technology` | Tech industry, software, hardware, science |
| `science` | Research, space, biology, physics |
| `health` | Medical research, public health, healthcare |
| `sports` | Global and US sports, results, transfers |
| `entertainment` | Movies, music, celebrity, culture |
| `general` | Broad mix of top news across all categories |

**Recommendation for most users:** Start with 2–3 categories. `technology` and `general` together give broad, quality coverage.

---

## Available Country Codes

The `country` setting filters to news from that country. Common codes:

| Country | Code |
|---------|------|
| United States | `us` |
| United Kingdom | `gb` |
| Canada | `ca` |
| Australia | `au` |
| India | `in` |
| Germany | `de` |
| France | `fr` |
| Japan | `jp` |
| Brazil | `br` |
| International mix | Use `general` category without country filter |

---

## Security Note on API Key Storage

Your NewsAPI key is stored in `~/.config/smf/skills/daily-news-digest/config.json` with `chmod 600` (owner read/write only). This means:

- The file is not readable by other users on the machine
- It is NOT encrypted — anyone with root access can read it
- It will be included in system backups (use Claw System Backup)

If your machine is shared or you have elevated security requirements, use the environment variable approach instead:

```bash
# Add to ~/.bashrc — only readable by you:
export NEWSAPI_KEY="your-key-here"
```

---

## Next Steps

Setup is verified and working. See **HOWTO.md** for complete usage walkthroughs:

Note: If you ever need to reset your configuration (e.g., you have a new API key), simply run `--configure` again and it will overwrite the saved settings.
- How to customize your categories
- How to schedule a daily briefing with cron
- How to get JSON output for scripting
- Tips for getting the most from the free NewsAPI plan
