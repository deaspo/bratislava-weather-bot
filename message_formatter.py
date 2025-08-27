from datetime import datetime
import config


class MessageFormatter:
    def __init__(self):
        self.city_name = config.CITY_NAME
        self.country_code = config.COUNTRY_CODE

    def format_current_weather(self, weather_data, city_name=None, custom_hashtags=None):
        """Format current weather into a tweet message"""
        city = city_name or self.city_name
        emojis = self._get_weather_emoji(weather_data["main"])
        temp_emoji = self._get_temperature_emoji(weather_data["temperature"])

        # Determine country flag based on city
        if city_name:
            if city_name in ["Nairobi", "Kisumu"]:
                flag = "🇰🇪"
            elif city_name == "Bratislava":
                flag = "🇸🇰"
            else:
                flag = ""
        else:
            flag = "🇸🇰"  # Default for Bratislava

        message = f"{emojis} Weather Update for {city} {flag}\n\n"
        message += f"{temp_emoji} {weather_data['temperature']}°C (feels like {weather_data['feels_like']}°C)\n"
        message += f"🌡️ {weather_data['description']}\n"
        message += f"💧 Humidity: {weather_data['humidity']}%\n"
        message += f"💨 Wind: {weather_data['wind_speed']} km/h\n"

        if weather_data["visibility"] < 10:
            message += f"👁️ Visibility: {weather_data['visibility']} km\n"

        message += f"\n⏰ {weather_data['timestamp'].strftime('%H:%M %d/%m/%Y')}"
        
        # Add custom hashtags if provided
        if custom_hashtags:
            hashtag_str = " ".join(custom_hashtags)
            message += f"\n\n{hashtag_str}"

        return message

    def format_forecast(self, forecast_data, hours=6):
        """Format weather forecast into a tweet message"""
        if not forecast_data:
            return None

        message = f"📅 {hours}h Forecast for {self.city_name} 🇸🇰\n\n"

        for forecast in forecast_data[:hours]:
            hour = forecast["timestamp"].strftime("%H:%M")
            temp = forecast["temperature"]
            desc = forecast["description"]
            emoji = self._get_weather_emoji(forecast["main"])

            message += f"{hour}: {emoji} {temp}°C - {desc}\n"

            if forecast["precipitation"] > 0:
                message += f"  🌧️ {forecast['precipitation']}mm\n"

        message += f"\n⏰ Updated: {datetime.now().strftime('%H:%M %d/%m/%Y')}"

        return message

    def format_weather_alert(self, alerts):
        """Format weather alerts into a tweet message"""
        if not alerts:
            return None

        messages = []

        for alert in alerts:
            message = f"⚠️ WEATHER ALERT for {self.city_name} 🇸🇰\n\n"
            message += f"📢 {alert['event']}\n"
            message += f"🏢 Source: {alert['sender']}\n"
            message += f"⏰ From: {alert['start'].strftime('%H:%M %d/%m')}\n"
            message += f"⏰ Until: {alert['end'].strftime('%H:%M %d/%m')}\n\n"

            # Truncate description if too long
            description = alert["description"]
            if len(description) > 100:
                description = description[:97] + "..."

            message += f"📝 {description}"

            messages.append(message)

        return messages

    def format_extreme_conditions(self, weather_data, conditions):
        """Format extreme weather conditions alert"""
        if not conditions:
            return None

        message = f"🚨 EXTREME WEATHER ALERT\n{self.city_name} 🇸🇰\n\n"

        for condition in conditions:
            message += f"{condition}\n"

        message += f"\nCurrent: {weather_data['temperature']}°C\n"
        message += f"Condition: {weather_data['description']}\n"
        message += f"⏰ {weather_data['timestamp'].strftime('%H:%M %d/%m/%Y')}"

        return message

    def format_daily_summary(self, current_weather, forecast_data):
        """Format daily weather summary"""
        emojis = self._get_weather_emoji(current_weather["main"])

        message = f"🌅 Daily Weather Summary\n{self.city_name} 🇸🇰\n\n"
        message += f"{emojis} Current: {current_weather['temperature']}°C\n"
        message += f"🌡️ {current_weather['description']}\n\n"

        if forecast_data:
            # Get temperature range for today
            temps = [f["temperature"] for f in forecast_data[:24]]  # Next 24 hours
            min_temp = min(temps)
            max_temp = max(temps)

            message += f"📊 Today's Range: {min_temp}°C - {max_temp}°C\n"

        message += f"🌅 Sunrise: {current_weather['sunrise'].strftime('%H:%M')}\n"
        message += f"🌇 Sunset: {current_weather['sunset'].strftime('%H:%M')}\n"
        message += "\n#BratislavaWeather #Slovakia"

        return message

    def _get_weather_emoji(self, condition):
        """Get emoji based on weather condition"""
        emoji_map = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Drizzle": "🌦️",
            "Thunderstorm": "⛈️",
            "Snow": "❄️",
            "Mist": "🌫️",
            "Fog": "🌫️",
            "Haze": "🌫️",
            "Smoke": "🌫️",
            "Sand": "🌪️",
            "Dust": "🌪️",
            "Ash": "🌋",
            "Squall": "💨",
            "Tornado": "🌪️",
        }
        return emoji_map.get(condition, "🌤️")

    def _get_temperature_emoji(self, temperature):
        """Get emoji based on temperature"""
        if temperature >= 30:
            return "🔥"
        elif temperature >= 25:
            return "🌡️"
        elif temperature >= 15:
            return "🌤️"
        elif temperature >= 5:
            return "🧥"
        elif temperature >= 0:
            return "🧊"
        else:
            return "❄️"

    def create_hashtags(self):
        """Create relevant hashtags"""
        return "#BratislavaWeather #Slovakia #Počasie #Bratislava #WeatherUpdate"
