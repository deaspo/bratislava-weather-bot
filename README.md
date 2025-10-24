# Multi-City Weather Bot 🌤️🇸🇰🇰🇪

Automated Twitter bot that posts every 2 hours weather updates for multiple cities:
- **Bratislava, Slovakia** 🇸🇰
- **Nairobi, Kenya** 🇰🇪  
- **Kisumu, Kenya** 🇰🇪

Uses OpenWeatherMap API with automated deployment via Caprover and staggered hourly updates to avoid rate limiting.

## ✨ Features

### 🌍 Multi-City Support
- **Three Cities**: Bratislava, Nairobi, and Kisumu
- **Staggered Updates**: Posts at different times to avoid rate limits
- **City-Specific Hashtags**: Customized hashtags for each location
- **Timezone Aware**: Proper timezone handling for each city
- **Individual or Batch**: Support for single-city or multi-city operations

### 🌤️ Weather Features
- **Hourly Updates**: Current weather conditions with emojis
- **Forecasts**: 6-24 hour weather predictions  
- **Alerts**: Severe weather warnings and notifications
- **Daily Summaries**: Comprehensive daily weather overview
- **Extreme Conditions**: Automatic alerts for dangerous weather

### 🤖 Bot Features
- **Multiple Modes**: Current, forecast, alerts, daily, multi-city, and test modes
- **Smart Formatting**: Weather-appropriate emojis and clear messaging
- **Error Handling**: Robust error recovery and logging
- **Rate Limiting**: Respects API limits and handles rate limiting
- **Health Monitoring**: Built-in health checks and status endpoints

### 🚀 Deployment Features
- **Containerized**: Docker-based deployment with Caprover
- **CI/CD Pipeline**: Automated deployment via GitHub Actions
- **Health Checks**: Monitoring endpoints for uptime verification
- **Scalable**: Easy horizontal scaling and resource management
- **Persistent Logging**: Comprehensive logging with log rotation

## 📁 Project Structure

```
bratislava-weather-bot/
├── 🐍 Core Application
│   ├── main.py                 # Main CLI with multi-city support
│   ├── multi_city_bot.py       # Multi-city weather bot class
│   ├── weather_service.py      # OpenWeatherMap API integration
│   ├── twitter_service.py      # Twitter API v2 integration  
│   ├── message_formatter.py    # Tweet formatting with emojis
│   ├── config.py              # Multi-city configuration
│   └── logger.py              # Centralized logging
├── 🚢 Deployment
│   ├── Dockerfile             # Container definition
│   ├── docker-entrypoint.sh   # Container startup script
│   ├── captain-definition      # Caprover deployment config
│   ├── healthcheck.py         # Health monitoring endpoints
│   └── caprover-setup.sh      # Automated Caprover setup
├── 🔄 CI/CD
│   └── .github/workflows/
│       └── deploy.yml         # GitHub Actions deployment
├── 🛠️ Utilities
│   ├── deploy.sh              # Local deployment script
│   ├── setup_cron.sh          # Cron job configuration
│   └── status.sh              # System status monitoring
├── 📚 Documentation
│   ├── README.md              # This file
│   ├── USAGE.md               # Detailed usage guide
│   ├── API_SETUP.md           # API keys setup guide
│   ├── DEPLOYMENT.md          # Local deployment guide
│   └── CAPROVER_DEPLOYMENT.md # Caprover deployment guide
└── ⚙️ Configuration
    ├── requirements.txt       # Python dependencies
    ├── .env.example           # Environment template
    └── .gitignore            # Git ignore rules
```

## 🚀 Quick Start

### Option 1: Caprover Deployment (Recommended)

1. **Setup Caprover on your Hetzner VPS** (see [CAPROVER_OFFICIAL_SETUP.md](CAPROVER_OFFICIAL_SETUP.md))
2. **Get API Keys** (see [API_SETUP.md](API_SETUP.md))
3. **Deploy with automated script:**
   ```bash
   ./caprover-setup.sh
   ```
4. **Configure GitHub Secrets** (WEATHER_APP_TOKEN, WEATHER_CAPROVER_SERVER, WEATHER_APP_NAME)
5. **Push to `devel` branch** to trigger deployment

### Option 2: Local/VPS Deployment

1. **Install dependencies:**
   ```bash
   ./deploy.sh
   ```
2. **Configure API keys:**
   ```bash
   cp .env.example .env
   nano .env  # Add your API keys
   ```
3. **Test the bot:**
   ```bash
   python main.py --mode test
   ```

### 📦 Production Configuration

For production deployments (Caprover), the bot automatically skips startup tests to avoid rate limiting. You can control this behavior:

- **Production Mode (recommended)**: Set `SKIP_STARTUP_TEST=true` in Caprover environment variables
- **Development Mode**: Leave `SKIP_STARTUP_TEST` unset or set to `false`

4. **Set up cron job:**
   ```bash
   ./setup_cron.sh
   ```

## 🎯 Bot Operation Modes

The bot supports flexible multi-city and single-city operations with comprehensive weather functionality.

### 🌍 Multi-City Operations (Default)

#### Current Weather
```bash
# All cities (Nairobi → Kisumu → Bratislava)
python main.py                           # Default mode
python main.py --mode multi-city         # Explicit multi-city mode
python main.py --mode current            # Current weather for all cities

# Specific city
python main.py --mode current --city Nairobi
python main.py --mode current --city Kisumu  
python main.py --mode current --city Bratislava
```

#### Weather Forecasts
```bash
# All cities with 6-hour forecast (default)
python main.py --mode forecast

# All cities with custom hours
python main.py --mode forecast --hours 12
python main.py --mode forecast --hours 24

# Specific city with custom forecast
python main.py --mode forecast --city Nairobi --hours 3
python main.py --mode forecast --city Kisumu --hours 6
```

#### Weather Alerts
```bash
# Check alerts for all cities
python main.py --mode alerts

# Check alerts for specific city
python main.py --mode alerts --city Bratislava
python main.py --mode alerts --city Nairobi
```

#### Daily Summaries
```bash
# Daily summary for all cities
python main.py --mode daily

# Daily summary for specific city
python main.py --mode daily --city Kisumu
```

#### Scheduled Tasks
```bash
# Run comprehensive automated scheduling
python main.py --mode schedule
```

**Automated Schedule:**
- **Every hour**: Current weather for all cities
- **Daily 7:00 AM**: Daily summary for all cities  
- **Daily 8:00 AM & 8:00 PM**: 6-hour forecast for all cities
- **Every 30 minutes**: Weather alerts check for all cities

#### Testing & Development
```bash
# Test all cities
python main.py --mode test

# Test specific city
python main.py --mode test --city Nairobi
```

### 🏙️ Available Cities
- **Nairobi, Kenya** 🇰🇪 (-1.2921°, 36.8219°)
- **Kisumu, Kenya** 🇰🇪 (-0.0917°, 34.7680°)  
- **Bratislava, Slovakia** 🇸🇰 (48.1486°, 17.1077°)

## 📱 Example Tweets

### Current Weather Updates
```
🌤️ Weather Update for Nairobi 🇰🇪

🌡️ 24°C (feels like 26°C)
⛅ Partly Cloudy
💧 Humidity: 72%
💨 Wind: 8 km/h NE

⏰ 15:30 30/08/2025

#NairobiWeather #KenyaWeather
```

```
☀️ Weather Update for Bratislava 🇸🇰

🌡️ 22°C (feels like 24°C)
�️ Clear Sky
💧 Humidity: 65%
💨 Wind: 12 km/h SW

⏰ 14:00 30/08/2025

#BratislavaWeather #SlovakiaWeather
```

### Weather Forecast
```
🔮 6-Hour Forecast for Kisumu 🇰🇪

📍 Next 6 hours:
🕒 16:00: 26°C ⛅ Partly Cloudy
🕕 18:00: 25°C 🌧️ Light Rain  
🕘 21:00: 23°C ⛅ Partly Cloudy

💧 Rain expected: 18:00-20:00
🌡️ Temp range: 23-26°C

#KisumuWeather #KenyaWeather
```

### Weather Alert
```
⚠️ WEATHER ALERT for Bratislava 🇸🇰

📢 Thunderstorm Warning
🏢 Source: Slovak Hydrometeorological Institute
⏰ From: 15:00 30/08/2025
⏰ Until: 22:00 30/08/2025

📝 Severe thunderstorms with heavy rain expected. 
Potential flooding in low-lying areas.

Stay indoors and avoid travel if possible.

#BratislavaWeather #WeatherAlert
```

### Daily Summary
```
🌅 Daily Weather Summary for Nairobi 🇰🇪

📅 30/08/2025

🌡️ Current: 24°C ⛅ Partly Cloudy
🌡️ Today: 21°C → 27°C
💧 Humidity: 72%
💨 Wind: 8 km/h NE

🔮 Tonight: 19°C 🌙 Clear
🔮 Tomorrow: 28°C ☀️ Sunny

Perfect weather for outdoor activities! ☀️

#NairobiWeather #KenyaWeather #WeatherSummary
```

## 🔧 API Keys Setup

### Required APIs:
- **Twitter API v2** - For posting tweets
- **OpenWeatherMap API** - For weather data

See [API_SETUP.md](API_SETUP.md) for detailed setup instructions.

## 📊 Monitoring

### Health Check Endpoints (Caprover deployment):
- `/health` - Basic health status
- `/status` - Detailed component status  
- `/logs` - Recent log entries

### Manual Monitoring:
```bash
# Check bot status
./status.sh

# View recent logs
tail -f logs/cron.log

# Test connectivity
python main.py --mode test
```

## 🔄 Deployment Options

### 1. Caprover (Recommended)
- ✅ Automated deployments via GitHub Actions
- ✅ Docker containerization
- ✅ Built-in SSL and domain management
- ✅ Health monitoring and scaling
- ✅ Web-based management dashboard

### 2. Traditional VPS
- ✅ Direct deployment on server
- ✅ Cron-based scheduling
- ✅ Simple setup and maintenance
- ✅ Full system access

## 🛠️ Development

### Local Development
```bash
# Clone and setup
git clone <repo-url>
cd bratislava-weather-bot
./deploy.sh

# Create feature branch
git checkout -b feature-name

# Test your changes
python main.py --mode test

# Commit and push
git add .
git commit -m "Add new feature"
git push origin feature-name
```

### Production Deployment
```bash
# Merge to devel branch
git checkout devel
git merge feature-name
git push origin devel  # Triggers automatic deployment
```

## 📚 Documentation

- **[API_SETUP.md](API_SETUP.md)** - Twitter and OpenWeatherMap API setup
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Local/VPS deployment guide
- **[CAPROVER_OFFICIAL_SETUP.md](CAPROVER_OFFICIAL_SETUP.md)** - Official Caprover deployment method
- **[CAPROVER_DEPLOYMENT.md](CAPROVER_DEPLOYMENT.md)** - Alternative Caprover setup guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Open a Pull Request

## 📄 License

This project is open source. Feel free to use and modify for your own weather bot projects.

## 🌟 Features Roadmap

- [x] **Multi-city support** - Support for Nairobi, Kisumu, and Bratislava
- [x] **Flexible operation modes** - Current, forecast, alerts, daily, and scheduled tasks
- [x] **City-specific operations** - Target individual cities or all cities
- [x] **Comprehensive scheduling** - Automated hourly, daily, and alert scheduling
- [ ] Weather trends and historical data analysis
- [ ] Integration with more social platforms (Mastodon, Bluesky)
- [ ] Advanced weather visualizations and charts
- [ ] Weather-based recommendations and tips
- [ ] Multilingual support (English, Slovak, Swahili)
- [ ] Weather photography integration
- [ ] Air quality monitoring
- [ ] Climate change tracking

---

**Twitter**: [@kidiwalogha](https://twitter.com/kidiwalogha) (or your chosen handle)  
**Weather Data**: Powered by [OpenWeatherMap](https://openweathermap.org/)  
**Deployment**: [Caprover](https://caprover.com/) + [GitHub Actions](https://github.com/features/actions)
