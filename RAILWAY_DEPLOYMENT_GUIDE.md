# Deploying Miku Bot to Railway

This guide walks you through deploying your Miku Telegram Bot to Railway.app, a modern platform that offers $5 free monthly credit and simple deployment.

## Prerequisites

1. A [Railway](https://railway.app/) account
2. Your Telegram Bot token from BotFather
3. Reddit API credentials (optional)

## Step 1: Prepare Your Project

Your project is already set up for deployment. The main files Railway will use are:
- `requirements.txt` - Lists all Python dependencies
- `Procfile` - Tells Railway how to run your application

## Step 2: Create a new Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your GitHub account if you haven't already
5. Select your Miku Bot repository

## Step 3: Configure Environment Variables

In your Railway project, go to the "Variables" tab and add the following:

**Required Variables:**
- `TELEGRAM_TOKEN` - Your Telegram bot token from BotFather
- `TELEGRAM_CHANNEL` - Your channel name (e.g., Miku_nakano111)
- `PORT` - Set to `5000`
- `PYTHON_VERSION` - Set to `3.9`
- `RAILWAY_ENVIRONMENT` - Set to `production`

**Optional Variables:**
- `REDDIT_CLIENT_ID` - Your Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Your Reddit API client secret
- `REDDIT_USER_AGENT` - Set to `MikuBot/1.0`
- `MAIN_POST_INTERVAL` - Time in seconds between fact posts (default: 600)
- `IMAGE_POST_INTERVAL` - Time in seconds between image posts (default: 900)
- `REDDIT_POST_INTERVAL` - Time in seconds between Reddit posts (default: 3600)

## Step 4: Configure the Start Command

Railway needs to know which command to run to start your bot. You have two options:

### Option 1: Use the Procfile (Recommended)
Your project already has a `Procfile` that Railway will automatically detect:

```
web: python fly_standalone.py
```

This file tells Railway to run your bot using the standalone script.

### Option 2: Manual Command (Optional)
If you need to override the command, go to the "Settings" tab and set the Start Command to:

```
python fly_standalone.py
```

## Step 5: Deploy

1. Go to the "Deployments" tab
2. Railway should automatically deploy your application
3. Check the logs to ensure everything is working properly

## Monitoring Your Bot

1. Click on the "Deployments" tab to see deployment status
2. Click on a deployment to view logs
3. Use the "Metrics" tab to monitor resource usage

## Troubleshooting

**Bot Doesn't Post**: Check the logs to see if there are authentication errors. Verify your `TELEGRAM_TOKEN` is correct.

**High Memory Usage**: Your bot is designed to be efficient, but if you see high memory usage, consider increasing the interval between posts.

**Railway Free Tier Limits**: Keep in mind the $5 credit limit. If you're approaching this limit, consider:
- Increasing intervals between posts
- Removing the Reddit functionality if not needed
- Scaling down the container resources

## Managing Railway Costs

Railway's $5 free credit should be sufficient for running this bot. However, to prevent unexpected charges:

1. Set up billing alerts in Railway
2. Monitor your usage in the "Metrics" tab
3. Consider scaling down resources if approaching the limit

## Additional Tips

- The bot will automatically handle restarts and continue from where it left off
- Railway automatically manages certificates and HTTPS
- For continuous updates, connect your GitHub repository to automatically deploy new commits

---

Remember to regularly check your Telegram channel to ensure the bot is posting content as expected!