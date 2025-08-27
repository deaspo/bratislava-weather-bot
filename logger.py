import logging
import os
from datetime import datetime
import config


def setup_logger():
    """Setup logging configuration"""

    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure logging
    log_filename = f"logs/weather_bot_{datetime.now().strftime('%Y%m%d')}.log"

    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler(),  # Also log to console
        ],
    )

    return logging.getLogger(__name__)


logger = setup_logger()
