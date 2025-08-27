#!/bin/bash
set -e

echo "🤖 Starting Bratislava Weather Bot..."

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

# Test bot functionality before starting services
echo "🧪 Testing bot functionality..."
python main.py --mode test || {
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

# Start cron daemon
echo "🕐 Starting cron daemon..."
service cron start

# Setup multi-city cron jobs for hourly updates
echo "⚙️ Setting up hourly weather updates..."

# Create cron entries for each city at staggered times
echo "0 * * * * cd /app && python main.py --mode city --city Bratislava >> logs/bratislava_cron.log 2>&1" >> /tmp/crontab
echo "5 * * * * cd /app && python main.py --mode city --city Nairobi >> logs/nairobi_cron.log 2>&1" >> /tmp/crontab
echo "10 * * * * cd /app && python main.py --mode city --city Kisumu >> logs/kisumu_cron.log 2>&1" >> /tmp/crontab

# Install cron jobs
crontab /tmp/crontab

# Create initial log entries
echo "$(date): Multi-City Weather Bot started" >> logs/bratislava_cron.log
echo "$(date): Multi-City Weather Bot started" >> logs/nairobi_cron.log  
echo "$(date): Multi-City Weather Bot started" >> logs/kisumu_cron.log

echo "✅ Hourly updates scheduled:"
echo "   - Bratislava: Every hour at minute 0"
echo "   - Nairobi: Every hour at minute 5"
echo "   - Kisumu: Every hour at minute 10"

# Start health check server in background
echo "🏥 Starting health check server..."
python healthcheck.py &

# Execute the main command
echo "🚀 Starting main bot process..."
exec "$@"
