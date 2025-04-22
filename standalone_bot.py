"""
A completely standalone Miku Bot implementation.
This script runs the bot without any web interface or Flask dependencies.
"""
import logging
import time
import os
from bot import setup_bot
from scheduler import setup_scheduler
from api_clients import initialize_reddit_client

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def run_standalone():
    """Run the bot in completely standalone mode"""
    print("=== Miku Bot Completely Standalone Mode ===")
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
        try:
            updater.idle()
        except KeyboardInterrupt:
            print("Stopping bot...")
            updater.stop()
        except Exception as e:
            logger.error(f"Error in bot runner: {e}")
    else:
        print("Bot setup failed. Check logs for details.")

if __name__ == "__main__":
    run_standalone()