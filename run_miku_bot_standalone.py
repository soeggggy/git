#!/usr/bin/env python
"""
Special bot launcher script to run ONLY the Miku bot in the run_miku_bot workflow.
This completely bypasses Flask app to avoid port conflicts.
"""
import os
import logging
import socket
import sys
import time
import traceback
from bot import setup_bot

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Force standalone mode for workflow
def force_standalone_bot():
    print("============================================")
    print("MIKU BOT FORCED STANDALONE MODE")
    print("This script bypasses Flask completely")
    print("============================================")
    
    try:
        # Initialize Reddit client
        from api_clients import initialize_reddit_client
        reddit_client = initialize_reddit_client()
        
        # Start the bot directly without Flask
        updater = setup_bot()
        
        # Keep the script running with proper signal handling
        if updater:
            print("Bot setup successful. Starting to poll for updates...")
            print("Press Ctrl+C to stop the bot")
            updater.idle()
        else:
            print("Bot setup failed. Check logs for details.")
            while True:
                time.sleep(10)
    except Exception as e:
        logger.error(f"Error running standalone bot: {e}")
        traceback.print_exc()
        
if __name__ == "__main__":
    # Always run in standalone mode when executed directly
    force_standalone_bot()