# Bratislava Weather Bot 🌤️🇸🇰

Automated Twitter bot that posts hourly weather updates for Bratislava, Slovakia using OpenWeatherMap API with automated deployment via Caprover.

## ✨ Features

### 🌤️ Weather Features
- **Hourly Updates**: Current weather conditions with emojis
- **Forecasts**: 6-24 hour weather predictions  
- **Alerts**: Severe weather warnings and notifications
- **Daily Summaries**: Comprehensive daily weather overview
- **Extreme Conditions**: Automatic alerts for dangerous weather

### 🤖 Bot Features
- **Multiple Modes**: Current, forecast, alerts, daily, and test modes
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
│   ├── main.py                 # Main bot script with CLI interface
│   ├── weather_service.py      # OpenWeatherMap API integration
│   ├── twitter_service.py      # Twitter API v2 integration  
│   ├── message_formatter.py    # Tweet formatting with emojis
│   ├── config.py              # Configuration management
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
4. **Configure GitHub Secrets** (APP_TOKEN, CAPROVER_SERVER, APP_NAME)
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
4. **Set up cron job:**
   ```bash
   ./setup_cron.sh
   ```

## 🎯 Bot Operation Modes

```bash
# Post current weather (default for cron)
python main.py --mode current

# Post weather forecast
python main.py --mode forecast --hours 6

# Check and post weather alerts  
python main.py --mode alerts

# Post daily summary
python main.py --mode daily

# Run continuous scheduling (for development)
python main.py --mode schedule

# Test all functionality
python main.py --mode test
```

## 📱 Example Tweets

### Current Weather
```
☀️ Weather Update for Bratislava 🇸🇰

🌡️ 22°C (feels like 24°C)
🌡️ Clear Sky
💧 Humidity: 65%
💨 Wind: 12 km/h

⏰ 14:00 27/08/2025
```

### Weather Alert
```
⚠️ WEATHER ALERT for Bratislava 🇸🇰

📢 Thunderstorm Warning
🏢 Source: Meteorological Service
⏰ From: 15:00 27/08
⏰ Until: 20:00 27/08

📝 Heavy thunderstorms expected...
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

- [ ] Multiple city support
- [ ] Weather trends and historical data
- [ ] Integration with more social platforms
- [ ] Advanced weather visualizations
- [ ] Weather-based recommendations
- [ ] Multilingual support (Slovak/English)

---

**Twitter**: [@BratislavaSK](https://twitter.com/BratislavaSK) (or your chosen handle)  
**Weather Data**: Powered by [OpenWeatherMap](https://openweathermap.org/)  
**Deployment**: [Caprover](https://caprover.com/) + [GitHub Actions](https://github.com/features/actions)
