# Daily News Digest

> Curated daily news briefing from top sources, filtered by your interests

---

## What It Does

Daily News Digest gathers the most important news stories from trusted sources and delivers them in a clean, readable format. Filter by category (technology, business, world, etc.), save stories for later, and search through your news history — all without the doom-scrolling.

---

## Installation

This skill is available from the SMF Works Skills Repository.

**Free tier:**
```bash
smfw install daily-news-digest
```

**Or clone directly:**
```bash
git clone https://github.com/smfworks/smfworks-skills
cd smfworks-skills
python install.sh
```

---

## Quick Start

Get your personalized daily news briefing:

```bash
python main.py digest
```

---

## Commands

### `digest`

**What it does:** Generate your daily news digest with top stories.

**Usage:**
```bash
python main.py digest [options]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--category` | ❌ No | Filter by topic | `technology` |
| `--sources` | ❌ No | Specific news sources | `BBC,CNN` |
| `--limit` | ❌ No | Number of stories (default: 10) | `5` |

**Example:**
```bash
python main.py digest
python main.py digest --category technology
python main.py digest --sources "BBC,The Guardian" --limit 5
```

**Output:**
```
📰 Your Daily News Digest — March 25, 2026
==================================================

🔬 TECHNOLOGY
------------------------------------------------------------
1. AI breakthrough announced by leading lab
   Source: TechCrunch | 2 hours ago
   
2. New smartphone features revealed
   Source: The Verge | 4 hours ago

💼 BUSINESS
------------------------------------------------------------
1. Markets close at record highs
   Source: Bloomberg | 1 hour ago

2. Major merger announced in retail sector
   Source: WSJ | 3 hours ago

🌍 WORLD
------------------------------------------------------------
1. International summit concludes with agreements
   Source: BBC | 5 hours ago

2. Climate initiative gains support
   Source: Reuters | 6 hours ago
```

---

### `search`

**What it does:** Search through cached news stories.

**Usage:**
```bash
python main.py search [keyword]
```

**Arguments:**

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `keyword` | ✅ Yes | Search term | `AI` |

**Example:**
```bash
python main.py search "AI"
python main.py search "climate change"
```

---

### `topics`

**What it does:** List all available news categories and sources.

**Usage:**
```bash
python main.py topics
```

**Example:**
```bash
python main.py topics
```

**Output:**
```
📚 Available Categories:
   • technology
   • business
   • world
   • science
   • health
   • sports
   • entertainment

📰 Available Sources:
   • BBC News
   • CNN
   • Reuters
   • Bloomberg
   • The Guardian
   • TechCrunch
   • The Verge
```

---

## Use Cases

- **Morning routine:** Read news while having coffee
- **Stay informed:** Track specific industries or topics
- **Research:** Search past news for trends
- **Briefings:** Get quick summaries before meetings

---

## Tips & Tricks

- Use `--limit 3` for a quick 3-headline summary
- Set up a daily cron job: `0 8 * * * python main.py digest`
- Bookmark interesting articles by saving the URL from output
- Use `--category` to filter noise and focus on what matters

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No stories found" | Check your internet connection or try a different category |
| "API rate limit" | Wait a few minutes or use `--limit` to reduce requests |
| Empty digest | Some categories may not have stories on weekends |

---

## Requirements

- Python 3.8+
- OpenClaw installed
- (Optional) News API key for more sources and better results

---

## Support

- 📖 [Full Documentation](https://smfworks.com/skills/daily-news-digest)
- 🐛 [Report Issues](https://github.com/smfworks/smfworks-skills/issues)
- 💬 [SMF Works](https://smfworks.com)
