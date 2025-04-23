# Deploying Miku Bot to Fly.io

This guide will walk you through deploying your Nakano Miku Telegram bot to fly.io.

## Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io/)
2. **Fly CLI**: Install the flyctl command-line tool:
   ```
   curl -L https://fly.io/install.sh | sh
   ```
   Or on macOS: `brew install flyctl`

3. **Login to Fly.io**:
   ```
   flyctl auth login
   ```

## Deployment Steps

### 1. Download Your Code
First, download your Replit project or clone it from a connected Git repository.

### 2. Add Secrets

Your bot needs access to the same secrets/environment variables it uses on Replit. Set these up in fly.io:

```bash
# Set your Telegram bot token
flyctl secrets set TELEGRAM_BOT_TOKEN="your_telegram_bot_token"

# Set your Telegram channel username
flyctl secrets set TELEGRAM_CHANNEL_USERNAME="your_channel_name"

# Set Reddit credentials (if using Reddit features)
flyctl secrets set REDDIT_CLIENT_ID="your_reddit_client_id"
flyctl secrets set REDDIT_CLIENT_SECRET="your_reddit_client_secret"
```

### 3. Launch Your Application

From your project directory:

```bash
# Initial launch (first deployment)
flyctl launch
```

This will detect your `fly.toml` configuration, create an app, and prepare it for deployment.
You can just press Enter to accept the defaults when prompted.

### 4. Deploy Your Application

After launch is complete, deploy your application:

```bash
flyctl deploy
```

### 5. Monitor Your Deployment

Check the status of your deployment:

```bash
# View logs
flyctl logs

# Check app status
flyctl status
```

### 6. Access the Health Check

Your bot has a health check endpoint available at:

```
https://your-app-name.fly.dev/status
```

## Maintenance Commands

- **Update configuration**: After changing `fly.toml`, redeploy with `flyctl deploy`
- **View app information**: `flyctl status`
- **Restart the app**: `flyctl restart`
- **SSH into the VM**: `flyctl ssh console`
- **Scale resources**: `flyctl scale memory 512` (change memory allocation to 512MB)

## Troubleshooting

### Bot not responding
1. Check logs with `flyctl logs`
2. Verify secrets are set correctly with `flyctl secrets list`
3. Try restarting with `flyctl restart`

### Health check failing
1. Check if port 8080 is properly configured
2. Verify the health endpoint is returning a 200 status code
3. Check CPU/memory usage with `flyctl status`

## Important Notes

- Your bot runs in a containerized environment with its own unique IP
- The bot and health check run on port 8080 internally
- Resources are allocated based on your fly.io account limits and configuration
- If needed, you can scale up resources in your `fly.toml` file