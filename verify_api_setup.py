#!/usr/bin/env python3
"""Quick verification script to check if API keys are loaded correctly."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

print("=" * 60)
print("API Configuration Status")
print("=" * 60)

# Check each API key
api_keys = {
    "YouTube": os.getenv("YOUTUBE_API_KEY"),
    "Ticketmaster": os.getenv("TICKETMASTER_API_KEY"),
    "OpenWeatherMap": os.getenv("OPENWEATHERMAP_API_KEY"),
    "Mapbox": os.getenv("MAPBOX_API_KEY"),
}

for api_name, api_key in api_keys.items():
    if api_key and api_key.strip():
        print(f"✅ {api_name}: Configured ({api_key[:8]}...)")
    else:
        print(f"❌ {api_name}: Not configured (will use mock data)")

print("=" * 60)

# Test the config loading
print("\nTesting config loading...")
try:
    from fabric_dashboard.utils.config import get_config

    config = get_config()
    if config:
        print("✅ Config loaded successfully")
        print(f"   - YouTube API: {'✅' if config.youtube_api_key else '❌ (mocks)'}")
        print(f"   - Ticketmaster API: {'✅' if config.ticketmaster_api_key else '❌ (mocks)'}")
        print(f"   - OpenWeatherMap API: {'✅' if config.openweathermap_api_key else '❌ (mocks)'}")
        print(f"   - Mapbox API: {'✅' if config.mapbox_api_key else '❌ (mocks)'}")
    else:
        print("❌ Could not load config")
except Exception as e:
    print(f"❌ Error loading config: {e}")

print("=" * 60)
print("\nConclusion:")
all_configured = all(key and key.strip() for key in api_keys.values())
if all_configured:
    print("✅ All APIs are configured - system will use REAL data")
else:
    print("⚠️  Some APIs are missing - system will use MOCK data for those")
print("=" * 60)
