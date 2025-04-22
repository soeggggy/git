import os

# Telegram bot configuration
DEFAULT_CHANNEL = os.getenv("TELEGRAM_CHANNEL_USERNAME", "")

# Reddit API configuration
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "MikuBot/1.0")

# Reddit subreddits to fetch Miku content from
MIKU_SUBREDDITS = [
    "5ToubunNoHanayome",
    "churchofmiku",
    "MikuNakano",
    "Nakano_Miku"
]

# API endpoints for anime images
WAIFU_PICS_API = "https://api.waifu.pics/sfw/waifu"
ANIME_PICS_API = "https://api.waifu.im/search"
SAFEBOORU_API = "https://safebooru.org/index.php?page=dapi&s=post&q=index&json=1&tags=nakano_miku"

# Scheduling intervals (in seconds)
# These can be customized via environment variables
MAIN_POST_INTERVAL = int(os.getenv("MAIN_POST_INTERVAL", 30)) * 60  # Default: Every 30 minutes
IMAGE_POST_INTERVAL = int(os.getenv("IMAGE_POST_INTERVAL", 15)) * 60  # Default: Every 15 minutes
REDDIT_POST_INTERVAL = int(os.getenv("REDDIT_POST_INTERVAL", 60)) * 60  # Default: Every hour

# Paths for data storage
HISTORY_FILE = "post_history.json"
