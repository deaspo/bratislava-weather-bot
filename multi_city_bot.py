#!/usr/bin/env python3
"""
Multi-City Weather Bot
Automated Twitter bot for posting weather updates for multiple cities
"""

import config
from weather_service import WeatherService
from twitter_service import TwitterService
from message_formatter import MessageFormatter
from logger import logger


class MultiCityWeatherBot:
    def __init__(self):
        self.twitter_service = TwitterService()
        self.cities = config.CITIES

        # Create weather services for each city
        self.weather_services = {}
        for city in self.cities:
            self.weather_services[city["name"]] = WeatherService(city)

        self.formatter = MessageFormatter()

    def post_current_weather_all_cities(self):
        """Post current weather update for all cities"""
        try:
            logger.info("Starting multi-city weather update")

            for city in self.cities:
                city_name = city["name"]
                weather_service = self.weather_services[city_name]

                logger.info(f"Posting weather for {city_name}")

                # Get current weather
                current_weather = weather_service.get_current_weather()
                if not current_weather:
                    logger.error(f"Failed to get weather data for {city_name}")
                    continue

                # Format message with city-specific hashtags
                message = self.formatter.format_current_weather(
                    current_weather, city_name, custom_hashtags=city.get("hashtags", [])
                )

                if not message:
                    logger.error(f"Failed to format weather message for {city_name}")
                    continue

                # Post to Twitter
                tweet_id = self.twitter_service.post_tweet(message)
                if tweet_id:
                    logger.info(
                        "Successfully posted weather update for %s (Tweet ID: %s)",
                        city_name,
                        tweet_id,
                    )
                else:
                    logger.warning(
                        "Skipped posting weather update for %s (rate limited or failed)",
                        city_name,
                    )

                # Small delay between city posts to avoid rate limiting
                import time

                time.sleep(5)

        except Exception as e:
            logger.error(f"Error in multi-city weather update: {e}")

    def post_current_weather_city(self, city_name):
        """Post current weather update for a specific city"""
        try:
            if city_name not in self.weather_services:
                logger.error(f"City {city_name} not configured")
                return False

            logger.info(f"Starting weather update for {city_name}")

            weather_service = self.weather_services[city_name]
            city_config = next(
                city for city in self.cities if city["name"] == city_name
            )

            # Get current weather
            current_weather = weather_service.get_current_weather()
            if not current_weather:
                logger.error(f"Failed to get weather data for {city_name}")
                return False

            # Format message
            message = self.formatter.format_current_weather(
                current_weather,
                city_name,
                custom_hashtags=city_config.get("hashtags", []),
            )

            if not message:
                logger.error(f"Failed to format weather message for {city_name}")
                return False

            # Post to Twitter
            success = self.twitter_service.post_tweet(message)
            if success:
                logger.info(f"Successfully posted weather update for {city_name}")
                return True
            else:
                logger.error(f"Failed to post weather update for {city_name}")
                return False

        except Exception as e:
            logger.error(f"Error posting weather for {city_name}: {e}")
            return False

    def get_available_cities(self):
        """Get list of configured cities"""
        return [city["name"] for city in self.cities]

    def test_all_cities(self):
        """Test weather data retrieval for all cities"""
        logger.info("Testing weather services for all cities...")

        for city in self.cities:
            city_name = city["name"]
            weather_service = self.weather_services[city_name]

            logger.info(f"Testing {city_name}...")
            current_weather = weather_service.get_current_weather()

            if current_weather:
                logger.info(
                    f"✅ {city_name}: {current_weather['temperature']}°C, {current_weather['description']}"
                )
            else:
                logger.error(f"❌ {city_name}: Failed to get weather data")
