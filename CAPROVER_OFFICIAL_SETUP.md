# 🚢 Official Caprover Deployment Setup Guide

This guide uses the official Caprover deployment method from their documentation.

## 📋 Prerequisites

1. **Hetzner VPS** with Caprover installed
2. **GitHub repository** with your bot code
3. **API keys** configured (Twitter + OpenWeatherMap)

## 🚀 Step-by-Step Setup

### Step 1: Create Caprover App

#### Option A: Use Setup Script (Recommended)
```bash
./caprover-setup.sh
```

#### Option B: Manual Setup
1. Login to your Caprover dashboard
2. Create a new app (e.g., `bratislava-weather-bot`)
3. Note the app name - this will be your `APP_NAME`

### Step 2: Enable App Token

1. Go to **Apps > [your-app] > Deployment** tab
2. Click **"Enable App Token"**
3. **Copy the generated token** - this is your `APP_TOKEN`
4. Keep this token secure!

### Step 3: Add Private Docker Registry (Required for GitHub Actions)

Since we're using GitHub Container Registry (ghcr.io):

1. Go to **Cluster > Docker Registries**
2. Click **"Add New Docker Registry"**
3. Fill in:
   - **Username**: `your-github-username`
   - **Password**: `your-github-personal-access-token` (see below)
   - **Domain**: `ghcr.io`
   - **Image Prefix**: `your-github-username` (must be lowercase)

#### Create GitHub Personal Access Token:
1. Go to GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate new token with these scopes:
   - `write:packages`
   - `read:packages`
3. Copy the token and use it as the registry password

### Step 4: Configure GitHub Repository Secrets

Add these secrets in **GitHub > Settings > Secrets and variables > Actions**:

```
CAPROVER_SERVER = https://captain.yourdomain.com
APP_NAME = bratislava-weather-bot
APP_TOKEN = <token-from-caprover-dashboard>
```

### Step 5: Set Environment Variables in Caprover

Go to **Apps > [your-app] > App Configs** and add:

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

### Step 6: Deploy!

Push to your `devel` branch:

```bash
git add .
git commit -m "Setup Caprover deployment"
git push origin devel
```

## 🔄 How the Deployment Works

### GitHub Actions Workflow:

1. **Test Phase**:
   - Validates Python code
   - Runs linting and syntax checks
   - Validates configuration

2. **Build & Deploy Phase** (only on push to `devel`):
   - Builds Docker image using your Dockerfile
   - Pushes image to GitHub Container Registry (`ghcr.io`)
   - Deploys image to Caprover using the official action

### Deployment Flow:
```
Push to `devel` → GitHub Actions → Build Docker Image → 
Push to ghcr.io → Deploy to Caprover → App Running!
```

## 📊 Monitoring Your Deployment

### GitHub Actions:
- Go to **Actions** tab in your GitHub repo
- Monitor build and deployment progress
- Check logs if deployment fails

### Caprover Dashboard:
- **Apps > [your-app] > App Logs**: View application logs
- **Apps > [your-app] > HTTP Settings**: Configure domain
- **Apps > [your-app] > App Configs**: Manage environment variables

### Health Endpoints:
- `https://your-app.yourdomain.com/health` - Basic health check
- `https://your-app.yourdomain.com/status` - Detailed status
- `https://your-app.yourdomain.com/logs` - Recent logs

## 🛠️ Advantages of This Method

### ✅ Benefits:
- **Official Caprover method** - Well supported and documented
- **Efficient builds** - Docker images built on GitHub (doesn't consume VPS resources)
- **Container registry** - Images stored in GitHub Container Registry
- **Automatic deployments** - Push to trigger deployment
- **Rollback capability** - Easy to rollback in Caprover dashboard
- **Scalable** - Can easily scale container instances

### 🔄 Deployment Process:
- **Zero downtime** deployments
- **Health checks** ensure app is running before switching traffic
- **Resource efficiency** - Build happens on GitHub infrastructure
- **Version control** - Each deployment tagged with commit SHA

## 🚨 Troubleshooting

### Common Issues:

#### 1. Docker Registry Authentication Failed
- Verify GitHub Personal Access Token has `write:packages` permission
- Ensure registry username matches GitHub username (lowercase)
- Check token is not expired

#### 2. App Token Invalid
- Regenerate app token in Caprover dashboard
- Update GitHub secrets with new token
- Ensure no extra spaces in secret values

#### 3. Build Fails
- Check GitHub Actions logs for specific error
- Verify Dockerfile syntax
- Ensure all required files are committed

#### 4. Health Check Fails
- Check app logs in Caprover dashboard
- Verify environment variables are set correctly
- Test health endpoint manually

### Debug Commands:

```bash
# Check Docker image locally
docker pull ghcr.io/yourusername/bratislava-weather-bot:latest

# Test health endpoint
curl https://your-app.yourdomain.com/health

# Check app logs
# (Use Caprover dashboard > Apps > your-app > App Logs)
```

## 🎉 Success!

Once everything is configured:

1. **Push to `devel`** triggers automatic deployment
2. **Monitor in GitHub Actions** for build progress
3. **Check Caprover dashboard** for deployment status
4. **Verify health endpoints** are responding
5. **Bot starts posting** hourly weather updates!

Your Bratislava Weather Bot is now deployed with enterprise-grade CI/CD! 🚀🌤️

## 📞 Support

- **Caprover Docs**: https://caprover.com/docs/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Caprover Slack**: https://join.slack.com/t/caprover/shared_invite/zt-2qlb28drp-RpxNfY3nUhroLuRJUUJzDA
