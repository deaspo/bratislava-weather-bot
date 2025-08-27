import os
from dotenv import load_dotenv

load_dotenv()

# Twitter API Configuration
TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# OpenWeatherMap API Configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
OPENWEATHER_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"

# Multi-City Configuration
CITIES = [
    {
        "name": "Bratislava",
        "country_code": "SK",
        "latitude": 48.1482,
        "longitude": 17.1067,
        "timezone": "Europe/Bratislava",
        "hashtags": ["#Bratislava", "#Slovakia", "#Weather"]
    },
    {
        "name": "Nairobi",
        "country_code": "KE", 
        "latitude": -1.2921,
        "longitude": 36.8219,
        "timezone": "Africa/Nairobi",
        "hashtags": ["#Nairobi", "#Kenya", "#Weather"]
    },
    {
        "name": "Kisumu",
        "country_code": "KE",
        "latitude": -0.1022,
        "longitude": 34.7617,
        "timezone": "Africa/Nairobi",
        "hashtags": ["#Kisumu", "#Kenya", "#Weather"]
    }
]

# Backward compatibility for single city mode
CITY_NAME = os.getenv("OPENWEATHER_CITY", "Bratislava")
COUNTRY_CODE = os.getenv("OPENWEATHER_COUNTRY_CODE", "SK")
LATITUDE = float(os.getenv("LATITUDE", "48.1482"))
LONGITUDE = float(os.getenv("LONGITUDE", "17.1067"))
TIMEZONE = os.getenv("TIMEZONE", "Europe/Bratislava")

# Bot Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Weather thresholds for alerts
TEMPERATURE_HIGH_THRESHOLD = 35  # °C
TEMPERATURE_LOW_THRESHOLD = -15  # °C
WIND_SPEED_THRESHOLD = 50  # km/h
RAIN_THRESHOLD = 10  # mm/h
