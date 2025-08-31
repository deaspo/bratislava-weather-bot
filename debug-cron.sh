#!/bin/bash

# Cron Debugging Script for Multi-City Weather Bot
echo "🔍 Weather Bot Cron Debugging Report"
echo "======================================"
echo ""

echo "📅 Current Date and Time:"
date
echo ""

echo "🕐 Cron Service Status:"
service cron status || echo "❌ Cron service not running"
echo ""

echo "� Cron Daemon Process:"
ps aux | grep cron | grep -v grep || echo "❌ No cron processes found"
echo ""

echo "�📋 Current Crontab:"
crontab -l || echo "❌ No crontab found"
echo ""

echo "� Bot Log Files:"
ls -la logs/ 2>/dev/null || echo "❌ No logs directory found"
echo ""

echo "🧪 Cron Test Log (should update every 5 minutes):"
if [ -f logs/cron_test.log ]; then
    echo "📄 Last 10 lines of cron_test.log:"
    tail -10 logs/cron_test.log
    echo ""
    echo "📊 Cron test entries count: $(wc -l < logs/cron_test.log 2>/dev/null || echo "0")"
else
    echo "❌ Cron test log not found - cron may not be working"
fi
echo ""

echo "🌍 Multi-City Weather Log:"
if [ -f logs/multi_city_cron.log ]; then
    echo "📄 Last 10 lines of multi_city_cron.log:"
    tail -10 logs/multi_city_cron.log
    echo ""
    echo "� Weather update entries: $(grep -c "Starting multi-city weather update" logs/multi_city_cron.log 2>/dev/null || echo "0")"
else
    echo "❌ Multi-city cron log not found"
fi
echo ""

echo "🧪 Manual Test:"
echo "Running: python3 main.py --mode test"
timeout 30 python3 main.py --mode test || echo "❌ Manual test failed or timed out"
echo ""

echo "🌍 Environment Variables Check:"
env | grep -E "(OPENWEATHER|TWITTER)" | sed 's/=.*/=***HIDDEN***/' || echo "❌ No weather/twitter env vars found"
echo ""

echo "💡 Troubleshooting Steps:"
echo "1. Check if cron is running: service cron status"
echo "2. Look for test cron entries: tail logs/cron_test.log"
echo "3. If no test entries, cron daemon isn't working"
echo "4. Check container logs in Caprover dashboard"
echo "5. Try restarting the container/app in Caprover"
echo ""

echo "🔧 Quick Fixes to Try:"
echo "1. Restart cron: service cron restart"
echo "2. Reinstall crontab: crontab /tmp/crontab"
echo "3. Check cron process: ps aux | grep cron"
