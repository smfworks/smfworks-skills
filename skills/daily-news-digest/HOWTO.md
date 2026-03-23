# Daily News Digest — Quick Reference

## Install
```bash
smfw install daily-news-digest
```

## Commands
```bash
python main.py digest                        # Get today's digest
python main.py digest --category tech       # Tech news only
python main.py digest --sources BBC,CNN     # Specific sources
python main.py search "keyword"             # Search past news
python main.py topics                        # List available topics
```

## Common Examples
```bash
# Get your daily news digest
python main.py digest

# Get just tech news
python main.py digest --category technology

# Get news from specific sources
python main.py digest --sources "BBC,The Guardian"

# Search for past news about a topic
python main.py search "AI"
```

## Help
```bash
python main.py --help
python main.py digest --help
```
