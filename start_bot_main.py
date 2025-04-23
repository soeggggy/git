#!/usr/bin/env python
"""
Special script to start the bot with the main application.
This script ensures both the web interface and bot are running.
"""
import os
import sys
import time
import logging
from threading import Thread

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_web_interface():
    """Start the Flask web interface"""
    logger.info("Starting web interface...")
    os.environ['FORCE_WEB_INTERFACE'] = 'true'  # Force web interface mode
    from main import app
    # We can't actually run the app here because it blocks
    # We'll let gunicorn handle that

def start_bot_thread():
    """Start the Telegram bot in a separate thread"""
    logger.info("Starting bot thread...")
    try:
        # Import and start bot
        from bot import setup_bot
        from scheduler import setup_scheduler
        
        # Initialize the bot
        updater = setup_bot()
        if not updater:
            logger.error("Failed to initialize bot")
            return

        # Set up the scheduler
        setup_scheduler(updater)
        
        # Start polling for updates
        logger.info("Starting bot polling...")
        updater.start_polling()
        
        logger.info("Bot polling started successfully")
    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    logger.info("===== Starting Miku bot and web interface =====")
    
    # Start web interface (handled by gunicorn)
    run_web_interface()
    
    # Start bot in separate thread
    bot_thread = Thread(target=start_bot_thread)
    bot_thread.daemon = True
    bot_thread.start()
    
    logger.info("Main startup script completed")
    
    # Print a message that can be seen in the Gunicorn logs
    print("Bot startup process completed - bot thread started")
    
    # Let the main thread continue - gunicorn will handle this process