import logging
import time
from bot import setup_bot
from scheduler import setup_scheduler
from api_clients import initialize_reddit_client
from telegram.ext import Updater

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def run_standalone_bot():
    """Run the bot in standalone mode without the Flask web interface"""
    logging.info("Starting Miku bot in standalone mode...")
    
    # Initialize Reddit client if credentials are available
    initialize_reddit_client()
    
    # Create and configure the bot
    from config import TELEGRAM_BOT_TOKEN
    updater = Updater(TELEGRAM_BOT_TOKEN)
    
    # Set up scheduler for regular posts
    setup_scheduler(updater)
    
    # Start the bot
    updater.start_polling()
    
    logging.info("Bot is running. Press Ctrl+C to stop.")
    
    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Bot is shutting down...")
        updater.stop()

if __name__ == '__main__':
    run_standalone_bot()