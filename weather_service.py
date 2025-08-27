import requests
from datetime import datetime
import pytz
import config
from logger import logger


class WeatherService:
    def __init__(self):
        self.api_key = config.OPENWEATHER_API_KEY
        self.base_url = config.OPENWEATHER_BASE_URL
        self.onecall_url = config.OPENWEATHER_ONECALL_URL
        self.lat = config.LATITUDE
        self.lon = config.LONGITUDE
        self.city_name = config.CITY_NAME

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
        """Get weather forecast using One Call API 3.0"""
        try:
            url = f"{self.onecall_url}"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "metric",
                "exclude": "minutely,daily",
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
        """Get weather alerts/warnings"""
        try:
            url = f"{self.onecall_url}"
            params = {
                "lat": self.lat,
                "lon": self.lon,
                "appid": self.api_key,
                "units": "metric",
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            alerts = data.get("alerts", [])

            if alerts:
                logger.info(
                    "Found %d weather alerts for %s", len(alerts), self.city_name
                )
                return self._parse_alerts(alerts)
            else:
                logger.info("No weather alerts for %s", self.city_name)
                return []

        except requests.exceptions.RequestException as e:
            logger.error("Error fetching weather alerts: %s", e)
            return []

    def _parse_current_weather(self, data):
        """Parse current weather data"""
        timezone = pytz.timezone(config.TIMEZONE)
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
        """Parse forecast data"""
        timezone = pytz.timezone(config.TIMEZONE)
        forecasts = []

        for hour_data in data.get("hourly", [])[:hours]:
            forecast_time = datetime.fromtimestamp(hour_data["dt"], timezone)
            forecasts.append(
                {
                    "timestamp": forecast_time,
                    "temperature": round(hour_data["temp"], 1),
                    "feels_like": round(hour_data["feels_like"], 1),
                    "humidity": hour_data["humidity"],
                    "description": hour_data["weather"][0]["description"].title(),
                    "main": hour_data["weather"][0]["main"],
                    "wind_speed": round(
                        hour_data.get("wind_speed", 0) * 3.6, 1
                    ),  # Convert m/s to km/h
                    "precipitation": round(
                        hour_data.get("rain", {}).get("1h", 0)
                        + hour_data.get("snow", {}).get("1h", 0),
                        1,
                    ),
                }
            )

        return forecasts

    def _parse_alerts(self, alerts):
        """Parse weather alerts"""
        timezone = pytz.timezone(config.TIMEZONE)
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
