#!/bin/bash

# Caprover Setup Script for Bratislava Weather Bot
# This script helps you set up the app in Caprover

set -e

echo "🚢 Caprover Setup for Bratislava Weather Bot"
echo "============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if caprover CLI is installed
if ! command -v caprover &> /dev/null; then
    print_error "Caprover CLI is not installed!"
    echo "Install it with: npm install -g caprover"
    exit 1
fi

print_info "Caprover CLI found ✅"

# Get Caprover details
echo ""
echo "Please provide your Caprover details:"

read -p "Caprover Server URL (e.g., https://captain.yourdomain.com): " CAPROVER_SERVER
read -s -p "Caprover Root Password: " CAPROVER_PASSWORD
echo ""
read -p "App Name (e.g., bratislava-weather-bot): " APP_NAME

# Login to Caprover
print_info "Logging into Caprover..."
caprover login --caproverUrl "$CAPROVER_SERVER" --caproverPassword "$CAPROVER_PASSWORD"

# Check if app exists, if not create it
print_info "Checking if app exists..."
if caprover list --caproverUrl "$CAPROVER_SERVER" --caproverPassword "$CAPROVER_PASSWORD" | grep -q "$APP_NAME"; then
    print_info "App '$APP_NAME' already exists"
else
    print_info "Creating new app '$APP_NAME'..."
    caprover app --caproverUrl "$CAPROVER_SERVER" --caproverPassword "$CAPROVER_PASSWORD" --caproverApp "$APP_NAME" --action create
fi

print_info "Configuring app settings..."

# Enable app token for GitHub Actions deployment
print_info "Enabling app token for GitHub Actions..."
print_warning "You need to manually enable the app token in Caprover dashboard:"
print_warning "1. Go to your Caprover dashboard: $CAPROVER_SERVER"
print_warning "2. Navigate to Apps > $APP_NAME > Deployment tab"
print_warning "3. Click 'Enable App Token' and copy the token"
print_warning "4. Add this token to GitHub Secrets as 'APP_TOKEN'"

# Set environment variables
echo ""
echo "🔐 Setting up environment variables..."
echo "You'll need to provide your API keys:"

read -p "Twitter API Key: " TWITTER_API_KEY
read -s -p "Twitter API Secret: " TWITTER_API_SECRET
echo ""
read -s -p "Twitter Access Token: " TWITTER_ACCESS_TOKEN
echo ""
read -s -p "Twitter Access Token Secret: " TWITTER_ACCESS_TOKEN_SECRET
echo ""
read -s -p "Twitter Bearer Token: " TWITTER_BEARER_TOKEN
echo ""
read -p "OpenWeatherMap API Key: " OPENWEATHER_API_KEY

# Create environment variables JSON
ENV_VARS=$(cat <<EOF
{
  "TWITTER_API_KEY": "$TWITTER_API_KEY",
  "TWITTER_API_SECRET": "$TWITTER_API_SECRET",
  "TWITTER_ACCESS_TOKEN": "$TWITTER_ACCESS_TOKEN",
  "TWITTER_ACCESS_TOKEN_SECRET": "$TWITTER_ACCESS_TOKEN_SECRET",
  "TWITTER_BEARER_TOKEN": "$TWITTER_BEARER_TOKEN",
  "OPENWEATHER_API_KEY": "$OPENWEATHER_API_KEY",
  "CITY_NAME": "Bratislava",
  "COUNTRY_CODE": "SK",
  "LATITUDE": "48.1482",
  "LONGITUDE": "17.1067",
  "TIMEZONE": "Europe/Bratislava",
  "LOG_LEVEL": "INFO"
}
EOF
)

# Save environment variables to temporary file
echo "$ENV_VARS" > /tmp/env_vars.json

print_info "Setting environment variables in Caprover..."
# Note: This might need to be done manually in Caprover UI
print_warning "Environment variables need to be set manually in Caprover UI"
print_warning "Go to your app settings and add the environment variables"

# Configure app settings
print_info "Configuring app for persistent storage..."

cat > caprover_config.json <<EOF
{
  "appName": "$APP_NAME",
  "hasDefaultSubDomainSsl": true,
  "hasPersistentData": true,
  "notExposeAsWebApp": false,
  "forceSsl": true,
  "websocketSupport": false,
  "containerHttpPort": 8080,
  "description": "Automated weather bot for Bratislava, Slovakia",
  "instanceCount": 1,
  "preDeployScript": "",
  "serviceUpdateOverride": "",
  "customNginxConfig": "",
  "redirectDomain": ""
}
EOF

print_info "App configuration saved to caprover_config.json"

print_info "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to your Caprover dashboard: $CAPROVER_SERVER"
echo "2. Navigate to Apps > $APP_NAME > Deployment tab"
echo "3. Enable App Token and copy it"
echo "4. Add GitHub Secrets (see below)"
echo "5. Set environment variables in the app settings"
echo "6. Push to 'devel' branch to trigger deployment"
echo ""
echo "🔐 GitHub Secrets to add:"
echo "   CAPROVER_SERVER = $CAPROVER_SERVER"
echo "   APP_NAME = $APP_NAME"
echo "   APP_TOKEN = <token from Caprover dashboard>"
echo ""
echo "🔗 Your app will be available at: https://$APP_NAME.yourdomain.com"
echo ""
print_info "GitHub Actions will automatically deploy on push to 'devel' branch"
