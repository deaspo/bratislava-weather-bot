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

# Create logs directory
mkdir -p logs

# Create initial log entry with diagnostics
{
    echo "=============================================="
    echo "$(date): Multi-City Weather Bot v2.0 started"
    echo "=============================================="
    echo "Container started at: $(date)"
    echo "Working directory: $(pwd)"
    echo "Python version: $(python3 --version)"
    echo "Python path: $(which python3)"
    echo "Environment check:"
    echo "  - OPENWEATHER_API_KEY: $(if [ -n "$OPENWEATHER_API_KEY" ]; then echo "✅ Set"; else echo "❌ Missing"; fi)"
    echo "  - TWITTER_CONSUMER_KEY: $(if [ -n "$TWITTER_CONSUMER_KEY" ]; then echo "✅ Set"; else echo "❌ Missing"; fi)"
    echo "  - TWITTER_ACCESS_TOKEN: $(if [ -n "$TWITTER_ACCESS_TOKEN" ]; then echo "✅ Set"; else echo "❌ Missing"; fi)"
    echo "Scheduler command: python3 main.py --mode multi-city"
    echo "Next execution should be at: $(date -d '+1 hour' '+%Y-%m-%d %H:00:00')"
    echo "=============================================="
    echo ""
} >> logs/multi_city_cron.log

# Start health check server in background
echo "🏥 Starting health check server..."
python3 healthcheck.py &

# Use Python scheduler instead of cron (more reliable in Docker)
echo "🚀 Starting Python-based scheduler..."
echo "🔧 This replaces cron with a more reliable Python scheduler"
echo "🕐 Weather updates: Every 2 hours at :00"
echo "💓 Test heartbeat: Every 5 minutes"
echo "📝 Logs: scheduler.log, scheduler_test.log, multi_city_cron.log"
echo ""
echo "✅ Scheduler configured:"
echo "   📅 Main updates: Every 2 hours at minute 0 (12:00, 2:00, 4:00, etc.)"
echo "   🌍 Multi-city mode: All cities (Nairobi → Kisumu → Bratislava)"
echo "   ⏱️  Built-in 5-second delays between cities to avoid rate limits"
echo "   💓 Heartbeat: Every 5 minutes for monitoring"
echo ""
echo "   💡 Monitor scheduler activity:"
echo "      tail -f logs/scheduler.log           (main scheduler activity)"
echo "      tail -f logs/scheduler_test.log      (heartbeat every 5 minutes)"  
echo "      tail -f logs/multi_city_cron.log     (weather updates every hour)"

# Run the Python scheduler, ensuring it's the main process
echo "🚀 Starting Python-based scheduler as the main container process..."
exec python3 -u python_scheduler.py