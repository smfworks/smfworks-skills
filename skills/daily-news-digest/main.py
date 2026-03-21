#!/usr/bin/env python3
"""
Daily News Digest Skill for OpenClaw
Fetches curated news headlines and delivers a daily briefing.

Requires: NewsAPI.org API key (free tier available)
Get yours at: https://newsapi.org/register
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import urllib.request
import urllib.error
import urllib.parse
import ssl


# Default configuration
DEFAULT_CONFIG = {
    "categories": ["business", "technology"],
    "country": "us",
    "max_articles": 5,
    "sources": [],  # Empty means all sources for category
}

# Category emojis for formatting
CATEGORY_EMOJIS = {
    "business": "💼",
    "technology": "💻",
    "science": "🔬",
    "health": "🏥",
    "sports": "⚽",
    "entertainment": "🎬",
    "general": "📰",
}


def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from file or return defaults."""
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    
    # Check for config in standard location
    standard_config = os.path.expanduser("~/.config/smf/skills/daily-news-digest/config.json")
    if os.path.exists(standard_config):
        with open(standard_config, 'r') as f:
            return json.load(f)
    
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict, config_path: str):
    """Save configuration to file."""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)


def get_api_key() -> Optional[str]:
    """Get NewsAPI key from environment or config."""
    # Check environment first
    api_key = os.environ.get('NEWSAPI_KEY')
    if api_key:
        return api_key
    
    # Check config file
    config_path = os.path.expanduser("~/.config/smf/skills/daily-news-digest/config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    
    return None


def fetch_news(api_key: str, category: str, country: str = "us", page_size: int = 5) -> List[Dict]:
    """Fetch news from NewsAPI."""
    # Use urlencode to safely construct query parameters
    params = urllib.parse.urlencode({
        'category': category,
        'country': country,
        'pageSize': page_size,
        'apiKey': api_key
    })
    url = f"https://newsapi.org/v2/top-headlines?{params}"
    
    # Use secure SSL context with certificate verification enabled
    ssl_context = ssl.create_default_context()
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'SMF-DailyNewsDigest/1.0'
            }
        )
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('status') != 'ok':
                return []
            
            return data.get('articles', [])
    
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("Error: Invalid API key. Please check your NewsAPI key.", file=sys.stderr)
        elif e.code == 429:
            print("Error: API rate limit exceeded. Free tier allows 100 requests/day.", file=sys.stderr)
        else:
            print(f"Error fetching news: HTTP {e.code}", file=sys.stderr)
        return []
    
    except Exception as e:
        print(f"Error fetching news: {e}", file=sys.stderr)
        return []


def format_article(article: Dict, index: int) -> str:
    """Format a single article for display."""
    title = article.get('title', 'No title')
    source = article.get('source', {}).get('name', 'Unknown source')
    url = article.get('url', '')
    
    # Clean up title (remove source name if appended)
    if ' - ' in title:
        title = title.rsplit(' - ', 1)[0]
    
    return f"{index}. {title}\n   📰 {source}\n   🔗 {url}"


def generate_digest(api_key: str, config: Dict) -> str:
    """Generate the full news digest."""
    categories = config.get('categories', ['business', 'technology'])
    country = config.get('country', 'us')
    max_articles = config.get('max_articles', 5)
    
    lines = [
        "📰 Daily News Digest",
        f"📅 {datetime.now().strftime('%A, %B %d, %Y')}",
        "",
    ]
    
    total_articles = 0
    
    for category in categories:
        emoji = CATEGORY_EMOJIS.get(category, "📰")
        lines.append(f"{emoji} {category.upper()}")
        lines.append("-" * 40)
        
        articles = fetch_news(api_key, category, country, max_articles)
        
        if not articles:
            lines.append("   No articles found for this category.")
        else:
            for i, article in enumerate(articles, 1):
                lines.append(format_article(article, i))
                lines.append("")
                total_articles += 1
        
        lines.append("")
    
    lines.append("—")
    lines.append(f"Powered by NewsAPI.org | {total_articles} articles")
    lines.append("Configure: smf run daily-news-digest --configure")
    
    return "\n".join(lines)


def configure_skill():
    """Interactive configuration wizard."""
    print("📰 Daily News Digest - Configuration")
    print("=" * 50)
    print()
    
    # API Key
    print("Step 1: NewsAPI Key")
    print("Get your free API key at: https://newsapi.org/register")
    print("Free tier: 100 requests/day (sufficient for daily digest)")
    print()
    
    api_key = input("Enter your NewsAPI key: ").strip()
    
    if not api_key:
        print("Error: API key is required.", file=sys.stderr)
        return False
    
    # Test the key
    print("\nTesting API key...")
    test_articles = fetch_news(api_key, "general", "us", 1)
    if not test_articles:
        print("Warning: Could not verify API key. Continuing anyway...")
    else:
        print("✅ API key verified!")
    
    # Categories
    print("\nStep 2: Select Categories")
    print("Available: business, technology, science, health, sports, entertainment, general")
    print("Enter categories separated by commas (e.g., business,technology)")
    categories_input = input("Categories [business,technology]: ").strip()
    
    if categories_input:
        categories = [c.strip().lower() for c in categories_input.split(',')]
    else:
        categories = ["business", "technology"]
    
    # Country
    print("\nStep 3: Country Code")
    print("Enter 2-letter country code (e.g., us, gb, ca, au)")
    country = input("Country [us]: ").strip().lower() or "us"
    
    # Max articles per category
    print("\nStep 4: Articles per Category")
    max_input = input("Max articles per category [5]: ").strip()
    max_articles = int(max_input) if max_input.isdigit() else 5
    
    # Save config
    config = {
        "api_key": api_key,
        "categories": categories,
        "country": country,
        "max_articles": max_articles,
    }
    
    config_path = os.path.expanduser("~/.config/smf/skills/daily-news-digest/config.json")
    save_config(config, config_path)
    
    # Secure the config file
    os.chmod(config_path, 0o600)
    
    print(f"\n✅ Configuration saved to: {config_path}")
    print("\nYour Daily News Digest is ready!")
    print("Run: smf run daily-news-digest")
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Daily News Digest - Get curated news delivered daily",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smf run daily-news-digest              # Run with saved configuration
  smf run daily-news-digest --configure  # Configure the skill
  smf run daily-news-digest --api-key KEY # Use specific API key (one-time)
        """
    )
    
    parser.add_argument(
        '--configure', '-c',
        action='store_true',
        help='Run configuration wizard'
    )
    
    parser.add_argument(
        '--api-key', '-k',
        help='NewsAPI key (overrides saved config)'
    )
    
    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )
    
    args = parser.parse_args()
    
    # Configuration mode
    if args.configure:
        success = configure_skill()
        sys.exit(0 if success else 1)
    
    # Get API key
    api_key = args.api_key or get_api_key()
    
    if not api_key:
        print("Error: No API key configured.", file=sys.stderr)
        print("Run: smf run daily-news-digest --configure", file=sys.stderr)
        print("Or get a free key at: https://newsapi.org/register", file=sys.stderr)
        sys.exit(1)
    
    # Load config
    config = load_config()
    
    # Override API key if provided
    if args.api_key:
        config['api_key'] = args.api_key
    
    # Generate digest
    digest = generate_digest(api_key, config)
    
    if args.output == 'json':
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "content": digest,
            "categories": config.get('categories', []),
        }
        print(json.dumps(result, indent=2))
    else:
        print(digest)


if __name__ == "__main__":
    main()
