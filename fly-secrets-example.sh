#!/bin/bash
# Example script for setting fly.io secrets
# Copy this file to fly-secrets.sh, modify with your actual values, and run to set your secrets

# Telegram Bot Token
flyctl secrets set TELEGRAM_BOT_TOKEN="your_telegram_bot_token_here"

# Telegram Channel Username
flyctl secrets set TELEGRAM_CHANNEL_USERNAME="your_channel_name_here"

# Reddit API credentials (if used)
flyctl secrets set REDDIT_CLIENT_ID="your_reddit_client_id_here"
flyctl secrets set REDDIT_CLIENT_SECRET="your_reddit_client_secret_here"

# Optional: Post intervals (in minutes)
flyctl secrets set MAIN_POST_INTERVAL="10"
flyctl secrets set IMAGE_POST_INTERVAL="15"
flyctl secrets set REDDIT_POST_INTERVAL="60"

echo "All secrets have been set!"