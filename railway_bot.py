#!/usr/bin/env python
"""
Railway-optimized script to run the Miku bot.
This script combines the bot with a lightweight health check
endpoint for Railway's health monitoring.
"""
import logging
import os
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define the health check handler
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Respond to GET requests with a 200 OK status"""
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Miku Bot is running')
        
    def log_message(self, format, *args):
        """Minimize logging of health check requests"""
        if self.path != '/health' and self.path != '/':
            logger.info(format % args)

def start_health_server():
    """Start a simple HTTP server to respond to health checks"""
    # Use the PORT environment variable provided by Railway
    port = int(os.environ.get('PORT', 5000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Starting health check server on port {port}")
    server.serve_forever()

def is_bot_already_running():
    """
    Check if another instance of this bot is already running.
    Attempts to make a getUpdates request to Telegram to see if there's a conflict.
    
    Returns:
        bool: True if bot is already running, False otherwise
    """
    from bot import get_bot
    import requests
    
    # Get bot token from environment or config
    bot_token = os.environ.get('TELEGRAM_TOKEN')
    if not bot_token:
        try:
            from config import TELEGRAM_TOKEN
            bot_token = TELEGRAM_TOKEN
        except ImportError:
            # If config.py doesn't have TELEGRAM_TOKEN defined
            pass
        
    if not bot_token:
        logger.error("No Telegram token found. Cannot check if bot is running.")
        return False
        
    # Try to get updates to see if another instance is running
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates?offset=-1&limit=1&timeout=0"
        response = requests.get(url, timeout=5)
        if response.status_code == 409:
            logger.error("Another instance of this bot is already running!")
            return True
    except Exception as e:
        logger.error(f"Error checking bot status: {e}")
        
    return False

def run_bot():
    """Run the Miku bot with optimal settings for Railway"""
    logger.info("Starting Miku Bot (Railway Optimized Version)")
    
    # Add a startup delay to ensure clean initialization (helps with restarts)
    time.sleep(2)
    
    # Check if another instance is already running
    if is_bot_already_running():
        logger.error("Bot instance already running. Exiting to avoid conflicts.")
        return
    
    # Import bot setup functions
    from bot import setup_bot
    from scheduler import setup_scheduler
    
    # Initialize and start the bot
    try:
        # Initialize the bot
        updater = setup_bot()
        if not updater:
            logger.error("Failed to initialize bot. Check your TELEGRAM_TOKEN.")
            return
            
        # Set up the scheduler
        setup_scheduler(updater)
        
        # Start polling for updates
        logger.info("Starting bot polling...")
        updater.start_polling()
        
        # Run the bot indefinitely 
        updater.idle()
    except Exception as e:
        logger.error(f"Error running bot: {e}")

if __name__ == "__main__":
    # Start the health check server in a separate thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Run the bot in the main thread
    run_bot()