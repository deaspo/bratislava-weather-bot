#!/usr/bin/env python3
"""
Python-based scheduler for multi-city weather bot
More reliable than cron in Docker containers
"""

import schedule
import time
import subprocess
import logging
import os
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs/scheduler.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)


def run_weather_update():
    """Run the multi-city weather update"""
    try:
        logger.info("🌍 Starting scheduled multi-city weather update...")

        # Open log file to stream output directly, preventing deadlocks
        with open("logs/multi_city_cron.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- {datetime.now()} ---\n")

            # Use Popen to run the command and redirect stdout/stderr directly to the log file.
            # This is a more robust method that avoids pipe buffer deadlocks.
            # The '-u' flag ensures the child process's output is unbuffered.
            process = subprocess.Popen(
                ["python3", "-u", "main.py", "--mode", "multi-city"],
                stdout=f,
                stderr=subprocess.STDOUT,
                text=True,
                cwd="/app",
            )

            # Wait for the process to complete and get the return code
            return_code = process.wait()

        if return_code == 0:
            logger.info("✅ Multi-city weather update completed successfully")
        else:
            logger.error("❌ Weather update failed with return code %s", return_code)

    except Exception:
        logger.exception("❌ Exception during weather update")


def test_heartbeat():
    """Test function to verify scheduler is working"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{timestamp}: Python scheduler test - I'm alive!\n"

        with open("logs/scheduler_test.log", "a") as f:
            f.write(message)

        logger.info("💓 Scheduler heartbeat logged")

    except Exception as e:
        logger.error(f"❌ Heartbeat test failed: {e}")


def main():
    """Main scheduler function"""
    logger.info("🚀 Starting Python-based weather bot scheduler...")

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)

    # Schedule the weather updates every hour at minute 0
    schedule.every().hour.at(":00").do(run_weather_update)

    # Schedule test heartbeat every 5 minutes for debugging
    schedule.every(5).minutes.do(test_heartbeat)

    # Run initial test to verify everything works
    logger.info("🧪 Running initial weather update...")
    run_weather_update()

    logger.info("📅 Scheduled tasks:")
    logger.info("   - Weather updates: Every hour at :00")
    logger.info("   - Test heartbeat: Every 5 minutes")
    logger.info("   - Logs: scheduler.log, scheduler_test.log, multi_city_cron.log")

    # Keep running and check for scheduled tasks
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            logger.info("🛑 Scheduler stopped by user")
            break
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")
            time.sleep(60)  # Wait a minute before retrying


if __name__ == "__main__":
    main()
