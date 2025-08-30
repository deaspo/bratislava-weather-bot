# Multi-City Weather Bot API Setup Guide

This guide explains how to obtain the necessary API keys for the Multi-City Weather Bot supporting Bratislava (Slovakia), Nairobi and Kisumu (Kenya).

## 1. Twitter API Setup (X API)

### Step 1: Create Twitter Developer Account
1. Go to https://developer.twitter.com/
2. Sign in with your Twitter account (or create one)
3. Apply for a developer account
4. Fill out the application form explaining you're creating a multi-city weather bot

### Step 2: Create a New Project/App
1. Once approved, go to the Developer Portal
2. Click "Create Project" or "Create App"
3. Name your project "Multi-City Weather Bot"
4. Select "Making a bot" as the use case
5. Describe your app: "Automated weather updates for Bratislava (Slovakia), Nairobi and Kisumu (Kenya)"

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
- Consider Twitter API v2 rate limits: 300 posts per 15-minute window

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
- **Free Plan**: 1,000 calls/day, 60 calls/minute (sufficient for multi-city bot)
- **Paid Plans**: Available if you need weather alerts and extended forecasts

### API Endpoints Used:
- **Current Weather API** (2.5/weather) - ✅ Free tier supported
- **Weather Forecast API** (2.5/forecast) - ✅ Free tier supported
- **One Call API 3.0** (weather alerts) - ❌ Requires paid subscription

### Multi-City Considerations:
- **3 cities × hourly updates** = ~72 API calls/day (well within free limits)
- **Forecast and daily summaries** add ~20-30 additional calls/day
- **Total usage**: ~100-150 API calls/day (easily within 1,000 daily limit)

### Free Tier Limitations:
- ❌ No weather alerts/warnings
- ❌ Limited to 5-day forecast
- ✅ Current weather for all cities
- ✅ 3-hour forecast intervals
- ✅ All essential weather data

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

# Multi-City Configuration (handled automatically by config.py)
# The following cities are pre-configured:
# - Bratislava, Slovakia (48.1486, 17.1077)
# - Nairobi, Kenya (-1.2921, 36.8219)
# - Kisumu, Kenya (-0.0917, 34.7680)

# Bot Settings
LOG_LEVEL=INFO
SKIP_STARTUP_TEST=false  # Set to true for production to avoid rate limiting
```

### Multi-City Environment Notes:
- **No manual coordinates needed** - Cities are pre-configured in `config.py`
- **Automatic timezone handling** - Each city uses appropriate timezone
- **Production optimization** - Set `SKIP_STARTUP_TEST=true` for Caprover deployment
- **City-specific hashtags** - Automatically included for each location

## 4. Testing Your Setup

After setting up the API keys, test your multi-city configuration:

```bash
# Test all cities without posting to Twitter
python main.py --mode test

# Test individual cities
python main.py --mode test --city Nairobi
python main.py --mode test --city Kisumu
python main.py --mode test --city Bratislava

# Test different modes with actual posting (use carefully)
python main.py --mode current --city Nairobi     # Single city current weather
python main.py --mode forecast --hours 3         # All cities 3-hour forecast
python main.py --mode daily --city Bratislava    # Single city daily summary
```

### Expected Test Output:
```
2025-08-30 10:30:00,611 - logger - INFO - Authenticated as: YourTwitterHandle (@yourusername)
2025-08-30 10:30:00,611 - logger - INFO - Successfully authenticated with Twitter API
Testing weather services for all cities...
Testing Nairobi...
✅ Nairobi: 24°C, Partly Cloudy
Testing Kisumu...
✅ Kisumu: 26°C, Clear Sky
Testing Bratislava...
✅ Bratislava: 18°C, Overcast
```

## Troubleshooting

### Twitter API Issues:
- **403 Forbidden**: Check app permissions, ensure Read+Write access
- **401 Unauthorized**: Verify all tokens and keys are correct
- **429 Rate Limited**: Multi-city updates might exceed rate limits
  - Solution: The bot includes 5-second delays between cities
  - Monitor usage: 3 cities × hourly = 72 tweets/day (within limits)

### OpenWeatherMap Issues:
- **401 Unauthorized**: Check API key is correct and active
- **403 Forbidden**: API key might not have access to required endpoints
- **429 Rate Limited**: Free plan limits exceeded (rare with 3 cities)
  - Monitor usage: ~100-150 calls/day vs 1,000 daily limit

### Multi-City Specific Issues:
- **"City not configured" error**: 
  ```bash
  python main.py --mode test  # Lists available cities: Nairobi, Kisumu, Bratislava
  ```
- **Only some cities posting**: Check logs for individual city failures
- **Rate limiting affecting all cities**: Increase delays in `multi_city_bot.py`

### General Issues:
- Check `.env` file exists and has correct format
- Ensure no spaces around the `=` in environment variables
- Verify internet connection
- Check logs in `logs/` directory for detailed error messages
- For production: Set `SKIP_STARTUP_TEST=true` to avoid startup rate limits

## Security Best Practices

1. **Never commit API keys to version control**
2. **Use environment variables for all secrets**
3. **Regularly rotate API keys**
4. **Monitor API usage to detect unusual activity**
5. **Use the principle of least privilege for API permissions**
