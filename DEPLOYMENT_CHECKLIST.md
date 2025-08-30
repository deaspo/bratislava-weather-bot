# 🚀 Bratislava Weather Bot - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 📋 Repository Setup
- [x] Git repository initialized with `devel` branch
- [x] All files committed and ready for deployment
- [x] GitHub Actions workflow configured
- [x] Dockerfile and Caprover configuration ready

### 🔑 API Keys Required
- [ ] **Twitter Developer Account** created
- [ ] **Twitter API v2 keys** obtained:
  - [ ] API Key (Consumer Key)
  - [ ] API Secret (Consumer Secret) 
  - [ ] Access Token
  - [ ] Access Token Secret
  - [ ] Bearer Token
- [ ] **OpenWeatherMap API key** obtained
- [ ] **Twitter bot account** created (@BratislavaSK or similar)

### 🚢 Caprover Server Setup
- [ ] **Hetzner VPS** provisioned and accessible
- [ ] **Docker** installed on VPS
- [ ] **Caprover** installed and configured
- [ ] **Domain** configured (e.g., yourdomain.com)
- [ ] **SSL certificates** working
- [ ] **Caprover CLI** installed locally (`npm install -g caprover`)

## 🎯 Deployment Steps

### Step 1: Push to GitHub
```bash
# Push your code to GitHub (if not already done)
git remote add origin https://github.com/yourusername/bratislava-weather-bot.git
git push -u origin devel
```

### Step 2: Configure GitHub Secrets
In your GitHub repository (`Settings > Secrets and variables > Actions`):
- [ ] `WEATHER_CAPROVER_SERVER` = https://captain.yourdomain.com
- [ ] `WEATHER_APP_NAME` = bratislava-weather-bot
- [ ] `WEATHER_APP_TOKEN` = your-caprover-app-token

### Step 3: Deploy with Caprover
Option A - Automated Script:
```bash
./caprover-setup.sh
```

Option B - Manual:
```bash
# Login to Caprover
caprover login --caproverUrl https://captain.yourdomain.com --caproverPassword yourpassword

# Create app
caprover app --caproverApp bratislava-weather-bot --action create

# Deploy
caprover deploy --caproverApp bratislava-weather-bot
```

### Step 4: Configure Environment Variables
In Caprover dashboard, add these environment variables:
- [ ] `TWITTER_API_KEY`
- [ ] `TWITTER_API_SECRET` 
- [ ] `TWITTER_ACCESS_TOKEN`
- [ ] `TWITTER_ACCESS_TOKEN_SECRET`
- [ ] `TWITTER_BEARER_TOKEN`
- [ ] `OPENWEATHER_API_KEY`
- [ ] `CITY_NAME=Bratislava`
- [ ] `COUNTRY_CODE=SK`
- [ ] `LATITUDE=48.1482`
- [ ] `LONGITUDE=17.1067`
- [ ] `TIMEZONE=Europe/Bratislava`
- [ ] `LOG_LEVEL=INFO`

## 🧪 Testing & Verification

### Health Checks
- [ ] App deployed successfully in Caprover
- [ ] Health endpoint responding: `https://your-app.yourdomain.com/health`
- [ ] Status endpoint working: `https://your-app.yourdomain.com/status`
- [ ] Logs accessible: `https://your-app.yourdomain.com/logs`

### Bot Functionality
- [ ] **Test Mode**: Bot passes all connectivity tests
- [ ] **Current Weather**: Successfully posts weather update
- [ ] **Forecast**: Successfully posts forecast  
- [ ] **Alerts**: Checks for weather alerts
- [ ] **Cron Jobs**: Scheduled posts working hourly

### Twitter Integration
- [ ] **Bot Account**: Profile set up with weather theme
- [ ] **Permissions**: Read and Write access configured
- [ ] **First Tweet**: Manual test post successful
- [ ] **Automatic Posts**: Hourly posts working

## 🔄 Automated Deployment

### GitHub Actions
- [ ] **Workflow file** present in `.github/workflows/deploy.yml`
- [ ] **Secrets** configured in GitHub repository
- [ ] **Test deployment** by pushing to `devel` branch
- [ ] **Actions tab** shows successful deployment

### Continuous Deployment
```bash
# Make changes and deploy
git add .
git commit -m "Update bot features"  
git push origin devel  # Triggers automatic deployment
```

## 📊 Monitoring Setup

### Health Monitoring
- [ ] **Caprover Dashboard**: Monitor resource usage
- [ ] **Health Endpoints**: Set up external monitoring (optional)
- [ ] **Log Monitoring**: Regular log review process

### Bot Monitoring  
- [ ] **Twitter Activity**: Verify regular posting
- [ ] **Error Handling**: Check logs for errors
- [ ] **API Limits**: Monitor API usage

## 🎉 Go Live Checklist

### Final Verification
- [ ] **24 Hour Test**: Bot runs successfully for 24 hours
- [ ] **All Post Types**: Current, forecast, alerts, daily all working
- [ ] **Error Recovery**: Bot handles API failures gracefully
- [ ] **Resource Usage**: Memory and CPU within limits

### Production Readiness
- [ ] **Backup Strategy**: Regular backups configured
- [ ] **Update Process**: Deployment pipeline tested
- [ ] **Rollback Plan**: Know how to rollback if needed
- [ ] **Support Documentation**: Team knows how to maintain

### Announcement
- [ ] **Bot Profile**: Complete with description and branding
- [ ] **First Official Tweet**: Welcome message posted
- [ ] **Social Media**: Announce the new weather bot
- [ ] **Documentation**: All guides up to date

## 🆘 Troubleshooting Quick Reference

### Common Issues & Solutions

**Deployment Fails:**
- Check GitHub Actions logs
- Verify Caprover credentials in secrets
- Ensure app exists in Caprover dashboard

**Bot Won't Post:**  
- Check environment variables in Caprover
- Verify API keys are valid
- Review application logs

**Health Check Fails:**
- Check container is running in Caprover
- Verify port 4200 is accessible
- Test health endpoint manually

**Cron Jobs Not Working:**
- Check cron service in container logs
- Verify timezone configuration
- Test manual execution

### Support Contacts
- **Caprover Documentation**: https://caprover.com/docs/
- **Twitter API Support**: https://developer.twitter.com/
- **OpenWeatherMap Support**: https://openweathermap.org/api

---

## 🎊 Success! 

Your Bratislava Weather Bot is now live and automatically posting hourly weather updates!

**Bot URL**: https://bratislava-weather-bot.yourdomain.com  
**Health Check**: https://bratislava-weather-bot.yourdomain.com/health  
**Twitter**: @BratislavaSK (or your chosen handle)

The bot will:
- ⏰ Post hourly weather updates
- 🌅 Post daily summaries at 7 AM
- 📊 Post forecasts at 8 AM and 8 PM  
- ⚠️ Alert on severe weather conditions

**Automatic Updates**: Push to `devel` branch → GitHub Actions → Deployed to Caprover! 🚀
