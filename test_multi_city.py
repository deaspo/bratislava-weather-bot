#!/usr/bin/env python3
"""
Test script for multi-city weather functionality
Tests weather retrieval without Twitter authentication
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock environment variables for testing
os.environ["OPENWEATHER_API_KEY"] = "test_key"  # Will fail but won't crash
os.environ["TWITTER_CONSUMER_KEY"] = "test"
os.environ["TWITTER_CONSUMER_SECRET"] = "test"
os.environ["TWITTER_ACCESS_TOKEN"] = "test"
os.environ["TWITTER_ACCESS_TOKEN_SECRET"] = "test"
os.environ["TWITTER_BEARER_TOKEN"] = "test"

import config
from weather_service import WeatherService
from multi_city_bot import MultiCityWeatherBot
from logger import logger


def test_multi_city_config():
    """Test multi-city configuration"""
    print("🌍 Testing Multi-City Configuration...")
    print(f"Number of cities configured: {len(config.CITIES)}")

    for i, city in enumerate(config.CITIES, 1):
        print(f"{i}. {city['name']}, {city['country_code']}")
        print(f"   📍 Coordinates: {city['latitude']}, {city['longitude']}")
        print(f"   🕐 Timezone: {city['timezone']}")
        print(f"   🏷️ Hashtags: {city['hashtags']}")
        print()


def test_weather_services():
    """Test weather service initialization for each city"""
    print("🌤️ Testing Weather Services...")

    for city in config.CITIES:
        print(f"Testing {city['name']}...")
        try:
            weather_service = WeatherService(city)
            print(f"✅ Weather service initialized for {city['name']}")
            print(f"   Timezone: {weather_service.timezone}")
            print(f"   Coordinates: {weather_service.lat}, {weather_service.lon}")
        except Exception as e:
            print(f"❌ Failed to initialize weather service for {city['name']}: {e}")
        print()


def test_multi_city_bot():
    """Test multi-city bot initialization"""
    print("🤖 Testing Multi-City Bot...")

    try:
        bot = MultiCityWeatherBot()
        cities = bot.get_available_cities()
        print(f"✅ Multi-city bot initialized")
        print(f"Available cities: {', '.join(cities)}")

        # Test weather service access
        for city_name in cities:
            weather_service = bot.weather_services[city_name]
            print(
                f"   {city_name}: {weather_service.city_name} ({weather_service.timezone})"
            )

    except Exception as e:
        print(f"❌ Failed to initialize multi-city bot: {e}")


if __name__ == "__main__":
    print("🧪 Multi-City Weather Bot Test Suite")
    print("=" * 50)

    test_multi_city_config()
    test_weather_services()
    test_multi_city_bot()

    print("✅ Configuration tests completed!")
    print("\nTo test with real API keys:")
    print("1. Set up your .env file with proper API keys")
    print("2. Run: python main.py --mode test --city Nairobi")
    print("3. Or run: python main.py --mode multi-city")
