import requests
from datetime import datetime
import pytz
import config
from logger import logger


class WeatherService:
    def __init__(self, city_config=None):
        """
        Initialize weather service for a specific city
        Args:
            city_config: Dictionary containing city info (name, lat, lon, timezone, etc.)
                        If None, uses default config values for backward compatibility
        """
        self.api_key = config.OPENWEATHER_API_KEY
        self.base_url = config.OPENWEATHER_BASE_URL
        self.forecast_url = config.OPENWEATHER_FORECAST_URL

        if city_config:
            self.lat = city_config["latitude"]
            self.lon = city_config["longitude"]
            self.city_name = city_config["name"]
            self.country_code = city_config["country_code"]
            self.timezone = city_config["timezone"]
        else:
            # Backward compatibility
            self.lat = config.LATITUDE
            self.lon = config.LONGITUDE
            self.city_name = config.CITY_NAME
            self.country_code = config.COUNTRY_CODE
            self.timezone = config.TIMEZONE

    def get_current_weather(self):
        """Get current weather data from OpenWeatherMap"""
        try:
            url = f"{self.base_url}/weather"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "en",
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            logger.info("Successfully fetched current weather for %s", self.city_name)
            return self._parse_current_weather(data)

        except requests.exceptions.RequestException as e:
            logger.error("Error fetching current weather: %s", e)
            return None

    def get_weather_forecast(self, hours=24):
        """Get weather forecast using free tier forecast API"""
        try:
            url = f"{self.forecast_url}"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "metric",
                "lang": "en",
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            logger.info("Successfully fetched forecast for %s", self.city_name)
            return self._parse_forecast(data, hours)

        except requests.exceptions.RequestException as e:
            logger.error("Error fetching forecast: %s", e)
            return None

    def get_weather_alerts(self):
        """Get weather alerts - not available on free tier, return empty list"""
        logger.info("Weather alerts not available on free tier for %s", self.city_name)
        return []

    def _parse_current_weather(self, data):
        """Parse current weather data"""
        timezone = pytz.timezone(self.timezone)
        current_time = datetime.now(timezone)

        return {
            "timestamp": current_time,
            "temperature": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"].title(),
            "main": data["weather"][0]["main"],
            "icon": data["weather"][0]["icon"],
            "wind_speed": round(
                data.get("wind", {}).get("speed", 0) * 3.6, 1
            ),  # Convert m/s to km/h
            "wind_direction": data.get("wind", {}).get("deg", 0),
            "visibility": data.get("visibility", 0) / 1000,  # Convert to km
            "clouds": data["clouds"]["all"],
            "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"], timezone),
            "sunset": datetime.fromtimestamp(data["sys"]["sunset"], timezone),
        }

    def _parse_forecast(self, data, hours):
        """Parse forecast data from 2.5 API"""
        timezone = pytz.timezone(self.timezone)
        forecasts = []

        # 2.5 forecast API returns data in 3-hour intervals
        forecast_list = data.get("list", [])

        # Calculate how many 3-hour intervals we need for the requested hours
        intervals_needed = min(len(forecast_list), (hours // 3) + 1)

        for forecast_data in forecast_list[:intervals_needed]:
            forecast_time = datetime.fromtimestamp(forecast_data["dt"], timezone)

            # Extract rain data safely
            rain_mm = 0
            if "rain" in forecast_data:
                rain_mm += forecast_data["rain"].get("3h", 0)

            # Extract snow data safely
            if "snow" in forecast_data:
                rain_mm += forecast_data["snow"].get("3h", 0)

            forecasts.append(
                {
                    "timestamp": forecast_time,
                    "temperature": round(forecast_data["main"]["temp"], 1),
                    "feels_like": round(forecast_data["main"]["feels_like"], 1),
                    "humidity": forecast_data["main"]["humidity"],
                    "description": forecast_data["weather"][0]["description"].title(),
                    "main": forecast_data["weather"][0]["main"],
                    "wind_speed": round(
                        forecast_data.get("wind", {}).get("speed", 0) * 3.6, 1
                    ),  # Convert m/s to km/h
                    "precipitation": round(rain_mm, 1),
                }
            )

        return forecasts

    def _parse_alerts(self, alerts):
        """Parse weather alerts"""
        timezone = pytz.timezone(self.timezone)
        parsed_alerts = []

        for alert in alerts:
            parsed_alerts.append(
                {
                    "sender": alert.get("sender_name", "Weather Service"),
                    "event": alert.get("event", ""),
                    "description": alert.get("description", ""),
                    "start": datetime.fromtimestamp(alert["start"], timezone),
                    "end": datetime.fromtimestamp(alert["end"], timezone),
                    "tags": alert.get("tags", []),
                }
            )

        return parsed_alerts

    def check_extreme_conditions(self, weather_data):
        """Check for extreme weather conditions"""
        alerts = []

        if weather_data["temperature"] >= config.TEMPERATURE_HIGH_THRESHOLD:
            alerts.append(f"🔥 High temperature alert: {weather_data['temperature']}°C")

        if weather_data["temperature"] <= config.TEMPERATURE_LOW_THRESHOLD:
            alerts.append(f"🧊 Low temperature alert: {weather_data['temperature']}°C")

        if weather_data["wind_speed"] >= config.WIND_SPEED_THRESHOLD:
            alerts.append(f"💨 High wind alert: {weather_data['wind_speed']} km/h")

        return alerts
