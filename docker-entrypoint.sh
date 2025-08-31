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

# Alternative cron startup method if service fails
if ! pgrep cron > /dev/null; then
    echo "⚠️ Service cron didn't work, trying direct startup..."
    /usr/sbin/cron -f &
    sleep 2
fi

# Verify cron is running
echo "🔍 Verifying cron daemon status..."
if pgrep cron > /dev/null; then
    echo "✅ Cron daemon is running (PID: $(pgrep cron))"
else
    echo "❌ Cron daemon not running, trying one more time..."
    /usr/sbin/cron &
    sleep 2
    if pgrep cron > /dev/null; then
        echo "✅ Cron daemon started (PID: $(pgrep cron))"
    else
        echo "❌ Failed to start cron daemon"
        exit 1
    fi
fi

# Clear any existing cron jobs to avoid conflicts
echo "🧹 Clearing any existing cron jobs..."
crontab -r 2>/dev/null || echo "No existing crontab found"

# Setup cron job based on requirements
echo "⚙️ Setting up weather update schedule..."

# Create comprehensive cron job with full environment
cat > /tmp/crontab << EOF
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
PYTHONPATH=/app
OPENWEATHER_API_KEY=$OPENWEATHER_API_KEY
TWITTER_CONSUMER_KEY=$TWITTER_CONSUMER_KEY
TWITTER_CONSUMER_SECRET=$TWITTER_CONSUMER_SECRET
TWITTER_ACCESS_TOKEN=$TWITTER_ACCESS_TOKEN
TWITTER_ACCESS_TOKEN_SECRET=$TWITTER_ACCESS_TOKEN_SECRET
TWITTER_BEARER_TOKEN=$TWITTER_BEARER_TOKEN

# Test cron job every 5 minutes to verify cron is working
*/5 * * * * echo "\$(date): Cron test - I'm alive!" >> logs/cron_test.log 2>&1

# Hourly multi-city weather updates at minute 0 of every hour
0 * * * * cd /app && /usr/local/bin/python3 main.py --mode multi-city >> logs/multi_city_cron.log 2>&1

# Alternative schedules (uncomment one if you want different timing):
# Every 30 minutes: 0,30 * * * * cd /app && /usr/local/bin/python3 main.py --mode multi-city >> logs/multi_city_cron.log 2>&1
# Every 2 hours: 0 */2 * * * cd /app && /usr/local/bin/python3 main.py --mode multi-city >> logs/multi_city_cron.log 2>&1  
# Every 15 minutes: */15 * * * * cd /app && /usr/local/bin/python3 main.py --mode multi-city >> logs/multi_city_cron.log 2>&1
EOF

# Install cron jobs
crontab /tmp/crontab

echo "📋 Installed cron job:"
crontab -l
echo ""

# Verify cron daemon is running
echo "🔍 Cron daemon status:"
service cron status
echo ""

# Create initial log entry with more diagnostics
mkdir -p logs
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
    echo "Cron job command: /usr/local/bin/python3 main.py --mode multi-city"
    echo "Next cron execution should be at: $(date -d '+1 hour' '+%Y-%m-%d %H:00:00')"
    echo "=============================================="
    echo ""
} >> logs/multi_city_cron.log

echo "✅ Weather update schedule configured:"
echo "   🧪 Test job: Every 5 minutes (check logs/cron_test.log)"
echo "   📅 Main job: Every hour at minute 0 (12:00, 1:00, 2:00, etc.)"
echo "   🌍 Multi-city mode: All cities (Nairobi → Kisumu → Bratislava)"
echo "   ⏱️  Built-in 5-second delays between cities to avoid rate limits"
echo "   📝 Logs: Check logs/multi_city_cron.log for weather updates"
echo ""
echo "   💡 Monitor cron activity:"
echo "      tail -f logs/cron_test.log     (should update every 5 minutes)"
echo "      tail -f logs/multi_city_cron.log  (weather updates every hour)"

# Start health check server in background
echo "🏥 Starting health check server..."
python3 healthcheck.py &

# Use Python scheduler instead of cron (more reliable in Docker)
echo "🚀 Starting Python-based scheduler..."
echo "� This replaces cron with a more reliable Python scheduler"
echo "🕐 Weather updates: Every hour at :00"  
echo "💓 Test heartbeat: Every 5 minutes"
echo "📝 Logs: scheduler.log, scheduler_test.log, multi_city_cron.log"

# Run the Python scheduler (this keeps the container alive)
exec python3 python_scheduler.py
