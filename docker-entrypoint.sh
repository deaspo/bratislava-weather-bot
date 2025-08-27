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

# Create initial log entry
echo "$(date): Bratislava Weather Bot started" >> logs/cron.log

# Start health check server in background
echo "🏥 Starting health check server..."
python healthcheck.py &

# Execute the main command
echo "🚀 Starting main bot process..."
exec "$@"
