# Daily News Digest — How-To Guide

**Prerequisites:** Setup complete (see SETUP.md). NewsAPI key configured.

---

## Table of Contents

1. [How to Get Your Daily News Briefing](#1-how-to-get-your-daily-news-briefing)
2. [How to Customize Your News Categories](#2-how-to-customize-your-news-categories)
3. [How to Get JSON Output for Scripts](#3-how-to-get-json-output-for-scripts)
4. [How to Save Your Digest to a File](#4-how-to-save-your-digest-to-a-file)
5. [How to Change Your Country](#5-how-to-change-your-country)
6. [Automating with Cron](#6-automating-with-cron)
7. [Combining with Other Skills](#7-combining-with-other-skills)
8. [Troubleshooting Common Issues](#8-troubleshooting-common-issues)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. How to Get Your Daily News Briefing

**What this does:** Fetches today's top headlines for your configured categories and prints a formatted digest.

**When to use it:** Every morning as part of your daily routine.

### Steps

**Step 1 — Navigate to the skill directory.**

```bash
cd ~/smfworks-skills/skills/daily-news-digest
```

**Step 2 — Run the digest.**

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
   Source: TechCrunch | techcrunch.com/2024/03/15/apple-m3-ultra

2. OpenAI Releases GPT-5 with Improved Reasoning
   Source: The Verge | theverge.com/2024/3/15/gpt5-release

3. Google DeepMind Achieves New Protein Folding Benchmark
   Source: Wired | wired.com/story/google-deepmind-alphafold

💼 Business
────────────
1. Fed Signals Rate Hold Through Mid-2024
   Source: Reuters | reuters.com/...

2. Amazon Reports Record Q4 Cloud Earnings
   Source: Bloomberg | bloomberg.com/...

Configure: smf run daily-news-digest --configure
```

**Step 3 — Click through to read articles you're interested in.**

The skill shows headlines and URLs. Open the URLs in your browser for the full story.

**Result:** A clean, focused news briefing in under 30 seconds.

---

## 2. How to Customize Your News Categories

**What this does:** Re-runs the configuration wizard to update which categories you follow.

**When to use it:** Your interests have changed, or you want to add/remove categories.

### Steps

**Step 1 — Run the configuration wizard.**

```bash
python3 main.py --configure
```

**Step 2 — At the categories prompt, enter your desired categories.**

Available categories: `business`, `technology`, `science`, `health`, `sports`, `entertainment`, `general`

```
Enter categories (comma-separated) [technology,science]: technology,health,science
```

**Step 3 — Confirm the rest of the settings** (press Enter to keep defaults).

**Step 4 — Run the digest to verify.**

```bash
python3 main.py
```

You should now see sections for Technology, Health, and Science.

**Result:** Your digest now covers exactly the categories you care about.

---

## 3. How to Get JSON Output for Scripts

**What this does:** Returns the digest as a JSON object instead of formatted text — useful for piping to other scripts or tools.

**When to use it:** You want to process the headlines programmatically or pipe them to another tool.

### Steps

**Step 1 — Run with `--output json`.**

```bash
python3 main.py --output json
```

Output:
```json
{
  "success": true,
  "timestamp": "2024-03-15T09:00:12.345678",
  "content": "📰 Daily News Digest...",
  "categories": [
    "technology",
    "business"
  ]
}
```

**Step 2 — Extract just the content field.**

```bash
python3 main.py --output json | python3 -c "import json,sys; print(json.load(sys.stdin)['content'])"
```

**Result:** JSON output ready for scripting, piping, or storage.

---

## 4. How to Save Your Digest to a File

**What this does:** Saves the daily digest as a text file you can read later or archive.

**When to use it:** You want to keep a record of daily news, or read the digest on a device that doesn't have internet.

### Steps

**Step 1 — Save to a date-stamped file.**

```bash
python3 main.py > ~/News/digest-$(date +%Y-%m-%d).txt
```

**Step 2 — Read it later.**

```bash
cat ~/News/digest-2024-03-15.txt
```

**Step 3 — Archive a week of digests.**

```bash
ls ~/News/
```

```
digest-2024-03-11.txt
digest-2024-03-12.txt
digest-2024-03-13.txt
digest-2024-03-14.txt
digest-2024-03-15.txt
```

**Result:** A complete daily archive of your news briefings.

---

## 5. How to Change Your Country

**What this does:** Sets which country's news you want headlines from.

**When to use it:** You're in a different country, or you want news from a specific market.

### Steps

**Step 1 — Run the configure wizard.**

```bash
python3 main.py --configure
```

**Step 2 — At the country prompt, enter your country code.**

| Country | Code |
|---------|------|
| United States | us |
| United Kingdom | gb |
| Canada | ca |
| Australia | au |
| India | in |
| Germany | de |
| France | fr |
| Japan | jp |
| Brazil | br |

```
Country [us]: gb
```

**Step 3 — Run the digest to verify.**

Headlines will now be from UK sources.

**Result:** Country-appropriate headlines from your region.

---

## 6. Automating with Cron

Schedule the digest to run every morning and save to a file — your news briefing is ready when you open your terminal.

### Open the cron editor

```bash
crontab -e
```

### Example: Run the digest every morning at 7 AM and save to a file

```bash
0 7 * * * cd /home/yourname/smfworks-skills/skills/daily-news-digest && python3 main.py > /home/yourname/News/digest-$(date +\%Y-\%m-\%d).txt 2>&1
```

### Example: Append digest to a weekly summary file

```bash
0 7 * * * cd /home/yourname/smfworks-skills/skills/daily-news-digest && python3 main.py >> /home/yourname/News/weekly-$(date +\%Y-W\%V).txt 2>&1
```

### Create the news directory first

```bash
mkdir -p ~/News
```

### Check the output

```bash
cat ~/News/digest-$(date +%Y-%m-%d).txt
```

### Cron Expression Reference

| Expression | Meaning |
|------------|---------|
| `0 7 * * *` | Every day at 7 AM |
| `0 6 * * 1-5` | Weekdays at 6 AM |
| `30 7 * * *` | Every day at 7:30 AM |

---

## 7. Combining with Other Skills

**Daily News Digest + Markdown Converter:** Save digest as markdown and convert to HTML:

```bash
python3 ~/smfworks-skills/skills/daily-news-digest/main.py > ~/News/today.txt
# Add Markdown formatting manually or via script, then:
python3 ~/smfworks-skills/skills/markdown-converter/main.py to-html ~/News/today.md
```

**Daily News Digest + File Organizer:** Save digests and organize by date:

```bash
python3 ~/smfworks-skills/skills/daily-news-digest/main.py > ~/News/digest.txt
python3 ~/smfworks-skills/skills/file-organizer/main.py organize-date ~/News/
```

---

## 8. Troubleshooting Common Issues

### `Error: No API key configured.`

No API key is saved or in environment.  
**Fix:** Run `python3 main.py --configure` and enter your key. Or: `export NEWSAPI_KEY=yourkey`

---

### `HTTP Error 401: Unauthorized`

Your API key is invalid or not yet active.  
**Fix:** Verify your key at [newsapi.org/account](https://newsapi.org/account). New accounts take a minute to activate.

---

### `HTTP Error 429: Too Many Requests`

Exceeded 100 daily requests on the free plan.  
**Fix:** The limit resets at midnight UTC. Reduce your max_articles setting and avoid running more than twice per day on the free plan.

---

### No articles returned

Some categories have limited coverage for certain countries.  
**Fix:** Try `us` as the country. Switch to `technology`, `business`, or `general` which have the most global coverage.

---

### Digest shows old news

NewsAPI updates top headlines periodically — results are cached for ~15 minutes.  
**Fix:** This is normal. Run again in 15 minutes for fresh results.

---

## 9. Tips & Best Practices

**Limit to 2–3 categories on the free plan.** Each category is a separate API request. With 100 requests/day, you have room for multiple daily runs with 2–3 categories each.

**Run it in the morning, not at night.** Top headlines are most relevant within 6–12 hours of publication. Running in the evening gives you yesterday's news wrapped in today's date.

**Save your digest to a file.** Use `python3 main.py > ~/News/digest-$(date +%Y-%m-%d).txt` so you can refer back to it even when you're offline later.

**Use `--api-key` for testing without touching config.** If you want to test a new key: `python3 main.py --api-key your-new-key --output json` — it won't overwrite your saved config.

**`general` category gives the broadest coverage.** If you want a quick overview of "what's happening," `general` is the best single category. It pulls from the widest range of sources.

**Consider different countries for different perspectives.** Try running once with `us` and once with `gb` to compare how the same stories are covered differently by US and UK press.
