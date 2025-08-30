#!/bin/bash
set -e

echo "🌍 Starting Multi-City Weather Bot v2.0..."

# In Caprover, environment variables are set directly in the dashboard
# Only create .env if we're running locally and it doesn't exist
if [ ! -f .env ] && [ -z "$OPENWEATHER_API_KEY" ]; then
    if [ -f .env.example ]; then
        echo "⚠️ No environment variables found, creating .env from example..."
        cp .env.example .env
        echo "❗ Please configure your API keys in .env file or Caprover environment variables!"
    else
        echo "⚠️ No .env.example file found and no environment variables set!"
        echo "❗ Please set environment variables in Caprover dashboard!"
    fi
elif [ -n "$OPENWEATHER_API_KEY" ]; then
    echo "✅ Environment variables detected from Caprover"
fi

# Skip testing in production to avoid rate limits
if [ "$ENVIRONMENT" = "development" ] || [ "$SKIP_STARTUP_TEST" != "true" ]; then
    echo "🧪 Testing bot functionality..."
    python3 main.py --mode test || {
        echo "❌ Bot test failed! Please check your API keys and configuration."
        echo "📋 Required environment variables:"
        echo "   - OPENWEATHER_API_KEY"
        echo "   - TWITTER_CONSUMER_KEY"
        echo "   - TWITTER_CONSUMER_SECRET" 
        echo "   - TWITTER_ACCESS_TOKEN"
        echo "   - TWITTER_ACCESS_TOKEN_SECRET"
        echo "   - TWITTER_BEARER_TOKEN"
        exit 1
    }
else
    echo "⏩ Skipping startup test in production to avoid rate limits"
    echo "✅ Production mode - assuming configuration is valid"
fi

# Start cron daemon
echo "🕐 Starting cron daemon..."
service cron start

# Clear any existing cron jobs to avoid conflicts
echo "🧹 Clearing any existing cron jobs..."
crontab -r 2>/dev/null || echo "No existing crontab found"

# Setup single multi-city cron job for hourly updates
echo "⚙️ Setting up hourly weather updates..."

# Create single cron entry for all cities (uses multi-city mode with built-in delays)
echo "0 * * * * cd /app && /usr/local/bin/python3 main.py --mode multi-city >> logs/multi_city_cron.log 2>&1" > /tmp/crontab

# Install cron jobs
crontab /tmp/crontab

echo "📋 Installed cron job:"
crontab -l

# Create initial log entry
mkdir -p logs
echo "$(date): Multi-City Weather Bot v2.0 started - All cities enabled" >> logs/multi_city_cron.log
echo "$(date): Cron job should execute: /usr/local/bin/python3 main.py --mode multi-city" >> logs/multi_city_cron.log

echo "✅ Hourly updates scheduled:"
echo "   - Multi-city mode: All cities (Bratislava, Nairobi, Kisumu) at minute 0"
echo "   - Built-in 5-second delays between cities to avoid rate limits"
echo "   - Logs: Check logs/multi_city_cron.log for cron job output"

# Start health check server in background
echo "🏥 Starting health check server..."
python3 healthcheck.py &

# Execute the main command
echo "🚀 Starting main bot process..."
exec "$@"
