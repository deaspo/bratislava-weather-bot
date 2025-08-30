# Multi-City Weather Bot - Comprehensive Usage Guide

## 🌍 Overview
The Multi-City Weather Bot supports automated weather updates for three cities:
- **Nairobi**, Kenya 🇰🇪 (-1.2921°, 36.8219°)
- **Kisumu**, Kenya 🇰🇪 (-0.0917°, 34.7680°)  
- **Bratislava**, Slovakia 🇸🇰 (48.1486°, 17.1077°)

## 🎯 Operation Modes

### 1. Current Weather (`current`)
Posts current weather conditions with temperature, humidity, wind, and weather description.

**Multi-City (Default):**
```bash
# All cities (Nairobi → Kisumu → Bratislava)
python main.py --mode current

# Alternative syntax (same result)
python main.py                    # Default mode
python main.py --mode multi-city  # Explicit multi-city
```

**Single City:**
```bash
python main.py --mode current --city Nairobi
python main.py --mode current --city Kisumu
python main.py --mode current --city Bratislava
```

**Sample Output:**
- ✅ Posts current weather tweet for each city
- ⏱️ 5-second delay between cities to avoid rate limiting
- 🏷️ City-specific hashtags included
- 📊 Comprehensive weather metrics

### 2. Weather Forecast (`forecast`)
Posts weather forecast for specified hours (1-24+ hours supported).

**Multi-City:**
```bash
# All cities with 6-hour forecast (default)
python main.py --mode forecast

# All cities with custom hours
python main.py --mode forecast --hours 1    # 1-hour forecast
python main.py --mode forecast --hours 3    # 3-hour forecast  
python main.py --mode forecast --hours 12   # 12-hour forecast
python main.py --mode forecast --hours 24   # 24-hour forecast
```

**Single City:**
```bash
python main.py --mode forecast --city Nairobi --hours 6
python main.py --mode forecast --city Kisumu --hours 12
python main.py --mode forecast --city Bratislava --hours 3
```

**Forecast Features:**
- 🔮 Hourly weather predictions
- 🌡️ Temperature trends
- 🌧️ Precipitation probability
- 💨 Wind conditions
- ⏰ Time-specific forecasts

### 3. Weather Alerts (`alerts`)
Checks and posts weather alerts, warnings, and severe weather notifications.

**Multi-City:**
```bash
# Check alerts for all cities
python main.py --mode alerts
```

**Single City:**
```bash
python main.py --mode alerts --city Nairobi
python main.py --mode alerts --city Kisumu
python main.py --mode alerts --city Bratislava
```

**Alert Features:**
- ⚠️ Severe weather warnings
- 🌪️ Storm notifications
- ❄️ Temperature extremes
- 🌊 Flooding alerts
- ⏰ Time-based alert windows

**Note:** Weather alerts require premium OpenWeatherMap API access. With free tier, the bot logs "Weather alerts not available on free tier" and returns successfully.

### 4. Daily Summary (`daily`)
Posts comprehensive daily weather summary with current conditions and forecast.

**Multi-City:**
```bash
# Daily summary for all cities
python main.py --mode daily
```

**Single City:**
```bash
python main.py --mode daily --city Nairobi
python main.py --mode daily --city Kisumu  
python main.py --mode daily --city Bratislava
```

**Daily Summary Includes:**
- 🌅 Current conditions
- 🌡️ Daily temperature range (min/max)
- 🔮 Tonight's forecast
- 🌤️ Tomorrow's preview
- 💧 Humidity and wind details
- 📅 Date and time stamps

### 5. Multi-City Update (`multi-city`)
Explicit multi-city mode that posts current weather for all cities in sequence.

```bash
python main.py --mode multi-city

# This is the same as:
python main.py                    # Default behavior
python main.py --mode current     # Current weather for all cities
```

**Execution Order:**
1. 🇰🇪 **Nairobi** (first)
2. 🇰🇪 **Kisumu** (second, after 5-second delay)
3. 🇸🇰 **Bratislava** (third, after another 5-second delay)

### 6. Scheduled Tasks (`schedule`)
Runs comprehensive automated scheduling with multiple daily events.

```bash
python main.py --mode schedule
```

**Automated Schedule:**

| Time | Frequency | Action | Cities |
|------|-----------|--------|--------|
| Every hour | `0 * * * *` | Current weather | All 3 cities |
| 7:00 AM daily | `0 7 * * *` | Daily summary | All 3 cities |
| 8:00 AM daily | `0 8 * * *` | 6-hour forecast | All 3 cities |
| 8:00 PM daily | `0 20 * * *` | 6-hour forecast | All 3 cities |
| Every 30 min | `*/30 * * * *` | Weather alerts check | All 3 cities |

**Schedule Features:**
- 🔄 **Continuous operation** - Runs indefinitely until interrupted
- ⏰ **Precise timing** - Uses Python `schedule` library
- 🎯 **Initial update** - Runs current weather update on startup
- 🛡️ **Error handling** - Continues running even if individual updates fail
- 📊 **Comprehensive logging** - Detailed logs for all scheduled activities

### 7. Test Mode (`test`)
Tests weather data retrieval without posting to Twitter (development/debugging).

**Test All Cities:**
```bash
python main.py --mode test
```

**Test Specific City:**
```bash
python main.py --mode test --city Nairobi
python main.py --mode test --city Kisumu
python main.py --mode test --city Bratislava
```

**Test Features:**
- ✅ **API connectivity** - Tests OpenWeatherMap API access
- 🌡️ **Data validation** - Verifies weather data structure
- 🐦 **Twitter authentication** - Confirms Twitter API access
- 📊 **Results display** - Shows temperature and conditions
- 🚫 **No posting** - Safe for development and debugging

## 🎛️ Command Line Options

### Required Arguments
None - the bot defaults to multi-city current weather mode.

### Optional Arguments

| Argument | Choices | Default | Description |
|----------|---------|---------|-------------|
| `--mode` | `current`, `forecast`, `alerts`, `daily`, `schedule`, `test`, `multi-city` | `multi-city` | Bot operation mode |
| `--hours` | 1-24+ integer | `6` | Hours for forecast (only used with `forecast` mode) |
| `--city` | `Nairobi`, `Kisumu`, `Bratislava` | None | Target specific city (if not specified, operates on all cities) |

### Help Command
```bash
python main.py --help
```

## 💡 Usage Examples

### Morning Weather Routine
```bash
# Start the day with daily summaries
python main.py --mode daily

# Follow up with 6-hour forecasts  
python main.py --mode forecast --hours 6

# Check for any weather alerts
python main.py --mode alerts
```

### Hourly Production Updates
```bash
# Standard hourly update (used in cron jobs)
python main.py

# Explicit multi-city mode (same result)
python main.py --mode multi-city
```

### City-Specific Operations
```bash
# Focus on Nairobi weather
python main.py --mode current --city Nairobi
python main.py --mode forecast --city Nairobi --hours 12
python main.py --mode daily --city Nairobi

# Emergency Kisumu weather check
python main.py --mode alerts --city Kisumu
python main.py --mode test --city Kisumu

# Bratislava evening forecast
python main.py --mode forecast --city Bratislava --hours 3
```

### Development and Testing
```bash
# Test all systems without posting
python main.py --mode test

# Test individual city APIs
python main.py --mode test --city Nairobi

# Debug specific functionality
python main.py --mode forecast --city Kisumu --hours 1
```

### Long-Running Operations
```bash
# Production scheduling (runs indefinitely)
python main.py --mode schedule

# Alternative: Use systemd or supervisor for production
# This command blocks and runs scheduled tasks continuously
```

## 🌍 City Configuration Details

Each city has specific configuration for optimal weather reporting:

### Nairobi, Kenya 🇰🇪
- **Coordinates**: -1.2921°, 36.8219°
- **Timezone**: EAT (UTC+3)
- **Hashtags**: `#NairobiWeather #KenyaWeather`
- **Climate**: Subtropical highland climate
- **Typical Conditions**: Mild temperatures year-round, rainy seasons

### Kisumu, Kenya 🇰🇪  
- **Coordinates**: -0.0917°, 34.7680°
- **Timezone**: EAT (UTC+3)
- **Hashtags**: `#KisumuWeather #KenyaWeather`
- **Climate**: Tropical savanna climate
- **Typical Conditions**: Warm and humid, near Lake Victoria

### Bratislava, Slovakia 🇸🇰
- **Coordinates**: 48.1486°, 17.1077°
- **Timezone**: CET/CEST (UTC+1/+2)
- **Hashtags**: `#BratislavaWeather #SlovakiaWeather`
- **Climate**: Continental climate
- **Typical Conditions**: Four distinct seasons, cold winters, warm summers

## 🚀 Production Deployment

### Docker/Caprover Deployment
The production environment uses cron-based scheduling:

```bash
# Hourly cron job (runs every hour at minute 0)
0 * * * * cd /app && python main.py --mode multi-city
```

### Rate Limiting Management
- **5-second delays** between city posts
- **Automatic rate limit detection** via Tweepy
- **Graceful degradation** - continues with remaining cities if one fails
- **Production-safe** - respects Twitter API limits

### Monitoring and Health Checks
```bash
# Check if bot is responding
curl http://your-domain.com/health

# Detailed status information
curl http://your-domain.com/status

# View recent activity
curl http://your-domain.com/logs
```

## 🛠️ Error Handling

The bot includes comprehensive error handling:

### API Failures
- **OpenWeatherMap API errors** - Logs error, continues with other cities
- **Twitter API rate limits** - Waits or skips based on Tweepy configuration
- **Network connectivity issues** - Retries and logs failures

### Configuration Errors  
- **Invalid city names** - Shows available cities and exits
- **Missing API keys** - Clear error messages with setup guidance
- **Invalid time parameters** - Uses sensible defaults

### Runtime Errors
- **Malformed weather data** - Skips affected city, continues with others
- **Tweet formatting issues** - Logs error details for debugging
- **Schedule conflicts** - Independent scheduling prevents cascading failures

## 📊 Logging and Debugging

### Log Levels
- **INFO**: Normal operations, successful posts, scheduling events
- **WARNING**: Rate limits, skipped operations, non-critical issues  
- **ERROR**: API failures, configuration problems, tweet posting failures

### Debug Information
- **API request/response details**
- **Tweet content before posting**
- **Scheduling and timing information**
- **City processing order and delays**

### Log Files (local deployment)
```bash
tail -f logs/weather-bot.log    # General application logs
tail -f logs/cron.log          # Cron job execution logs
tail -f logs/error.log         # Error-specific logs
```

## 🔧 Customization

### Adding New Cities
1. Update `config.py` with new city coordinates and hashtags
2. The bot automatically creates weather services for all configured cities
3. Test with `python main.py --mode test --city NewCityName`

### Modifying Schedules
Edit the `run_scheduled_tasks()` method in `multi_city_bot.py`:
```python
# Custom scheduling examples
schedule.every(2).hours.do(self.post_current_weather_all_cities)  # Every 2 hours
schedule.every().day.at("06:00").do(self.post_daily_summary_all_cities)  # 6 AM daily
schedule.every().monday.at("09:00").do(self.post_forecast_all_cities, hours=12)  # Monday 9 AM
```

### Tweet Formatting
Modify `message_formatter.py` to customize:
- **Emoji selections**
- **Hashtag strategies** 
- **Message templates**
- **Weather condition descriptions**

---

## 🆘 Troubleshooting

### Common Issues

**"City not configured" error:**
```bash
python main.py --mode test  # See available cities
```

**Rate limiting issues:**
- Reduce posting frequency
- Check Twitter API limits
- Verify API credentials

**Weather data not found:**
- Verify OpenWeatherMap API key
- Check city coordinates in config.py
- Test with `--mode test`

**Import errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version compatibility

### Getting Help
- Check logs for detailed error messages
- Use test mode to debug without posting
- Verify API credentials and limits
- Review configuration files for typos
