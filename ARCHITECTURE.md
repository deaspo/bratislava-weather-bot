# Multi-City Weather Bot Architecture

## 🏗️ System Overview

The Multi-City Weather Bot is designed as a scalable, maintainable system supporting weather updates for multiple cities worldwide. It uses a modular architecture with clear separation of concerns.

## 📐 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Main Entry Point                        │
│                          main.py                               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Multi-City Bot Core                          │
│                  multi_city_bot.py                             │
├─────────────────┬───────────────┬───────────────┬───────────────┤
│  City Manager   │ Weather Ops   │  Twitter Ops  │  Scheduling   │
│                 │               │               │               │
│ • City Config   │ • Current     │ • Tweet Posts │ • Cron Tasks  │
│ • City Loop     │ • Forecast    │ • Rate Limits │ • Intervals   │
│ • Error Handle  │ • Alerts      │ • Threading   │ • Automation  │
│                 │ • Daily       │               │               │
└─────────────────┼───────────────┼───────────────┼───────────────┘
                  │               │               │
                  ▼               ▼               ▼
        ┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
        │ Weather Service │ │ Twitter API │ │  Scheduler  │
        │ weather_service │ │twitter_svc  │ │  schedule   │
        │     .py         │ │   .py       │ │   library   │
        └─────────────────┘ └─────────────┘ └─────────────┘
                  │               │
                  ▼               ▼
        ┌─────────────────┐ ┌─────────────┐
        │ OpenWeatherMap  │ │ Twitter API │
        │      API        │ │     v2      │
        └─────────────────┘ └─────────────┘
```

## 🏛️ Core Components

### 1. Main Entry Point (`main.py`)
**Purpose**: Command-line interface and mode routing
```python
# Key Features:
- Argument parsing (--mode, --city, --hours)
- Multi-city bot initialization
- Mode routing (current, forecast, alerts, daily, schedule, test)
- Error handling and exit codes
- Help system
```

**Modes Supported**:
- `current` - Current weather (all cities or specific city)
- `forecast` - Weather forecast (1-24+ hours)
- `alerts` - Weather warnings and alerts
- `daily` - Daily weather summary
- `schedule` - Automated scheduling
- `test` - Development testing
- `multi-city` - Explicit multi-city current weather

### 2. Multi-City Bot Core (`multi_city_bot.py`)
**Purpose**: Orchestrates multi-city weather operations
```python
class MultiCityWeatherBot:
    def __init__(self):
        # Initialize services for all configured cities
        # Create weather services per city
        # Setup Twitter service (shared)
        # Configure message formatter
```

**Key Methods**:
- `post_current_weather_all_cities()` - Current weather for all cities
- `post_current_weather_city(city_name)` - Current weather for specific city
- `post_forecast_all_cities(hours)` - Forecast for all cities
- `post_forecast_city(city_name, hours)` - Forecast for specific city
- `post_alerts_all_cities()` - Alerts for all cities
- `post_alerts_city(city_name)` - Alerts for specific city
- `post_daily_summary_all_cities()` - Daily summary for all cities
- `post_daily_summary_city(city_name)` - Daily summary for specific city
- `run_scheduled_tasks()` - Comprehensive automation
- `test_all_cities()` - Testing without posting

### 3. Weather Service (`weather_service.py`)
**Purpose**: OpenWeatherMap API integration per city
```python
class WeatherService:
    def __init__(self, city_config):
        # City-specific configuration
        # API endpoints and parameters
        # Error handling setup
```

**API Integration**:
- **Current Weather**: `api.openweathermap.org/data/2.5/weather`
- **Forecast**: `api.openweathermap.org/data/2.5/forecast`
- **Rate Limiting**: Respects free tier limits (1,000 calls/day)

### 4. Twitter Service (`twitter_service.py`)
**Purpose**: Twitter API v2 integration with rate limiting
```python
class TwitterService:
    def __init__(self):
        # Twitter API v2 client
        # Rate limiting configuration
        # Error handling
```

**Features**:
- Single tweet posting
- Thread posting (for alerts)
- Automatic rate limit handling
- Tweet ID tracking
- Error recovery

### 5. Message Formatter (`message_formatter.py`)
**Purpose**: Weather data to tweet conversion
```python
class MessageFormatter:
    def format_current_weather(weather, city, hashtags):
    def format_forecast(forecast, hours):
    def format_weather_alert(alerts):
    def format_daily_summary(current, forecast):
```

**Features**:
- Weather-appropriate emojis
- City-specific hashtags
- Temperature and condition formatting
- Timezone-aware timestamps
- Character limit compliance

### 6. Configuration (`config.py`)
**Purpose**: Multi-city configuration management
```python
CITIES = [
    {
        "name": "Nairobi",
        "lat": -1.2921,
        "lon": 36.8219,
        "hashtags": ["#NairobiWeather", "#KenyaWeather"]
    },
    {
        "name": "Kisumu", 
        "lat": -0.0917,
        "lon": 34.7680,
        "hashtags": ["#KisumuWeather", "#KenyaWeather"]
    },
    {
        "name": "Bratislava",
        "lat": 48.1486,
        "lon": 17.1077,
        "hashtags": ["#BratislavaWeather", "#SlovakiaWeather"]
    }
]
```

### 7. Logging (`logger.py`)
**Purpose**: Centralized logging with multi-city context
- City-specific log messages
- Operation tracking ([1/3], [2/3], [3/3])
- Error categorization
- Performance monitoring

## 🔄 Data Flow

### Multi-City Weather Update Flow
```
1. main.py --mode current
   ↓
2. MultiCityWeatherBot.post_current_weather_all_cities()
   ↓
3. For each city in config.CITIES:
   ├── WeatherService(city).get_current_weather()
   ├── MessageFormatter.format_current_weather()
   ├── TwitterService.post_tweet()
   └── Sleep 5 seconds (rate limiting)
   ↓
4. Return success/failure status
```

### Single-City Operation Flow
```
1. main.py --mode forecast --city Nairobi --hours 6
   ↓
2. MultiCityWeatherBot.post_forecast_city("Nairobi", 6)
   ↓
3. WeatherService("Nairobi").get_weather_forecast(6)
   ↓
4. MessageFormatter.format_forecast()
   ↓
5. TwitterService.post_tweet()
   ↓
6. Return success/failure status
```

## 🕒 Scheduling Architecture

### Production Scheduling (Caprover)
```bash
# Cron job runs every hour
0 * * * * cd /app && python main.py --mode multi-city
```

### Development Scheduling
```python
# schedule library in run_scheduled_tasks()
schedule.every().hour.do(post_current_weather_all_cities)
schedule.every().day.at("07:00").do(post_daily_summary_all_cities)  
schedule.every().day.at("08:00").do(post_forecast_all_cities, hours=6)
schedule.every().day.at("20:00").do(post_forecast_all_cities, hours=6)
schedule.every(30).minutes.do(post_alerts_all_cities)
```

## 🌐 Multi-City Design Principles

### 1. City Configuration Driven
- All cities defined in `config.py`
- No hardcoded city logic
- Easy to add/remove cities
- City-specific settings (coordinates, hashtags)

### 2. Independent City Processing
- Each city processed separately
- Failure in one city doesn't affect others
- Individual error logging and recovery
- City-specific weather services

### 3. Rate Limiting Strategy
- 5-second delays between cities
- Respects Twitter API limits (300 posts/15min)
- OpenWeatherMap free tier friendly (~100-150 calls/day)
- Graceful degradation on rate limits

### 4. Flexible Operation Modes
```python
# All cities
python main.py --mode forecast

# Single city  
python main.py --mode forecast --city Nairobi

# Custom parameters
python main.py --mode forecast --city Kisumu --hours 12
```

### 5. Comprehensive Error Handling
- API failure recovery
- Network error handling
- Rate limit management
- Configuration validation
- Graceful degradation

## 🔧 Extensibility Features

### Adding New Cities
1. Update `config.py` with new city data
2. No code changes required
3. Automatic service creation
4. Immediate availability in all modes

### Adding New Weather Features
1. Extend `WeatherService` with new API calls
2. Add formatting in `MessageFormatter`  
3. Create new methods in `MultiCityWeatherBot`
4. Add CLI option in `main.py`

### Adding New Social Platforms
1. Create new service class (e.g., `mastodon_service.py`)
2. Integrate into `MultiCityWeatherBot`
3. Update message formatting if needed
4. Add configuration options

## 📊 Performance Characteristics

### API Usage (3 Cities)
- **Hourly updates**: 3 weather API calls, 3 Twitter posts
- **Daily forecast**: 3 weather API calls, 3 Twitter posts  
- **Daily summary**: 6 weather API calls, 3 Twitter posts
- **Total daily**: ~100-150 OpenWeather calls, ~75 tweets

### Rate Limiting
- **Twitter**: 300 posts per 15-minute window (sufficient)
- **OpenWeatherMap**: 1,000 calls per day (sufficient)
- **Processing time**: ~20 seconds for all 3 cities (with delays)

### Memory Usage
- **Base footprint**: ~50-100MB
- **Per city overhead**: ~5-10MB
- **Scalable**: Can handle 10+ cities without issues

### Error Recovery
- **Individual city failures**: Continue with remaining cities
- **API failures**: Log error, retry logic where appropriate
- **Rate limiting**: Automatic backoff and retry
- **Network issues**: Timeout handling and recovery

## 🚀 Deployment Architecture

### Container Structure (Docker)
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["tail", "-f", "/dev/null"]  # Allows cron to run
```

### Health Monitoring
- `/health` endpoint - Basic system health
- `/status` endpoint - Detailed component status
- `/logs` endpoint - Recent application logs
- Automatic restart on failures

### CI/CD Pipeline
- GitHub Actions deployment
- Automatic testing before deployment
- Environment variable management
- Caprover integration

## 🛡️ Security Architecture

### API Key Management
- Environment variables only
- No hardcoded secrets
- Caprover secret management
- Regular key rotation capability

### Rate Limiting Protection
- Built-in API rate limiting
- Exponential backoff
- Request queuing
- Circuit breaker patterns

### Error Information
- Sensitive data filtering in logs
- Safe error messages
- No API keys in error outputs
- Secure logging practices

## 🔍 Monitoring & Observability

### Logging Strategy
- Structured logging with context
- Multi-city operation tracking
- Performance metrics
- Error categorization and alerting

### Health Checks
- API connectivity verification
- Twitter authentication status
- Weather data availability
- System resource monitoring

### Metrics Collection
- API response times
- Success/failure rates per city
- Tweet posting statistics
- Error frequency and types

This architecture supports the current 3-city setup while being easily extensible to support additional cities, weather features, and social platforms as needed.
