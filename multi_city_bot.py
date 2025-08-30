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
            logger.info(
                "=== Starting multi-city weather update for %d cities ===",
                len(self.cities),
            )

            for i, city in enumerate(self.cities, 1):
                city_name = city["name"]
                weather_service = self.weather_services[city_name]

                logger.info(
                    "[%d/%d] Processing weather for %s", i, len(self.cities), city_name
                )

                # Get current weather
                current_weather = weather_service.get_current_weather()
                if not current_weather:
                    logger.error("Failed to get weather data for %s", city_name)
                    continue

                # Format message with city-specific hashtags
                message = self.formatter.format_current_weather(
                    current_weather, city_name, custom_hashtags=city.get("hashtags", [])
                )

                if not message:
                    logger.error("Failed to format weather message for %s", city_name)
                    continue

                # Post to Twitter
                tweet_id = self.twitter_service.post_tweet(message)
                if tweet_id:
                    logger.info(
                        "✅ [%d/%d] Successfully posted weather update for %s (Tweet ID: %s)",
                        i,
                        len(self.cities),
                        city_name,
                        tweet_id,
                    )
                else:
                    logger.warning(
                        "⚠️ [%d/%d] Skipped posting weather update for %s (rate limited or failed)",
                        i,
                        len(self.cities),
                        city_name,
                    )

                # Small delay between city posts to avoid rate limiting
                import time

                if i < len(self.cities):  # Don't sleep after the last city
                    logger.info("⏱️ Waiting 5 seconds before next city...")
                    time.sleep(5)

            logger.info("=== Multi-city weather update completed ===")

        except Exception as e:
            logger.error("Error in multi-city weather update: %s", e)

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

    def post_forecast_all_cities(self, hours=6):
        """Post weather forecast for all cities"""
        try:
            logger.info(
                "=== Starting multi-city forecast update for %d cities (%d hours) ===",
                len(self.cities),
                hours,
            )

            overall_success = True
            for i, city in enumerate(self.cities, 1):
                city_name = city["name"]
                weather_service = self.weather_services[city_name]

                logger.info(
                    "[%d/%d] Processing forecast for %s", i, len(self.cities), city_name
                )

                try:
                    # Get forecast data
                    forecast_data = weather_service.get_weather_forecast(hours)
                    if not forecast_data:
                        logger.error("Failed to get forecast data for %s", city_name)
                        overall_success = False
                        continue

                    # Format forecast message
                    message = self.formatter.format_forecast(forecast_data, hours)
                    if not message:
                        logger.error(
                            "Failed to format forecast message for %s", city_name
                        )
                        overall_success = False
                        continue

                    # Post forecast
                    tweet_id = self.twitter_service.post_tweet(message)
                    if tweet_id:
                        logger.info("Successfully posted forecast for %s", city_name)
                    else:
                        logger.error("Failed to post forecast for %s", city_name)
                        overall_success = False

                    # Add delay between cities to avoid rate limiting
                    if i < len(self.cities):  # Don't sleep after last city
                        import time

                        time.sleep(5)

                except Exception as e:
                    logger.error("Error processing forecast for %s: %s", city_name, e)
                    overall_success = False
                    continue

            logger.info("=== Multi-city forecast update completed ===")
            return overall_success

        except Exception as e:
            logger.error("Error in post_forecast_all_cities: %s", e)
            return False

    def post_forecast_city(self, city_name, hours=6):
        """Post weather forecast for a specific city"""
        try:
            if city_name not in self.get_available_cities():
                logger.error("City %s not configured", city_name)
                return False

            logger.info("Starting forecast update for %s (%d hours)", city_name, hours)

            weather_service = self.weather_services[city_name]
            forecast_data = weather_service.get_weather_forecast(hours)

            if not forecast_data:
                logger.error("Failed to get forecast data for %s", city_name)
                return False

            message = self.formatter.format_forecast(forecast_data, hours)
            if not message:
                logger.error("Failed to format forecast message for %s", city_name)
                return False

            tweet_id = self.twitter_service.post_tweet(message)
            if tweet_id:
                logger.info("Successfully posted forecast for %s", city_name)
                return True
            else:
                logger.error("Failed to post forecast for %s", city_name)
                return False

        except Exception as e:
            logger.error("Error in post_forecast_city for %s: %s", city_name, e)
            return False

    def post_alerts_all_cities(self):
        """Post weather alerts for all cities"""
        try:
            logger.info(
                "=== Checking weather alerts for %d cities ===", len(self.cities)
            )

            overall_success = True
            alerts_found = False

            for i, city in enumerate(self.cities, 1):
                city_name = city["name"]
                weather_service = self.weather_services[city_name]

                logger.info(
                    "[%d/%d] Checking alerts for %s", i, len(self.cities), city_name
                )

                try:
                    # Check for weather alerts
                    alerts = weather_service.get_weather_alerts()
                    if not alerts:
                        logger.info("No weather alerts for %s", city_name)
                        continue

                    alerts_found = True
                    alert_messages = self.formatter.format_weather_alert(alerts)
                    if not alert_messages:
                        logger.warning(
                            "Failed to format weather alerts for %s", city_name
                        )
                        overall_success = False
                        continue

                    # Post alerts as a thread if multiple, or single tweet
                    if len(alert_messages) == 1:
                        tweet_id = self.twitter_service.post_tweet(alert_messages[0])
                        if tweet_id:
                            logger.info(
                                "Successfully posted weather alert for %s", city_name
                            )
                        else:
                            logger.error(
                                "Failed to post weather alert for %s", city_name
                            )
                            overall_success = False
                    else:
                        tweet_ids = self.twitter_service.post_thread(alert_messages)
                        if tweet_ids:
                            logger.info(
                                "Successfully posted weather alert thread for %s with %d tweets",
                                city_name,
                                len(tweet_ids),
                            )
                        else:
                            logger.error(
                                "Failed to post weather alert thread for %s", city_name
                            )
                            overall_success = False

                    # Add delay between cities to avoid rate limiting
                    if i < len(self.cities):  # Don't sleep after last city
                        import time

                        time.sleep(5)

                except Exception as e:
                    logger.error("Error processing alerts for %s: %s", city_name, e)
                    overall_success = False
                    continue

            if not alerts_found:
                logger.info("No weather alerts found for any city")

            logger.info("=== Multi-city alerts check completed ===")
            return overall_success

        except Exception as e:
            logger.error("Error in post_alerts_all_cities: %s", e)
            return False

    def post_alerts_city(self, city_name):
        """Post weather alerts for a specific city"""
        try:
            if city_name not in self.get_available_cities():
                logger.error("City %s not configured", city_name)
                return False

            logger.info("Checking weather alerts for %s", city_name)

            weather_service = self.weather_services[city_name]
            alerts = weather_service.get_weather_alerts()

            if not alerts:
                logger.info("No weather alerts for %s", city_name)
                return True  # No alerts is success

            alert_messages = self.formatter.format_weather_alert(alerts)
            if not alert_messages:
                logger.warning("Failed to format weather alerts for %s", city_name)
                return False

            # Post alerts as a thread if multiple, or single tweet
            if len(alert_messages) == 1:
                tweet_id = self.twitter_service.post_tweet(alert_messages[0])
                if tweet_id:
                    logger.info("Successfully posted weather alert for %s", city_name)
                    return True
            else:
                tweet_ids = self.twitter_service.post_thread(alert_messages)
                if tweet_ids:
                    logger.info(
                        "Successfully posted weather alert thread for %s with %d tweets",
                        city_name,
                        len(tweet_ids),
                    )
                    return True

            logger.error("Failed to post weather alerts for %s", city_name)
            return False

        except Exception as e:
            logger.error("Error in post_alerts_city for %s: %s", city_name, e)
            return False

    def post_daily_summary_all_cities(self):
        """Post daily weather summary for all cities"""
        try:
            logger.info(
                "=== Starting daily summary for %d cities ===", len(self.cities)
            )

            overall_success = True
            for i, city in enumerate(self.cities, 1):
                city_name = city["name"]
                weather_service = self.weather_services[city_name]

                logger.info(
                    "[%d/%d] Processing daily summary for %s",
                    i,
                    len(self.cities),
                    city_name,
                )

                try:
                    # Get current weather and forecast
                    current_weather = weather_service.get_current_weather()
                    forecast_data = weather_service.get_weather_forecast(24)

                    if not current_weather:
                        logger.error(
                            "Failed to get current weather for daily summary of %s",
                            city_name,
                        )
                        overall_success = False
                        continue

                    # Format daily summary message
                    message = self.formatter.format_daily_summary(
                        current_weather, forecast_data
                    )
                    if not message:
                        logger.error("Failed to format daily summary for %s", city_name)
                        overall_success = False
                        continue

                    # Post daily summary
                    tweet_id = self.twitter_service.post_tweet(message)
                    if tweet_id:
                        logger.info(
                            "Successfully posted daily summary for %s", city_name
                        )
                    else:
                        logger.error("Failed to post daily summary for %s", city_name)
                        overall_success = False

                    # Add delay between cities to avoid rate limiting
                    if i < len(self.cities):  # Don't sleep after last city
                        import time

                        time.sleep(5)

                except Exception as e:
                    logger.error(
                        "Error processing daily summary for %s: %s", city_name, e
                    )
                    overall_success = False
                    continue

            logger.info("=== Multi-city daily summary completed ===")
            return overall_success

        except Exception as e:
            logger.error("Error in post_daily_summary_all_cities: %s", e)
            return False

    def post_daily_summary_city(self, city_name):
        """Post daily weather summary for a specific city"""
        try:
            if city_name not in self.get_available_cities():
                logger.error("City %s not configured", city_name)
                return False

            logger.info("Starting daily summary for %s", city_name)

            weather_service = self.weather_services[city_name]
            current_weather = weather_service.get_current_weather()
            forecast_data = weather_service.get_weather_forecast(24)

            if not current_weather:
                logger.error(
                    "Failed to get current weather for daily summary of %s", city_name
                )
                return False

            message = self.formatter.format_daily_summary(
                current_weather, forecast_data
            )
            if not message:
                logger.error("Failed to format daily summary for %s", city_name)
                return False

            tweet_id = self.twitter_service.post_tweet(message)
            if tweet_id:
                logger.info("Successfully posted daily summary for %s", city_name)
                return True
            else:
                logger.error("Failed to post daily summary for %s", city_name)
                return False

        except Exception as e:
            logger.error("Error in post_daily_summary_city for %s: %s", city_name, e)
            return False

    def run_scheduled_tasks(self):
        """Run scheduled tasks for all cities"""
        try:
            import schedule
            import time

            logger.info("Setting up scheduled tasks for multi-city weather bot...")

            # Hourly weather updates for all cities
            schedule.every().hour.do(self.post_current_weather_all_cities)

            # Daily summary at 7 AM for all cities
            schedule.every().day.at("07:00").do(self.post_daily_summary_all_cities)

            # 6-hour forecast twice a day (8 AM and 8 PM) for all cities
            schedule.every().day.at("08:00").do(self.post_forecast_all_cities, hours=6)
            schedule.every().day.at("20:00").do(self.post_forecast_all_cities, hours=6)

            # Weather alerts check every 30 minutes
            schedule.every(30).minutes.do(self.post_alerts_all_cities)

            logger.info(
                "Scheduled tasks configured for multi-city bot. Starting initial update..."
            )

            # Run initial update
            self.post_current_weather_all_cities()

            # Keep the bot running
            logger.info("Multi-city weather bot is now running scheduled tasks...")
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        except KeyboardInterrupt:
            logger.info("Multi-city scheduled tasks stopped by user")
        except Exception as e:
            logger.error("Error in run_scheduled_tasks: %s", e)
            raise
