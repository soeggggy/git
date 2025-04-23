# 🎀 Nakano Miku Telegram Bot

A dedicated Telegram bot for automatically sharing Nakano Miku content to a Telegram channel or group.

## 🌟 Features

- 📝 Automatically posts Miku facts on a schedule
- 🖼️ Shares high-quality Miku images
- 📱 Fetches content from Reddit (optional)
- 🔄 Prevents duplicate content using advanced tracking
- 📊 Simple web dashboard for monitoring (optional)
- 🚀 Ready for deployment to cloud platforms

## 🚀 Deployment Options

This bot can be deployed to several platforms:

### Railway (Recommended)

The simplest deployment option with $5 free monthly credit.

[View Railway Deployment Guide](./RAILWAY_DEPLOYMENT_GUIDE.md)

### Fly.io

Another excellent option with a generous free tier.

[View Fly.io Deployment Guide](./FLY_DEPLOYMENT_GUIDE.md)

### Other Options

- Render.com
- Heroku
- PythonAnywhere
- Oracle Cloud (Free Tier)

## ⚙️ Configuration

Configure the bot using environment variables:

```
# Required Telegram variables
TELEGRAM_TOKEN=your_bot_token_from_botfather
TELEGRAM_CHANNEL=Miku_nakano111

# Optional Reddit API variables
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

See [.env.example](./.env.example) for all available options.

## 🔧 Local Development

1. Clone this repository
2. Create a `.env` file based on `.env.example`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python railway_bot.py`

## 📊 Monitoring

The bot includes a built-in health check endpoint that responds on:
- `GET /` - Simple status page
- `GET /health` - Health check endpoint (returns 200 OK)

## 💡 Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License

MIT

---

Made with ❤️ for Nakano Miku fans