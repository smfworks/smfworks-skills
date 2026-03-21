#!/usr/bin/env python3
"""
Coffee Briefing - SMF Works Pro Skill
Your personal morning briefing with weather, calendar, and priorities.

Requires: SMF Works Pro Subscription + OpenWeatherMap API key
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import urllib.request
import urllib.error
import ssl

# Add shared module path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

try:
    from smf_auth import require_subscription, validate_token
except ImportError:
    # Fallback for standalone testing
    def require_subscription():
        """Check if user has active subscription."""
        token_path = os.path.expanduser("~/.smf/token")
        if not os.path.exists(token_path):
            print("❌ Pro skill requires SMF Works subscription")
            print("   Subscribe at: https://smf.works/subscribe")
            return False
        return True
    
    def validate_token():
        return True


# Default configuration
DEFAULT_CONFIG = {
    "weather_api_key": "",
    "location": {
        "city": "New York",
        "lat": 40.7128,
        "lon": -74.0060,
        "units": "imperial"  # imperial (F) or metric (C)
    },
    "calendar": {
        "enabled": False,
        "calendar_id": "primary",
        "max_events": 5
    },
    "priorities": {
        "source": "auto",  # auto, file
        "file_path": "",
        "max_priorities": 3
    },
    "output": {
        "format": "text",  # text or json
        "include_icons": True
    }
}

# Weather icons mapping
WEATHER_ICONS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "🌨️",
    "mist": "🌫️",
    "fog": "🌫️",
    "haze": "🌫️",
}


def load_config(config_path: Optional[str] = None) -> Dict:
    """Load configuration from file or return defaults."""
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            # Merge with defaults
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
    
    # Check for config in standard location
    standard_config = os.path.expanduser("~/.config/smf/skills/coffee-briefing/config.json")
    if os.path.exists(standard_config):
        with open(standard_config, 'r') as f:
            config = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
    
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict, config_path: str):
    """Save configuration to file."""
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    # Secure the config file
    os.chmod(config_path, 0o600)


def fetch_weather(api_key: str, lat: float, lon: float, units: str = "imperial") -> Optional[Dict]:
    """Fetch current weather from OpenWeatherMap."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'SMF-CoffeeBriefing/1.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Invalid weather API key", file=sys.stderr)
        else:
            print(f"❌ Weather API error: HTTP {e.code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Weather fetch error: {e}", file=sys.stderr)
        return None


def format_weather(weather_data: Dict, units: str) -> str:
    """Format weather data for display."""
    if not weather_data:
        return "🌤️ Weather data unavailable"
    
    try:
        temp = round(weather_data['main']['temp'])
        feels_like = round(weather_data['main']['feels_like'])
        temp_min = round(weather_data['main']['temp_min'])
        temp_max = round(weather_data['main']['temp_max'])
        description = weather_data['weather'][0]['description']
        main_weather = weather_data['weather'][0]['main'].lower()
        city = weather_data.get('name', 'Unknown')
        
        # Get appropriate icon
        icon = WEATHER_ICONS.get(main_weather, "🌤️")
        
        # Temperature unit symbol
        unit_symbol = "°F" if units == "imperial" else "°C"
        
        lines = [
            f"{icon} Weather in {city}",
            f"   Current: {temp}{unit_symbol}, {description}",
            f"   Feels like: {feels_like}{unit_symbol}",
            f"   High: {temp_max}{unit_symbol} | Low: {temp_min}{unit_symbol}"
        ]
        
        return "\n".join(lines)
    except KeyError as e:
        return f"🌤️ Weather data incomplete"


def extract_priorities(config: Dict) -> List[str]:
    """Extract top priorities from configured source."""
    source = config.get('priorities', {}).get('source', 'auto')
    max_p = config.get('priorities', {}).get('max_priorities', 3)
    
    priorities = []
    
    if source == 'file':
        file_path = config.get('priorities', {}).get('file_path', '')
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Extract lines starting with numbers or dashes
                    for line in content.split('\n'):
                        line = line.strip()
                        if line and (line[0].isdigit() or line.startswith('-')):
                            clean = line.lstrip('-0123456789. ')
                            if clean and len(clean) > 3:
                                priorities.append(clean)
                                if len(priorities) >= max_p:
                                    break
            except Exception as e:
                print(f"Warning: Could not read priorities file: {e}", file=sys.stderr)
    
    # Default priorities if none found
    if not priorities:
        priorities = [
            "Review today's calendar and prepare",
            "Check messages and respond to urgent items",
            "Focus on your most important task"
        ]
    
    return priorities[:max_p]


def format_priorities(priorities: List[str]) -> str:
    """Format priorities for display."""
    lines = ["🎯 Top Priorities"]
    
    for i, priority in enumerate(priorities, 1):
        lines.append(f"   {i}. {priority}")
    
    return "\n".join(lines)


def generate_briefing(config: Dict, test_mode: bool = False) -> str:
    """Generate the full coffee briefing."""
    # Check subscription (unless in test mode)
    if not test_mode and not require_subscription():
        return ""
    
    # Get weather
    api_key = config.get('weather_api_key')
    weather_str = "🌤️ Weather unavailable (configure API key)"
    
    if api_key:
        lat = config.get('location', {}).get('lat', 40.7128)
        lon = config.get('location', {}).get('lon', -74.0060)
        units = config.get('location', {}).get('units', 'imperial')
        
        weather_data = fetch_weather(api_key, lat, lon, units)
        weather_str = format_weather(weather_data, units)
    
    # Get calendar (placeholder - would integrate with Google Calendar API)
    calendar_enabled = config.get('calendar', {}).get('enabled', False)
    calendar_str = "📅 Calendar not configured (optional)"
    
    if calendar_enabled:
        calendar_str = "📅 Calendar integration requires OAuth setup (see SETUP.md)"
    
    # Get priorities
    priorities = extract_priorities(config)
    priorities_str = format_priorities(priorities)
    
    # Build briefing
    now = datetime.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        greeting = "☕ Good Morning!"
    elif 12 <= hour < 17:
        greeting = "☕ Good Afternoon!"
    else:
        greeting = "☕ Good Evening!"
    
    lines = [
        f"{greeting} Here's your briefing for {now.strftime('%A, %B %d, %Y')}",
        "",
        weather_str,
        "",
        calendar_str,
        "",
        priorities_str,
        "",
        "—",
        "Powered by SMF Works Coffee Briefing ☕",
        "Configure: smf run coffee-briefing --configure",
        "Subscribe: https://smf.works/subscribe"
    ]
    
    return "\n".join(lines)


def configure_skill():
    """Interactive configuration wizard."""
    print("☕ Coffee Briefing - Configuration")
    print("=" * 50)
    print()
    
    config = load_config()
    
    # Step 1: Weather API Key
    print("Step 1: OpenWeatherMap API Key")
    print("Get your free API key at: https://openweathermap.org/api")
    print("Free tier: 1,000 calls/day (sufficient for daily briefings)")
    print()
    
    api_key = input("Enter your OpenWeatherMap API key: ").strip()
    if api_key:
        config['weather_api_key'] = api_key
    
    # Step 2: Location
    print("\nStep 2: Your Location")
    city = input(f"City name [{config['location']['city']}]: ").strip()
    if city:
        config['location']['city'] = city
    
    units = input("Units (imperial/metric) [imperial]: ").strip().lower()
    if units in ['imperial', 'metric']:
        config['location']['units'] = units
    
    # Step 3: Priorities
    print("\nStep 3: Priorities Source")
    print("Options: auto (default), file")
    
    source = input("Source [auto]: ").strip()
    if source:
        config['priorities']['source'] = source
    
    if source == 'file':
        file_path = input("Path to priorities file: ").strip()
        if file_path:
            config['priorities']['file_path'] = os.path.expanduser(file_path)
    
    # Step 4: Schedule info
    print("\nStep 4: Schedule")
    print("Recommended: Run daily at 7:00 AM via OpenClaw cron")
    print("Command: openclaw cron add --name 'coffee-briefing' --schedule '0 7 * * *' --command 'smf run coffee-briefing'")
    
    # Save config
    config_path = os.path.expanduser("~/.config/smf/skills/coffee-briefing/config.json")
    save_config(config, config_path)
    
    print(f"\n✅ Configuration saved to: {config_path}")
    print("\nYour Coffee Briefing is ready!")
    print("Run: smf run coffee-briefing")
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Coffee Briefing - Your personal morning briefing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smf run coffee-briefing              # Generate today's briefing
  smf run coffee-briefing --configure  # Run configuration wizard
  smf run coffee-briefing --test-mode  # Test without subscription check
  smf run coffee-briefing --output json # Output as JSON
        """
    )
    
    parser.add_argument(
        '--configure', '-c',
        action='store_true',
        help='Run configuration wizard'
    )
    
    parser.add_argument(
        '--test-mode', '-t',
        action='store_true',
        help='Test mode (skip subscription check)'
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
    
    # Load config
    config = load_config()
    
    # Generate briefing
    briefing = generate_briefing(config, test_mode=args.test_mode)
    
    if not briefing:
        sys.exit(1)
    
    if args.output == 'json':
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "content": briefing,
            "config": {
                "location": config.get('location', {}).get('city'),
            }
        }
        print(json.dumps(result, indent=2))
    else:
        print(briefing)


if __name__ == "__main__":
    main()
