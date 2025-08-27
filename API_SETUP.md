# API Setup Guide

This guide explains how to obtain the necessary API keys for the Bratislava Weather Bot.

## 1. Twitter API Setup (X API)

### Step 1: Create Twitter Developer Account
1. Go to https://developer.twitter.com/
2. Sign in with your Twitter account (or create one)
3. Apply for a developer account
4. Fill out the application form explaining you're creating a weather bot

### Step 2: Create a New Project/App
1. Once approved, go to the Developer Portal
2. Click "Create Project" or "Create App"
3. Name your project "Bratislava Weather Bot"
4. Select "Making a bot" as the use case
5. Describe your app: "Automated weather updates for Bratislava, Slovakia"

### Step 3: Generate Keys and Tokens
1. Go to your app settings
2. Generate the following:
   - **API Key** (Consumer Key)
   - **API Secret Key** (Consumer Secret)
   - **Bearer Token**
   - **Access Token**
   - **Access Token Secret**

### Step 4: Set App Permissions
1. In your app settings, go to "Settings" > "User authentication settings"
2. Set permissions to "Read and Write"
3. Set Type to "Bot or Automated App"
4. Add your website URL (can be a placeholder like https://example.com)

### Important Notes:
- Keep all keys and tokens secure
- Never share them publicly or commit them to version control
- The bot will need "Read and Write" permissions to post tweets

## 2. OpenWeatherMap API Setup

### Step 1: Create Account
1. Go to https://openweathermap.org/
2. Click "Sign In" then "Create an Account"
3. Fill out the registration form
4. Verify your email address

### Step 2: Get API Key
1. After logging in, go to https://home.openweathermap.org/api_keys
2. Your default API key will be shown
3. You can create additional keys if needed
4. Copy the API key

### Step 3: Choose Plan
- **Free Plan**: 1,000 calls/day, 60 calls/minute (sufficient for our bot)
- **Paid Plans**: Available if you need more calls

### API Endpoints Used:
- Current Weather API
- One Call API 3.0 (for forecasts and alerts)
- Both are included in the free plan

## 3. Setting Up Environment Variables

Create a `.env` file in your project directory with the following content:

```bash
# Twitter API Credentials
TWITTER_API_KEY=your_api_key_here
TWITTER_API_SECRET=your_api_secret_here
TWITTER_ACCESS_TOKEN=your_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
TWITTER_BEARER_TOKEN=your_bearer_token_here

# OpenWeatherMap API
OPENWEATHER_API_KEY=your_openweathermap_api_key_here

# Location Settings (Bratislava coordinates)
CITY_NAME=Bratislava
COUNTRY_CODE=SK
LATITUDE=48.1482
LONGITUDE=17.1067

# Bot Settings
TIMEZONE=Europe/Bratislava
LOG_LEVEL=INFO
```

## 4. Testing Your Setup

After setting up the API keys, test your configuration:

```bash
# Test the bot
python main.py --mode test

# Test individual components
python main.py --mode current    # Post current weather
python main.py --mode forecast   # Post forecast
python main.py --mode alerts     # Check for alerts
```

## Troubleshooting

### Twitter API Issues:
- **403 Forbidden**: Check app permissions, ensure Read+Write access
- **401 Unauthorized**: Verify all tokens and keys are correct
- **429 Rate Limited**: You're making too many requests, wait and try again

### OpenWeatherMap Issues:
- **401 Unauthorized**: Check API key is correct and active
- **403 Forbidden**: API key might not have access to required endpoints
- **429 Rate Limited**: Free plan limits exceeded

### General Issues:
- Check `.env` file exists and has correct format
- Ensure no spaces around the `=` in environment variables
- Verify internet connection
- Check logs in `logs/` directory for detailed error messages

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for all secrets**
3. **Regularly rotate API keys**
4. **Monitor API usage to detect unusual activity**
5. **Use the principle of least privilege for API permissions**
