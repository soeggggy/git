"""
A script to run only the Telegram bot without the Flask web interface.
This avoids port conflicts when running both services.
"""
import sys
import logging
from bot import setup_bot
from api_clients import initialize_reddit_client

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Run the bot in standalone mode"""
    logger.info("Starting Miku bot in standalone mode...")
    
    # Initialize Reddit client if credentials are available
    initialize_reddit_client()
    
    # Start the bot
    updater = setup_bot()
    
    logger.info("Bot is running. Press Ctrl+C to stop.")
    
    # Keep the script running
    try:
        # Use updater.idle() to properly handle signals
        if updater:
            updater.idle()
        else:
            # Fallback if updater wasn't properly initialized
            import time
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Bot is shutting down...")
        if updater:
            updater.stop()
    except Exception as e:
        logger.error(f"Error in bot runner: {e}")

if __name__ == '__main__':
    main()