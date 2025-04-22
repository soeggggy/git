"""
A dedicated standalone script to run only the Telegram bot without the web interface.
This script is specifically designed to be called by the 'run_miku_bot' workflow.
"""
import logging
from bot import setup_bot
from api_clients import initialize_reddit_client

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

print("=== Miku Bot Standalone Mode ===")
print("Starting bot without web interface...")

# Initialize Reddit client if credentials are available
reddit_client = initialize_reddit_client()
if reddit_client:
    print("Reddit client initialized successfully")
else:
    print("Reddit client initialization failed or credentials not provided")

# Start the bot
print("Setting up bot...")
updater = setup_bot()

if updater:
    print("Bot setup successful. Starting to poll for updates...")
    print("Press Ctrl+C to stop the bot")
    
    # Keep the script running with proper signal handling
    updater.idle()
else:
    print("Bot setup failed. Check logs for details.")
