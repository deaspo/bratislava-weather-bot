#!/bin/bash

# Monitor Bratislava Weather Bot logs and status

echo "📊 Bratislava Weather Bot Status"
echo "================================="

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "✅ Virtual environment: OK"
else
    echo "❌ Virtual environment: Missing"
fi

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ Configuration file: OK"
else
    echo "❌ Configuration file: Missing"
fi

# Check if cron job is set up
if crontab -l 2>/dev/null | grep -q "main.py"; then
    echo "✅ Cron job: Active"
    echo "   Schedule: $(crontab -l 2>/dev/null | grep main.py | cut -d' ' -f1-5)"
else
    echo "❌ Cron job: Not configured"
fi

# Show recent log entries
echo ""
echo "📝 Recent Activity:"
echo "==================="

if [ -f "logs/cron.log" ]; then
    echo "Last 10 cron log entries:"
    tail -10 logs/cron.log
else
    echo "No cron log file found"
fi

echo ""
echo "📊 Log Files:"
echo "============="
if [ -d "logs" ]; then
    ls -la logs/
else
    echo "No logs directory found"
fi

# Test bot connectivity
echo ""
echo "🧪 Testing Bot Connectivity:"
echo "============================="
source venv/bin/activate 2>/dev/null || echo "Warning: Could not activate virtual environment"
python main.py --mode test 2>/dev/null && echo "✅ Bot test passed" || echo "❌ Bot test failed"
