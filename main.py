#!/usr/bin/env python3
"""
Multi-City Weather Bot
Automated Twitter bot for posting weather updates for multiple cities
Supports Bratislava (Slovakia), Nairobi and Kisumu (Kenya)
"""

import sys
import argparse

# Try to import multi-city functionality
try:
    from multi_city_bot import MultiCityWeatherBot
    from logger import logger

    MULTI_CITY_AVAILABLE = True
except ImportError as e:
    print(f"Error: Multi-city functionality not available: {e}")
    MultiCityWeatherBot = None
    MULTI_CITY_AVAILABLE = False
    sys.exit(1)


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
        help="Specific city for single city operations (Bratislava, Nairobi, Kisumu). If not specified, operates on all cities.",
    )

    args = parser.parse_args()

    try:
        # Check if multi-city functionality is available
        if not MULTI_CITY_AVAILABLE:
            logger.error("Multi-city functionality not available. Cannot proceed.")
            sys.exit(1)

        # Initialize multi-city bot for all operations
        multi_bot = MultiCityWeatherBot()

        if args.mode == "multi-city":
            # Post weather for all configured cities
            multi_bot.post_current_weather_all_cities()
            sys.exit(0)

        elif args.mode == "city" and args.city:
            # Single city mode with specified city
            success = multi_bot.post_current_weather_city(args.city)
            sys.exit(0 if success else 1)

        elif args.mode == "current":
            # Post current weather for all cities
            multi_bot.post_current_weather_all_cities()
            sys.exit(0)

        elif args.mode == "forecast":
            # Post forecast for all cities or specific city
            if args.city:
                if args.city in multi_bot.get_available_cities():
                    logger.info(
                        "Running forecast for %s (%d hours)", args.city, args.hours
                    )
                    success = multi_bot.post_forecast_city(args.city, args.hours)
                    sys.exit(0 if success else 1)
                else:
                    logger.error(
                        "❌ City %s not configured. Available cities: %s",
                        args.city,
                        ", ".join(multi_bot.get_available_cities()),
                    )
                    sys.exit(1)
            else:
                logger.info("Running forecast for all cities (%d hours)", args.hours)
                success = multi_bot.post_forecast_all_cities(args.hours)
                sys.exit(0 if success else 1)

        elif args.mode == "alerts":
            # Check weather alerts for all cities or specific city
            if args.city:
                if args.city in multi_bot.get_available_cities():
                    logger.info("Checking alerts for %s", args.city)
                    success = multi_bot.post_alerts_city(args.city)
                    sys.exit(0 if success else 1)
                else:
                    logger.error(
                        "❌ City %s not configured. Available cities: %s",
                        args.city,
                        ", ".join(multi_bot.get_available_cities()),
                    )
                    sys.exit(1)
            else:
                logger.info("Checking weather alerts for all cities")
                success = multi_bot.post_alerts_all_cities()
                sys.exit(0 if success else 1)

        elif args.mode == "daily":
            # Post daily summary for all cities or specific city
            if args.city:
                if args.city in multi_bot.get_available_cities():
                    logger.info("Running daily summary for %s", args.city)
                    success = multi_bot.post_daily_summary_city(args.city)
                    sys.exit(0 if success else 1)
                else:
                    logger.error(
                        "❌ City %s not configured. Available cities: %s",
                        args.city,
                        ", ".join(multi_bot.get_available_cities()),
                    )
                    sys.exit(1)
            else:
                logger.info("Running daily summary for all cities")
                success = multi_bot.post_daily_summary_all_cities()
                sys.exit(0 if success else 1)

        elif args.mode == "schedule":
            # Run scheduled tasks for multi-city bot
            logger.info("Starting multi-city scheduled tasks...")
            multi_bot.run_scheduled_tasks()
            # This will run indefinitely until interrupted

        elif args.mode == "test":
            if args.city:
                # Test specific city
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
                multi_bot.test_all_cities()
                logger.info("✅ All tests passed!")
                sys.exit(0)

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
