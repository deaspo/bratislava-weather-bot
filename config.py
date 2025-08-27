import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API Configuration
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
OPENWEATHER_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"

# Location Configuration
CITY_NAME = os.getenv("CITY_NAME", "Bratislava")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", "SK")
LATITUDE = float(os.getenv("LATITUDE", "48.1482"))
LONGITUDE = float(os.getenv("LONGITUDE", "17.1067"))

# Bot Configuration
TIMEZONE = os.getenv("TIMEZONE", "Europe/Bratislava")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Weather thresholds for alerts
TEMPERATURE_HIGH_THRESHOLD = 30  # °C
TEMPERATURE_LOW_THRESHOLD = -10  # °C
WIND_SPEED_THRESHOLD = 50  # km/h
RAIN_THRESHOLD = 10  # mm/h
