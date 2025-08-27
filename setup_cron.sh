#!/bin/bash

# Setup cron jobs for Multi-City Weather Bot

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$SCRIPT_DIR/.venv/bin/python"
MAIN_SCRIPT="$SCRIPT_DIR/main.py"

echo "🕐 Setting up cron jobs for Multi-City Weather Bot..."

# Create cron job entries
# Multi-city mode (recommended) - Single job posts all cities with built-in delays
MULTI_CITY_CRON="0 * * * * cd $SCRIPT_DIR && $PYTHON_PATH $MAIN_SCRIPT --mode multi-city >> logs/multi_city_cron.log 2>&1"

# Individual city modes (alternative) - Separate jobs for each city
BRATISLAVA_CRON="0 * * * * cd $SCRIPT_DIR && $PYTHON_PATH $MAIN_SCRIPT --mode city --city Bratislava >> logs/bratislava_cron.log 2>&1"
NAIROBI_CRON="5 * * * * cd $SCRIPT_DIR && $PYTHON_PATH $MAIN_SCRIPT --mode city --city Nairobi >> logs/nairobi_cron.log 2>&1"
KISUMU_CRON="10 * * * * cd $SCRIPT_DIR && $PYTHON_PATH $MAIN_SCRIPT --mode city --city Kisumu >> logs/kisumu_cron.log 2>&1"

echo "Choose deployment mode:"
echo "1) Multi-city mode - Single job posts all cities with delays (RECOMMENDED)"
echo "2) Separate mode - Individual jobs for each city"
echo "3) Both modes (for testing only)"
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "Setting up multi-city cron job..."
        (crontab -l 2>/dev/null; echo "$MULTI_CITY_CRON") | crontab -
        echo "✅ Multi-city cron job added!"
        echo "📍 All cities: Every hour at minute 0 with 5-second delays"
        ;;
    2)
        echo "Setting up separate city updates..."
        (crontab -l 2>/dev/null; echo "$BRATISLAVA_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$NAIROBI_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$KISUMU_CRON") | crontab -
        echo "✅ Separate cron jobs added!"
        echo "📍 Bratislava: Every hour at minute 0"
        echo "📍 Nairobi: Every hour at minute 5"
        echo "📍 Kisumu: Every hour at minute 10"
        ;;
    3)
        echo "Setting up both modes (testing only)..."
        (crontab -l 2>/dev/null; echo "$MULTI_CITY_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$BRATISLAVA_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$NAIROBI_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$KISUMU_CRON") | crontab -
        echo "✅ All cron jobs added!"
        echo "⚠️  Warning: This will post updates twice for each city!"
        ;;
    3)
        echo "Setting up both modes..."
        (crontab -l 2>/dev/null; echo "$BRATISLAVA_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$NAIROBI_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$KISUMU_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$MULTI_CITY_CRON") | crontab -
        echo "✅ All cron jobs added!"
        echo "⚠️  Warning: This will post updates twice for each city!"
        ;;
    *)
        echo "Invalid choice. Setting up separate updates (default)..."
        (crontab -l 2>/dev/null; echo "$BRATISLAVA_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$NAIROBI_CRON") | crontab -
        (crontab -l 2>/dev/null; echo "$KISUMU_CRON") | crontab -
        echo "✅ Separate cron jobs added!"
        ;;
esac

echo ""
echo "📂 Logs will be saved to:"
echo "  - logs/bratislava_cron.log"
echo "  - logs/nairobi_cron.log" 
echo "  - logs/kisumu_cron.log"
echo "  - logs/multi_city_cron.log (if batch mode enabled)"
echo ""
echo "To view current crontab:"
echo "  crontab -l"
echo ""
echo "To remove cron jobs:"
echo "  crontab -e  # and delete the relevant lines"
echo ""
echo "To monitor logs:"
echo "  tail -f logs/bratislava_cron.log"
echo "  tail -f logs/nairobi_cron.log"
echo "  tail -f logs/kisumu_cron.log"
echo "  tail -f logs/multi_city_cron.log"
echo ""
echo "To test manually:"
echo "  python main.py --mode city --city Bratislava"
echo "  python main.py --mode city --city Nairobi"
echo "  python main.py --mode city --city Kisumu"
echo "  python main.py --mode multi-city"
