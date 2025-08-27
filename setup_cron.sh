#!/bin/bash

# Setup cron job for Bratislava Weather Bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/venv/bin/python"
MAIN_SCRIPT="$SCRIPT_DIR/main.py"

echo "🕐 Setting up cron job for Bratislava Weather Bot..."

# Create cron job entry
CRON_JOB="0 * * * * cd $SCRIPT_DIR && $PYTHON_PATH $MAIN_SCRIPT --mode current >> logs/cron.log 2>&1"

# Add to crontab
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "✅ Cron job added successfully!"
echo "📍 Bot will run hourly at minute 0"
echo "📂 Logs will be saved to logs/cron.log"
echo ""
echo "To view current crontab:"
echo "  crontab -l"
echo ""
echo "To remove the cron job:"
echo "  crontab -e  # and delete the line"
echo ""
echo "To monitor cron logs:"
echo "  tail -f logs/cron.log"
