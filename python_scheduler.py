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
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_weather_update():
    """Run the multi-city weather update"""
    try:
        logger.info("🌍 Starting scheduled multi-city weather update...")
        
        # Run the main bot command
        result = subprocess.run([
            'python3', 'main.py', '--mode', 'multi-city'
        ], 
        capture_output=True, 
        text=True, 
        cwd='/app'
        )
        
        if result.returncode == 0:
            logger.info("✅ Multi-city weather update completed successfully")
        else:
            logger.error(f"❌ Weather update failed with return code {result.returncode}")
            logger.error(f"Error output: {result.stderr}")
            
        # Log the output
        with open('logs/multi_city_cron.log', 'a') as f:
            f.write(f"\n--- {datetime.now()} ---\n")
            f.write(result.stdout)
            if result.stderr:
                f.write(f"ERRORS:\n{result.stderr}")
            f.write("\n")
            
    except Exception as e:
        logger.error(f"❌ Exception during weather update: {e}")

def test_heartbeat():
    """Test function to verify scheduler is working"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{timestamp}: Python scheduler test - I'm alive!\n"
        
        with open('logs/scheduler_test.log', 'a') as f:
            f.write(message)
            
        logger.info("💓 Scheduler heartbeat logged")
        
    except Exception as e:
        logger.error(f"❌ Heartbeat test failed: {e}")

def main():
    """Main scheduler function"""
    logger.info("🚀 Starting Python-based weather bot scheduler...")
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
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
