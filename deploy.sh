#!/bin/bash

# Bratislava Weather Bot Deployment Script
# This script sets up the bot on a Hetzner VPS

set -e

echo "🤖 Setting up Bratislava Weather Bot..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip if not present
echo "🐍 Installing Python dependencies..."
sudo apt install -y python3 python3-pip python3-venv cron

# Create virtual environment
echo "🏗️ Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Create .env file from example
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "❗ Please edit .env file with your API keys before running the bot!"
else
    echo "✅ .env file already exists"
fi

# Make main.py executable
chmod +x main.py

# Create logs directory
mkdir -p logs

# Test the bot
echo "🧪 Testing bot functionality..."
python main.py --mode test

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Test the bot: python main.py --mode current"
echo "3. Set up cron job: ./setup_cron.sh"
echo "4. Monitor logs in the logs/ directory"
