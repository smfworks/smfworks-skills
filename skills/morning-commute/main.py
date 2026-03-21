#!/usr/bin/env python3
"""
Morning Commute - SMF Works Pro Skill
Your daily commute briefing with traffic, transit, and weather.

Requires: SMF Works Pro Subscription
APIs: OpenStreetMap (free), OSRM (free), OpenWeatherMap (optional)
"""

import os
import sys
import json
import argparse
from datetime import datetime
from typing import Dict, Optional
import urllib.request
import urllib.error
import urllib.parse
import ssl

# Add shared module path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

try:
    from smf_auth import require_subscription
except ImportError:
    def require_subscription():
        token_path = os.path.expanduser("~/.smf/token")
        if not os.path.exists(token_path):
            print("❌ Pro skill requires SMF Works subscription")
            return False
        # Check token is non-empty
        try:
            with open(token_path, 'r') as f:
                token = f.read().strip()
            if not token:
                print("❌ Pro skill requires SMF Works subscription")
                return False
        except Exception:
            return False
        return True

DEFAULT_CONFIG = {
    "home": {"address": "", "lat": 0, "lon": 0},
    "work": {"address": "", "lat": 0, "lon": 0},
    "weather_api_key": "",
    "departure_time": "08:00",
    "units": "imperial"
}

def load_config():
    config_path = os.path.expanduser("~/.config/smf/skills/morning-commute/config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            config = DEFAULT_CONFIG.copy()
            config.update(json.load(f))
            return config
    return DEFAULT_CONFIG.copy()

def save_config(config):
    config_path = os.path.expanduser("~/.config/smf/skills/morning-commute/config.json")
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    os.chmod(config_path, 0o600)

def geocode_address(address):
    """Free geocoding via OpenStreetMap Nominatim."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(address)}&format=json&limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'SMF-MorningCommute/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
    except Exception as e:
        print(f"Geocoding error: {e}", file=sys.stderr)
    return None

def get_route(home_lat, home_lon, work_lat, work_lon):
    """Free routing via OSRM demo server."""
    try:
        # Use HTTPS for OSRM API
        url = f"https://router.project-osrm.org/route/v1/driving/{home_lon},{home_lat};{work_lon},{work_lat}?overview=false"
        req = urllib.request.Request(url, headers={'User-Agent': 'SMF-MorningCommute/1.0'})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            if data.get('code') == 'Ok':
                route = data['routes'][0]
                return {
                    'duration': round(route['duration'] / 60),  # minutes
                    'distance': round(route['distance'] / 1609.34, 1)  # miles
                }
    except Exception as e:
        print(f"Routing error: {e}", file=sys.stderr)
    return None

def get_weather(api_key, lat, lon, units="imperial"):
    """OpenWeatherMap current weather."""
    if not api_key:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units={units}"
        # Use secure SSL context with certificate verification enabled
        ssl_ctx = ssl.create_default_context()
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ssl_ctx, timeout=30) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"Weather error: {e}", file=sys.stderr)
    return None

def generate_briefing(config, test_mode=False):
    if not test_mode and not require_subscription():
        return ""
    
    home = config.get('home', {})
    work = config.get('work', {})
    
    lines = ["🚗 Morning Commute Briefing", f"📅 {datetime.now().strftime('%A, %B %d, %Y')}", ""]
    
    # Weather
    weather_key = config.get('weather_api_key')
    if weather_key and home.get('lat'):
        w = get_weather(weather_key, home['lat'], home['lon'], config.get('units', 'imperial'))
        if w:
            temp = round(w['main']['temp'])
            desc = w['weather'][0]['description']
            unit = "°F" if config.get('units') == 'imperial' else "°C"
            lines.append(f"🌤️ {temp}{unit}, {desc}")
            lines.append("")
    
    # Route
    if home.get('lat') and work.get('lat'):
        route = get_route(home['lat'], home['lon'], work['lat'], work['lon'])
        if route:
            lines.append(f"🚗 Commute: {route['duration']} min ({route['distance']} mi)")
            # Simple traffic estimate (rush hour check)
            hour = datetime.now().hour
            if 7 <= hour <= 9:
                delay = int(route['duration'] * 0.3)
                lines.append(f"   ⚠️ Traffic delay: +{delay} min")
            lines.append("")
    
    # Departure
    dep_time = config.get('departure_time', '08:00')
    lines.append(f"⏰ Target arrival: {dep_time}")
    lines.append("")
    
    lines.extend([
        "—",
        "Powered by SMF Works Morning Commute",
        "Configure: smf run morning-commute --configure"
    ])
    
    return "\n".join(lines)

def configure():
    print("🚗 Morning Commute Configuration")
    print("=" * 50)
    config = load_config()
    
    print("\nStep 1: Home Address")
    home_addr = input("Home address: ").strip()
    if home_addr:
        config['home']['address'] = home_addr
        coords = geocode_address(home_addr)
        if coords:
            config['home']['lat'] = coords[0]
            config['home']['lon'] = coords[1]
            print(f"✅ Located: {coords[0]:.4f}, {coords[1]:.4f}")
    
    print("\nStep 2: Work Address")
    work_addr = input("Work address: ").strip()
    if work_addr:
        config['work']['address'] = work_addr
        coords = geocode_address(work_addr)
        if coords:
            config['work']['lat'] = coords[0]
            config['work']['lon'] = coords[1]
            print(f"✅ Located: {coords[0]:.4f}, {coords[1]:.4f}")
    
    print("\nStep 3: Weather API (Optional)")
    print("Get free key at: https://openweathermap.org/api")
    w_key = input("API key (Enter to skip): ").strip()
    if w_key:
        config['weather_api_key'] = w_key
    
    print("\nStep 4: Settings")
    dep = input("Target arrival time [08:00]: ").strip()
    if dep:
        config['departure_time'] = dep
    
    save_config(config)
    print("\n✅ Configuration saved!")
    print("Run: smf run morning-commute")
    return True

def main():
    parser = argparse.ArgumentParser(description="Morning Commute Briefing")
    parser.add_argument('--configure', '-c', action='store_true', help='Configure skill')
    parser.add_argument('--test-mode', '-t', action='store_true', help='Skip subscription check')
    args = parser.parse_args()
    
    if args.configure:
        configure()
        return
    
    config = load_config()
    briefing = generate_briefing(config, test_mode=args.test_mode)
    if briefing:
        print(briefing)

if __name__ == "__main__":
    main()
