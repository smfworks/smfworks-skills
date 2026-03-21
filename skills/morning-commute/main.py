#!/usr/bin/env python3
"""
Morning Commute - SMF Works Pro Skill
Your daily commute briefing with traffic, transit, and weather.

Requires: SMF Works Pro Subscription + API keys (see SETUP.md)
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
    "home_location": {
        "address": "",
        "lat": 0.0,
        "lon": 0.0
    },
    "work_location": {
        "address": "",
        "lat": 0.0,
        "lon": 0.0
    },
    "weather_api_key": "",
    "transit_api_key": "",  # Optional: for public transit
    "departure_time": "08:00",  # 24-hour format
    "mode": "driving",  # driving, transit, walking, bicycling
    "units": "imperial",  # imperial or metric
    "include_alternatives": True,
    "alert_threshold_minutes": 10  # Alert if delay > 10 min
}

# Weather icons
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
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
    
    standard_config = os.path.expanduser("~/.config/smf/skills/morning-commute/config.json")
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
    os.chmod(config_path, 0o600)


def geocode_address(address: str) -> Optional[Tuple[float, float]]:
    """Geocode address to lat/lon using Nominatim (OpenStreetMap).
    
    Free, no API key required. Be respectful with usage.
    """
    try:
        encoded = urllib.parse.quote(address)
        url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1"
        
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'SMF-MorningCommute/1.0'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)
    except Exception as e:
        print(f"⚠️  Geocoding error: {e}", file=sys.stderr)
    
    return None


def fetch_weather(api_key: str, lat: float, lon: float, units: str = "imperial") -> Optional[Dict]:
    """Fetch current weather from OpenWeatherMap."""
    if not api_key:
        return None
    
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'SMF-MorningCommute/1.0'})
        with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 401:
            print("❌ Invalid weather API key", file=sys.stderr)
        return None
    except Exception as e:
        print(f"⚠️  Weather fetch error: {e}", file=sys.stderr)
        return None


def format_weather(weather_data: Dict, units: str) -> str:
    """Format weather data for display."""
    if not weather_data:
        return "🌤️ Weather data unavailable"
    
    try:
        temp = round(weather_data['main']['temp'])
        description = weather_data['weather'][0]['description']
        main_weather = weather_data['weather'][0]['main'].lower()
        icon = WEATHER_ICONS.get(main_weather, "🌤️")
        unit_symbol = "°F" if units == "imperial" else "°C"
        
        return f"{icon} {temp}{unit_symbol}, {description}"
    except KeyError:
        return "🌤️ Weather data incomplete"


def get_route_info_osrm(start_lat: float, start_lon: float, end_lat: float, end_lon: float) -> Optional[Dict]:
    """Get route info using OSRM (Open Source Routing Machine).
    
    Free, no API key required. Limited to OSM coverage.
    """
    try:
        # OSRM demo server - for production, self-host or use paid service
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=false"
        
        req = urllib.request.Request(url, headers={'User-Agent': 'SMF-MorningCommute/1.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('code') == 'Ok' and data.get('routes'):
                route = data['routes'][0]
                duration_sec = route['duration']
                distance_m = route['distance']
                
                return {
                    'duration_min': round(duration_sec / 60),
                    'distance_mi': round(distance_m / 1609.34, 1),  # meters to miles
                    'distance_km': round(distance_m / 1000, 1)
                }
    except Exception as e:
        print(f"⚠️  Routing error: {e}", file=sys.stderr)
    
    return None


def estimate_traffic_delay(base_duration: int, hour: int, minute: int) -> int:
    """Estimate traffic delay based on time of day.
    
    Simple heuristic - for accurate traffic, use Google Maps API (paid).
    """
    # Rush hour multipliers
    time_val = hour + minute / 60
    
    # Morning rush: 7-9 AM
    if 7 <= time_val <= 9:
        return int(base_duration * 0.3)  # 30% longer
    
    # Evening rush: 5-7 PM
    if 17 <= time_val <= 19:
        return int(base_duration * 0.4)  # 40% longer
    
    # Mid-day: slight delay
    if 12 <= time_val <= 14:
        return int(base_duration * 0.1)
    
    return 0


def format_route_info(route_info: Optional[Dict], delay: int, units: str) -> str:
    """Format route info for display."""
    if not route_info:
        return "🚗 Route info unavailable (configure locations)"
    
    base_duration = route_info['duration_min']
    total_duration = base_duration + delay
    
    distance = route_info['distance_mi'] if units == "imperial" else route_info['distance_km']
    distance_unit = "mi" if units == "imperial" else "km"
    
    lines = [f"🚗 Commute: {total_duration} min ({distance} {distance_unit})"]
    
    if delay > 0:
        lines.append(f"   ⚠️  Traffic delay: +{delay} min")
        lines.append(f"   Normal time: {base_duration} min")
    else:
        lines.append(f"   ✅ Clear route")
    
    return "\n".join(lines)


def get_departure_alert(departure_time: str, delay_min: int) -> str:
    """Generate departure time alert."""
    try:
        # Parse departure time
        dep_hour, dep_min = map(int, departure_time.split(':'))
        
        # Calculate recommended departure
        total_delay = timedelta(minutes=delay_min + 5)  # +5 min buffer
        dep_time = datetime.now().replace(hour=dep_hour, minute=dep_min, second=0, microsecond=0)
        recommended = dep_time - total_delay
        
        lines = [f"⏰ Departure Alert"]
        lines.append(f"   Target arrival: {departure_time}")
        lines.append(f"   Leave by: {recommended.strftime('%I:%M %p')}")
        
        return "\n".join(lines)
    except Exception:
        return "⏰ Configure departure time for alerts"


def generate_commute_briefing(config: Dict, test_mode: bool = False) -> str:
    """Generate the full morning commute briefing."""
    # Check subscription
    if not test_mode and not require_subscription():
        return ""
    
    # Get locations
    home = config.get('home_location', {})
    work = config.get('work_location', {})
    
    # Get weather at home
    weather_str = "🌤️ Weather unavailable"
    api_key = config.get('weather_api_key')
    if api_key and home.get('lat') and home.get('lon'):
        weather_data = fetch_weather(api_key, home['lat'], home['lon'], config.get('units', 'imperial'))
        weather_str = format_weather(weather_data, config.get('units', 'imperial'))
    
    # Get route info
    route_str = "🚗 Route unavailable (configure home & work)"
    departure_alert = "⏰ Configure departure time"
    
    if home.get('lat') and home.get('lon') and work.get('lat') and work.get('lon'):
        route_info = get_route_info_osrm(
            home['lat'], home['lon'],
            work['lat'], work['lon']
        )
        
        if route_info:
            # Calculate delay
            dep_time = config.get('departure_time', '08:00')
            try:
                dep_hour, dep_min = map(int, dep_time.split(':'))
            except:
                dep_hour, dep_min = 8, 0
            
            delay = estimate_traffic_delay(route_info['duration_min'], dep_hour, dep_min)
            
            route_str = format_route_info(route_info, delay, config.get('units', 'imperial'))
            departure_alert = get_departure_alert(dep_time, delay)
    
    # Build briefing
    now = datetime.now()
    
    lines = [
        f"🚗 Morning Commute Briefing — {now.strftime('%A, %B %d')}",
        "",
        weather_str,
        "",
        route_str,
        "",
        departure_alert,
        "",
        "—",
        "Powered by SMF Works Morning Commute",
        "Configure: smf run morning-commute --configure",
        "Subscribe: https://smf.works/subscribe"
    ]
    
    return "\n".join(lines)


def configure_skill():
    """Interactive configuration wizard."""
    print("🚗 Morning Commute - Configuration")
    print("=" * 50)
    print()
    
    config = load_config()
    
    # Step 1: Home Location
    print("Step 1: Home Location")
    print("Enter your home address (e.g., '123 Main St, Pittsboro, NC')")
    home_address = input("Home address: ").strip()
    
    if home_address:
        print("Geocoding address...")
        coords = geocode_address(home_address)
        if coords:
            config['home_location']['address'] = home_address
            config['home_location']['lat'] = coords[0]
            config['home_location']['lon'] = coords[1]
            print(f"✅ Found: {coords[0]:.4f}, {coords[1]:.4f}")
        else:
            print("⚠️  Could not geocode. You'll need to enter coordinates manually.")
            config['home_location']['address'] = home_address
    
    # Step 2: Work Location
    print("\nStep 2: Work Location")
    print("Enter your work address")
    work_address = input("Work address: ").strip()
    
    if work_address:
        print("Geocoding address...")
        coords = geocode_address(work_address)
        if coords:
            config['work_location']['address'] = work_address
            config['work_location']['lat'] = coords[0]
            config['work_location']['lon'] = coords[1]
            print(f"✅ Found: {coords[0]:.4f}, {coords[1]:.4f}")
        else:
            print("⚠️  Could not geocode.")
            config['work_location']['address'] = work_address
    
    # Step 3: Weather API
    print("\nStep 3: Weather API (Optional)")
    print("Get free API key at: https://openweathermap.org/api")
    print("Adds current conditions to your briefing")
    
    weather_key = input("OpenWeatherMap API key (press Enter to skip): ").strip()
    if weather_key:
        config['weather_api_key'] = weather_key
    
    # Step 4: Departure Time
    print("\nStep 4: Departure Settings")
    dep_time = input("Target arrival time (HH:MM, 24h) [08:00]: ").strip()
    if dep_time:
        config['departure_time'] = dep_time
    
    units = input("Units (imperial/metric) [imperial]: ").strip().lower()
    if units in ['imperial', 'metric']:
        config['units'] = units
    
    # Step 5: Schedule
    print("\nStep 5: Schedule")
    print("Recommended: Run weekday mornings at 6:30 AM")
    print("Command: openclaw cron add --name 'morning-commute' --schedule '30 6 * * 1-5' --command 'smf run morning-commute'")
    
    # Save config
    config_path = os.path.expanduser("~/.config/smf/skills/morning-commute/config.json")
    save_config(config, config_path)
    
    print(f"\n✅ Configuration saved to: {config_path}")
    print("\nYour Morning Commute briefing is ready!")
    print("Run: smf run morning-commute")
    
    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Morning Commute - Your commute briefing with traffic and weather",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  smf run morning-commute              # Generate commute briefing
  smf run morning-commute --configure  # Run configuration wizard
  smf run morning-commute --test-mode  # Test without subscription check
  smf run morning-commute --output json # Output as JSON
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
    briefing = generate_commute_briefing(config, test_mode=args.test_mode)
    
    if not briefing:
        sys.exit(1)
    
    if args.output == 'json':
        result = {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "content": briefing,
            "config": {
                "home": config.get('home_location', {}).get('address'),
                "work": config.get('work_location', {}).get('address'),
            }
        }
        print(json.dumps(result, indent=2))
    else:
        print(briefing)


if __name__ == "__main__":
    main()
