# Caprover Deployment Guide

This guide explains how to deploy the Bratislava Weather Bot using Caprover with automated GitHub Actions.

## 🚢 Caprover Overview

Caprover is a self-hosted PaaS (Platform as a Service) that makes it easy to deploy applications on your VPS. It provides:
- Docker-based deployments
- Automatic SSL certificates
- Load balancing
- Easy domain management
- Web-based dashboard

## 📋 Prerequisites

### 1. Caprover Server Setup
First, you need to set up Caprover on your Hetzner VPS:

```bash
# SSH into your Hetzner VPS
ssh root@your-server-ip

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Caprover
docker run -p 80:80 -p 443:443 -p 3000:3000 -d \
    --name captain-captain \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /captain:/captain \
    caprover/caprover

# Wait a few seconds and then setup
docker logs captain-captain --follow
```

### 2. Initial Caprover Configuration
1. Go to `http://your-server-ip:3000`
2. Use password `captain42` (default)
3. Change the password
4. Set up your domain (e.g., `yourdomain.com`)
5. Configure SSL certificates

### 3. Install Caprover CLI
On your local machine:
```bash
npm install -g caprover
```

## 🚀 Deployment Setup

### Method 1: Automated Setup Script

Run the automated setup script:

```bash
./caprover-setup.sh
```

This script will:
- Login to your Caprover instance
- Create the app if it doesn't exist
- Guide you through setting environment variables
- Deploy the application

### Method 2: Manual Setup

#### Step 1: Create App in Caprover
```bash
caprover login --caproverUrl https://captain.yourdomain.com --caproverPassword yourpassword
caprover app --caproverApp bratislava-weather-bot --action create
```

#### Step 2: Configure Environment Variables
In the Caprover dashboard, go to your app and set these environment variables:

```
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
OPENWEATHER_API_KEY=your_openweather_api_key
CITY_NAME=Bratislava
COUNTRY_CODE=SK
LATITUDE=48.1482
LONGITUDE=17.1067
TIMEZONE=Europe/Bratislava
LOG_LEVEL=INFO
```

#### Step 3: Deploy
```bash
caprover deploy --caproverApp bratislava-weather-bot
```

## 🔄 GitHub Actions Automated Deployment

### GitHub Repository Secrets

In your GitHub repository, add these secrets (`Settings > Secrets and variables > Actions`):

```
CAPROVER_URL=https://captain.yourdomain.com
CAPROVER_PASSWORD=your_caprover_password
CAPROVER_APP_NAME=bratislava-weather-bot
```

### Deployment Workflow

The GitHub Actions workflow (`.github/workflows/deploy.yml`) will:

1. **On Push to `devel` branch:**
   - Run tests and code validation
   - Deploy to Caprover automatically

2. **On Pull Request:**
   - Run tests only (no deployment)

### Triggering Deployment

```bash
# Make changes to your code
git add .
git commit -m "Update weather bot features"
git push origin devel
```

The deployment will start automatically and you can monitor it in the GitHub Actions tab.

## 📊 Monitoring & Health Checks

### Health Check Endpoints

The bot includes a health check server accessible at:

- `https://your-app.yourdomain.com/health` - Basic health status
- `https://your-app.yourdomain.com/status` - Detailed component status
- `https://your-app.yourdomain.com/logs` - Recent log entries

### Caprover Monitoring

In the Caprover dashboard you can:
- View real-time logs
- Monitor resource usage
- Check deployment history
- Configure scaling settings

### Manual Monitoring

SSH into your server and check:

```bash
# Check container status
docker ps | grep bratislava-weather-bot

# View logs
docker logs bratislava-weather-bot-captain --follow

# Check health endpoint
curl https://your-app.yourdomain.com/health
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Deployment Fails
- Check GitHub Actions logs
- Verify Caprover credentials in GitHub secrets
- Ensure app exists in Caprover

#### 2. App Won't Start
- Check environment variables are set correctly
- Review container logs in Caprover dashboard
- Verify API keys are valid

#### 3. Health Check Fails
- Check if port 4200 is accessible
- Verify health check endpoint responds
- Review application logs

#### 4. Cron Jobs Not Running
- Check if cron service is running in container
- Verify timezone settings
- Review cron logs at `/app/logs/cron.log`

### Debug Commands

```bash
# Connect to running container
docker exec -it bratislava-weather-bot-captain bash

# Check cron jobs
docker exec bratislava-weather-bot-captain crontab -l

# Test bot manually
docker exec bratislava-weather-bot-captain python main.py --mode test

# View recent logs
docker exec bratislava-weather-bot-captain tail -f logs/cron.log
```

## 🔄 Updates and Maintenance

### Automatic Updates
- Push to `devel` branch triggers automatic deployment
- No downtime during updates
- Rollback available in Caprover dashboard

### Manual Updates
```bash
# Deploy specific version
git checkout specific-commit
caprover deploy --caproverApp bratislava-weather-bot

# Rollback in Caprover UI if needed
```

### Backup and Recovery
```bash
# Backup app data (if using persistent storage)
docker exec bratislava-weather-bot-captain tar -czf /backup.tar.gz /app/logs

# Copy backup to local machine
docker cp bratislava-weather-bot-captain:/backup.tar.gz ./backup-$(date +%Y%m%d).tar.gz
```

## 🌐 Custom Domain Setup

### Configure Domain in Caprover
1. Go to app settings in Caprover dashboard
2. Enable "Has Default SubDomain SSL"
3. Add custom domain (e.g., `weather.yourdomain.com`)
4. Configure DNS A record pointing to your server IP

### SSL Certificate
Caprover automatically provides SSL certificates via Let's Encrypt.

## 📈 Scaling

### Horizontal Scaling
In Caprover dashboard:
1. Go to app settings
2. Increase "Instance Count"
3. Configure load balancer if needed

### Resource Limits
Set memory and CPU limits in the Caprover app configuration:
```json
{
  "memLimit": "256m",
  "cpuLimit": "0.5"
}
```

## 🎉 Production Checklist

Before going live:

- [ ] ✅ Caprover server properly configured
- [ ] ✅ Domain and SSL certificate working
- [ ] ✅ Environment variables set correctly
- [ ] ✅ GitHub Actions deployment working
- [ ] ✅ Health checks responding
- [ ] ✅ Cron jobs running
- [ ] ✅ Twitter API permissions configured
- [ ] ✅ Bot successfully posting tweets
- [ ] ✅ Monitoring and alerting set up
- [ ] ✅ Backup strategy in place

Your Bratislava Weather Bot is now ready for production with automated deployment! 🎊
