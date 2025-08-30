#!/usr/bin/env python3
"""
Bratislava Weather Bot
Automated Twitter bot for posting weather updates for Bratislava, Slovakia
Now supports multiple cities including Nairobi and Kisumu, Kenya
"""

import sys
import argparse
import schedule
import time

from weather_service import WeatherService
from twitter_service import TwitterService
from message_formatter import MessageFormatter
from logger import logger

# Try to import multi-city functionality, fallback gracefully if not available
try:
    from multi_city_bot import MultiCityWeatherBot

    MULTI_CITY_AVAILABLE = True
except ImportError as e:
    logger.warning("Multi-city functionality not available: %s", e)
    MultiCityWeatherBot = None
    MULTI_CITY_AVAILABLE = False


class BratislavaWeatherBot:
    def __init__(self):
        self.weather_service = WeatherService()
        self.twitter_service = TwitterService()
        self.formatter = MessageFormatter()

    def post_current_weather(self):
        """Post current weather update"""
        try:
            logger.info("Starting current weather update")

            # Get current weather
            current_weather = self.weather_service.get_current_weather()
            if not current_weather:
                logger.error("Failed to get current weather data")
                return False

            # Check for extreme conditions
            extreme_conditions = self.weather_service.check_extreme_conditions(
                current_weather
            )

            # Post extreme weather alert if needed
            if extreme_conditions:
                alert_message = self.formatter.format_extreme_conditions(
                    current_weather, extreme_conditions
                )
                if alert_message:
                    self.twitter_service.post_tweet(alert_message)
                    logger.info("Posted extreme weather alert")

            # Format and post regular weather update
            message = self.formatter.format_current_weather(current_weather)
            tweet_id = self.twitter_service.post_tweet(message)

            if tweet_id:
                logger.info("Successfully posted current weather update")
                return True
            else:
                logger.error("Failed to post weather update")
                return False

        except Exception as e:
            logger.error("Error in post_current_weather: %s", e)
            return False

    def post_forecast(self, hours=6):
        """Post weather forecast"""
        try:
            logger.info("Starting forecast update for %d hours", hours)

            forecast_data = self.weather_service.get_weather_forecast(hours)
            if not forecast_data:
                logger.error("Failed to get forecast data")
                return False

            message = self.formatter.format_forecast(forecast_data, hours)
            if not message:
                logger.error("Failed to format forecast message")
                return False

            tweet_id = self.twitter_service.post_tweet(message)

            if tweet_id:
                logger.info("Successfully posted forecast update")
                return True
            else:
                logger.error("Failed to post forecast update")
                return False

        except Exception as e:
            logger.error("Error in post_forecast: %s", e)
            return False

    def post_weather_alerts(self):
        """Post weather alerts/warnings"""
        try:
            logger.info("Checking for weather alerts")

            alerts = self.weather_service.get_weather_alerts()
            if not alerts:
                logger.info("No weather alerts found")
                return True

            alert_messages = self.formatter.format_weather_alert(alerts)
            if not alert_messages:
                logger.warning("Failed to format weather alerts")
                return False

            # Post alerts as a thread if multiple, or single tweet
            if len(alert_messages) == 1:
                tweet_id = self.twitter_service.post_tweet(alert_messages[0])
                if tweet_id:
                    logger.info("Successfully posted weather alert")
                    return True
            else:
                tweet_ids = self.twitter_service.post_thread(alert_messages)
                if tweet_ids:
                    logger.info(
                        "Successfully posted weather alert thread with %d tweets",
                        len(tweet_ids),
                    )
                    return True

            logger.error("Failed to post weather alerts")
            return False

        except Exception as e:
            logger.error("Error in post_weather_alerts: %s", e)
            return False

    def post_daily_summary(self):
        """Post daily weather summary"""
        try:
            logger.info("Starting daily summary update")

            current_weather = self.weather_service.get_current_weather()
            forecast_data = self.weather_service.get_weather_forecast(24)

            if not current_weather:
                logger.error("Failed to get current weather for daily summary")
                return False

            message = self.formatter.format_daily_summary(
                current_weather, forecast_data
            )
            tweet_id = self.twitter_service.post_tweet(message)

            if tweet_id:
                logger.info("Successfully posted daily summary")
                return True
            else:
                logger.error("Failed to post daily summary")
                return False

        except Exception as e:
            logger.error("Error in post_daily_summary: %s", e)
            return False

    def run_hourly_update(self):
        """Run hourly weather update routine"""
        logger.info("=== Starting hourly weather update ===")

        success = True

        # Check and post weather alerts first
        if not self.post_weather_alerts():
            success = False

        # Post current weather
        if not self.post_current_weather():
            success = False

        if success:
            logger.info("=== Hourly update completed successfully ===")
        else:
            logger.warning("=== Hourly update completed with errors ===")

        return success

    def run_scheduled_tasks(self):
        """Set up and run scheduled tasks"""
        # Hourly weather updates
        schedule.every().hour.do(self.run_hourly_update)

        # Daily summary at 7 AM
        schedule.every().day.at("07:00").do(self.post_daily_summary)

        # 6-hour forecast twice a day (8 AM and 8 PM)
        schedule.every().day.at("08:00").do(self.post_forecast, hours=6)
        schedule.every().day.at("20:00").do(self.post_forecast, hours=6)

        logger.info("Scheduled tasks configured. Bot is now running...")

        # Initial update
        self.run_hourly_update()

        # Keep the bot running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    parser = argparse.ArgumentParser(description="Multi-City Weather Bot")
    parser.add_argument(
        "--mode",
        choices=[
            "current",
            "forecast",
            "alerts",
            "daily",
            "schedule",
            "test",
            "multi-city",
            "city",
        ],
        default="multi-city",
        help="Bot operation mode",
    )
    parser.add_argument(
        "--hours", type=int, default=6, help="Hours for forecast (default: 6)"
    )
    parser.add_argument(
        "--city",
        type=str,
        help="Specific city for single city operations (Bratislava, Nairobi, Kisumu)",
    )

    args = parser.parse_args()

    try:
        if args.mode == "multi-city":
            # Multi-city mode - post weather for all configured cities
            if not MULTI_CITY_AVAILABLE:
                logger.error(
                    "Multi-city mode not available. Falling back to single-city mode."
                )
                bot = BratislavaWeatherBot()
                success = bot.post_current_weather()
                sys.exit(0 if success else 1)

            multi_bot = MultiCityWeatherBot()
            multi_bot.post_current_weather_all_cities()
            sys.exit(0)

        elif args.mode == "city" and args.city:
            # Single city mode with specified city
            if not MULTI_CITY_AVAILABLE:
                if args.city.lower() == "bratislava":
                    logger.warning(
                        "Multi-city not available. Using single-city bot for Bratislava."
                    )
                    bot = BratislavaWeatherBot()
                    success = bot.post_current_weather()
                    sys.exit(0 if success else 1)
                else:
                    logger.error(
                        "Multi-city functionality required for %s but not available.",
                        args.city,
                    )
                    sys.exit(1)

            multi_bot = MultiCityWeatherBot()
            success = multi_bot.post_current_weather_city(args.city)
            sys.exit(0 if success else 1)

        elif args.mode == "test":
            if args.city:
                # Test specific city
                if not MULTI_CITY_AVAILABLE:
                    if args.city.lower() == "bratislava":
                        logger.warning(
                            "Multi-city not available. Testing single-city bot for Bratislava."
                        )
                        bot = BratislavaWeatherBot()
                        weather = bot.weather_service.get_current_weather()
                        if weather:
                            logger.info(
                                "✅ Test completed for Bratislava: %s°C, %s",
                                weather["temperature"],
                                weather["description"],
                            )
                        sys.exit(0 if weather else 1)
                    else:
                        logger.error(
                            "❌ Multi-city functionality required for %s but not available.",
                            args.city,
                        )
                        sys.exit(1)

                multi_bot = MultiCityWeatherBot()
                if args.city in multi_bot.get_available_cities():
                    success = multi_bot.post_current_weather_city(args.city)
                    logger.info("✅ Test completed for %s", args.city)
                    sys.exit(0 if success else 1)
                else:
                    logger.error(
                        "❌ City %s not configured. Available cities: %s",
                        args.city,
                        ", ".join(multi_bot.get_available_cities()),
                    )
                    sys.exit(1)
            else:
                # Test all cities
                if not MULTI_CITY_AVAILABLE:
                    logger.warning(
                        "Multi-city not available. Testing single-city bot only."
                    )
                    bot = BratislavaWeatherBot()
                    weather = bot.weather_service.get_current_weather()
                    if weather:
                        logger.info("✅ Single-city weather service working")
                    else:
                        logger.error("❌ Single-city weather service failed")
                        sys.exit(1)

                    account_info = bot.twitter_service.get_account_info()
                    if account_info:
                        logger.info(
                            "✅ Twitter service working - @%s", account_info["username"]
                        )
                    else:
                        logger.error("❌ Twitter service failed")
                        sys.exit(1)

                    logger.info("✅ All available tests passed!")
                    sys.exit(0)

                multi_bot = MultiCityWeatherBot()
                multi_bot.test_all_cities()

                # Also test the original single-city bot for backward compatibility
                logger.info("Testing original single-city bot...")
                bot = BratislavaWeatherBot()

                weather = bot.weather_service.get_current_weather()
                if weather:
                    logger.info("✅ Single-city weather service working")
                else:
                    logger.error("❌ Single-city weather service failed")
                    sys.exit(1)

                account_info = bot.twitter_service.get_account_info()
                if account_info:
                    logger.info(
                        "✅ Twitter service working - @%s", account_info["username"]
                    )
                else:
                    logger.error("❌ Twitter service failed")
                    sys.exit(1)

                logger.info("✅ All tests passed!")
                sys.exit(0)

        else:
            # Original single-city bot functionality (Bratislava)
            bot = BratislavaWeatherBot()

            if args.mode == "current":
                success = bot.post_current_weather()
                sys.exit(0 if success else 1)

            elif args.mode == "forecast":
                success = bot.post_forecast(args.hours)
                sys.exit(0 if success else 1)

            elif args.mode == "alerts":
                success = bot.post_weather_alerts()
                sys.exit(0 if success else 1)

            elif args.mode == "daily":
                success = bot.post_daily_summary()
                sys.exit(0 if success else 1)

            elif args.mode == "schedule":
                bot.run_scheduled_tasks()

            else:
                logger.error("Unknown mode: %s", args.mode)
                sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error("Fatal error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
