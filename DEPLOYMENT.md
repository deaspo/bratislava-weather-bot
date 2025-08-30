# Multi-City Weather Bot - Complete Deployment Guide

This guide walks you through deploying the Multi-City Weather Bot supporting Bratislava (Slovakia), Nairobi and Kisumu (Kenya) on your VPS.

## 🚀 Quick Start

### Prerequisites
- VPS running Ubuntu/Debian (tested on Hetzner)
- SSH access to your server
- Twitter Developer Account
- OpenWeatherMap API Account

### 1. Clone/Upload the Project
```bash
# Upload the project to your VPS or use git
cd /home/your_username/
# If using git:
git clone <your-repo-url> bratislava-weather-bot
cd bratislava-weather-bot
```

### 2. Run Automated Setup
```bash
./deploy.sh
```

This script will:
- Update system packages
- Install Python and dependencies  
- Create virtual environment
- Install Python packages
- Create .env template
- Set up project structure

### 3. Configure API Keys
```bash
# Edit the environment file
nano .env

# Add your API keys (see API_SETUP.md for details)
```

### 4. Test the Multi-City Bot
```bash
# Activate virtual environment
source venv/bin/activate

# Test all cities
python main.py --mode test

# Test individual cities
python main.py --mode test --city Nairobi
python main.py --mode test --city Kisumu
python main.py --mode test --city Bratislava

# Test different modes (careful - these post to Twitter)
python main.py --mode current --city Nairobi
python main.py --mode forecast --hours 3
python main.py --mode current
python main.py --mode forecast --hours 6
```

### 5. Set Up Automated Posting
```bash
# Set up hourly cron job
./setup_cron.sh
```

### 6. Monitor the Bot
```bash
# Check bot status
./status.sh

# Monitor live logs
tail -f logs/cron.log
```

## 📋 Manual Setup (Alternative)

If you prefer manual setup:

### 1. System Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install requirements
sudo apt install -y python3 python3-pip python3-venv cron

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit with your API keys
nano .env
```

### 3. Cron Setup
```bash
# Open crontab
crontab -e

# Add this line for multi-city hourly updates:
0 * * * * cd /path/to/bratislava-weather-bot && /path/to/bratislava-weather-bot/venv/bin/python main.py --mode multi-city >> logs/cron.log 2>&1

# Alternative: Use current mode (same result)
0 * * * * cd /path/to/bratislava-weather-bot && /path/to/bratislava-weather-bot/venv/bin/python main.py --mode current >> logs/cron.log 2>&1

# Optional: Add daily summary at 7 AM
0 7 * * * cd /path/to/bratislava-weather-bot && /path/to/bratislava-weather-bot/venv/bin/python main.py --mode daily >> logs/cron.log 2>&1

# Optional: Add forecasts twice daily (8 AM and 8 PM)
0 8,20 * * * cd /path/to/bratislava-weather-bot && /path/to/bratislava-weather-bot/venv/bin/python main.py --mode forecast --hours 6 >> logs/cron.log 2>&1
```

## 🎯 Multi-City Bot Operation Modes

The bot supports flexible multi-city and single-city operations:

### Multi-City Commands (Default)
```bash
# Post current weather for all cities (Nairobi → Kisumu → Bratislava)
python main.py                           # Default mode
python main.py --mode current            # Explicit current mode
python main.py --mode multi-city         # Explicit multi-city mode

# Multi-city forecasts
python main.py --mode forecast           # 6-hour forecast for all cities
python main.py --mode forecast --hours 12 # 12-hour forecast for all cities

# Multi-city daily summaries and alerts
python main.py --mode daily              # Daily summary for all cities  
python main.py --mode alerts             # Check alerts for all cities
```

### Single-City Commands
```bash
# Target specific cities
python main.py --mode current --city Nairobi
python main.py --mode current --city Kisumu
python main.py --mode current --city Bratislava

# City-specific forecasts
python main.py --mode forecast --city Nairobi --hours 6
python main.py --mode forecast --city Kisumu --hours 3
python main.py --mode forecast --city Bratislava --hours 12

# City-specific daily summaries
python main.py --mode daily --city Nairobi
python main.py --mode daily --city Kisumu
python main.py --mode daily

# Run continuous scheduling (for development)
python main.py --mode schedule

# Test all functionality
python main.py --mode test
```

## 📊 Monitoring & Maintenance

### Check Bot Status
```bash
./status.sh
```

### View Logs
```bash
# Cron logs
tail -f logs/cron.log

# Application logs
tail -f logs/weather_bot_$(date +%Y%m%d).log

# All recent logs
ls -la logs/
```

### Monitor Cron Jobs
```bash
# List active cron jobs
crontab -l

# Check cron service status
sudo systemctl status cron

# View system cron logs
sudo journalctl -u cron
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Bot Not Posting
- Check API keys in `.env` file
- Verify internet connection
- Check cron job is active: `crontab -l`
- Review logs for errors: `tail logs/cron.log`

#### 2. Permission Errors
```bash
# Fix script permissions
chmod +x *.sh

# Fix Python file permissions
chmod +x main.py
```

#### 3. Python Path Issues
```bash
# Verify Python path in cron job
which python3
# Update cron job with correct paths
```

#### 4. API Rate Limits
- OpenWeatherMap free tier: 1,000 calls/day, 60/minute
- Twitter free tier: Various limits depending on endpoints
- Check logs for rate limit errors

#### 5. Timezone Issues
```bash
# Check system timezone
timedatectl

# Set correct timezone
sudo timedatectl set-timezone Europe/Bratislava
```

### Log Analysis
```bash
# Check for errors in logs
grep -i error logs/*.log

# Check successful posts
grep -i "successfully posted" logs/*.log

# Monitor API calls
grep -i "fetched" logs/*.log
```

## 🔄 Updates & Maintenance

### Updating the Bot
```bash
# Stop cron job temporarily
crontab -r

# Update code (if using git)
git pull origin main

# Reinstall dependencies if needed
source venv/bin/activate
pip install -r requirements.txt

# Test updated bot
python main.py --mode test

# Restore cron job
./setup_cron.sh
```

### Backup Important Data
```bash
# Backup configuration and logs
tar -czf backup_$(date +%Y%m%d).tar.gz .env logs/

# Store backup securely
scp backup_*.tar.gz user@backup-server:/backups/
```

## 📈 Scaling & Optimization

### For Higher Frequency Updates
If you want more frequent updates, consider:

1. **Increase Update Frequency**:
   ```bash
   # Every 30 minutes instead of hourly
   */30 * * * * cd /path/to/bot && python main.py --mode current
   ```

2. **Upgrade OpenWeatherMap Plan**: For more API calls

3. **Add Error Recovery**: Implement retry logic for failed posts

### Performance Monitoring
```bash
# Monitor resource usage
htop

# Check disk space (logs can grow)
df -h

# Clean old logs periodically (add to cron)
find logs/ -name "*.log" -mtime +30 -delete
```

## 🌐 Twitter Account Setup

### Account Settings for @BratislavaSK
1. **Profile Setup**:
   - Name: "Bratislava Weather"
   - Username: @BratislavaSK (or similar available)
   - Bio: "🌤️ Automated weather updates for Bratislava, Slovakia 🇸🇰 • Powered by OpenWeatherMap"
   - Location: "Bratislava, Slovakia"
   - Website: Link to your VPS or GitHub repo

2. **Profile Picture**: Weather-related icon or Bratislava landmark

3. **Banner**: Sky/weather themed or city skyline

## 🎉 Go Live!

Once everything is tested and working:

1. **Final Test**: `python main.py --mode test`
2. **Enable Cron**: `./setup_cron.sh`
3. **Monitor First Posts**: `tail -f logs/cron.log`
4. **Announce**: Tweet about your new weather bot!

Your Bratislava Weather Bot is now live and will automatically post hourly weather updates! 🎉

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review logs in `logs/` directory  
3. Test individual components with `--mode test`
4. Verify API keys and permissions

The bot is designed to be robust and handle most errors gracefully while logging detailed information for debugging.
