#!/bin/bash
set -e

echo "🤖 Starting Bratislava Weather Bot..."

# Check if .env file exists, if not create from example
if [ ! -f .env ]; then
    echo "⚠️ No .env file found, creating from example..."
    cp .env.example .env
    echo "❗ Please configure your API keys in the Caprover environment variables!"
fi

# Test bot functionality before starting services
echo "🧪 Testing bot functionality..."
python main.py --mode test || {
    echo "❌ Bot test failed! Please check your API keys and configuration."
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
