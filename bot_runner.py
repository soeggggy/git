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
    # Start the bot and save the updater
    updater = setup_bot()
    
    logging.info("Bot is running. Press Ctrl+C to stop.")
    
    # Keep the script running
    try:
        # If we have an updater, use idle to properly handle signals
        if updater:
            updater.idle()
        else:
            # Fallback if updater wasn't properly initialized
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Bot is shutting down...")
        if updater:
            updater.stop()
    except Exception as e:
        logging.error(f"Error in bot runner: {e}")

if __name__ == '__main__':
    run_standalone_bot()