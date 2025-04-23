#!/usr/bin/env python
"""
Production-ready script to run the Miku bot with health check endpoint for fly.io.
This script is specifically modified for deployment to fly.io.
"""
import os
import logging
import socket
import sys
import time
import traceback
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
from bot import setup_bot

# Set up logging with more verbose output for production
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global vars to track bot status
bot_status = {
    "status": "starting",
    "uptime_seconds": 0,
    "start_time": time.time()
}

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status' or self.path == '/health':
            # Calculate current uptime
            bot_status["uptime_seconds"] = int(time.time() - bot_status["start_time"])
            uptime = bot_status["uptime_seconds"]
            
            # Format uptime for human readability
            uptime_human = f"{uptime // 86400}d {(uptime % 86400) // 3600}h {(uptime % 3600) // 60}m {uptime % 60}s"
            
            # Prepare response data
            response_data = {
                "status": bot_status["status"],
                "bot_name": "Nakano Miku Bot",
                "version": "1.0.0",
                "uptime_seconds": uptime,
                "uptime_human": uptime_human,
                "keepalive": True,
                "channel": os.getenv("TELEGRAM_CHANNEL_USERNAME", "Unknown")
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())
        else:
            # For any other path, return 404
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def log_message(self, format, *args):
        # Customize logging or disable it
        if args[1] != "200":  # Only log non-200 responses to reduce noise
            logger.info("%s - %s", self.client_address[0], format % args)

def start_health_server():
    """Start the health check server in a separate thread"""
    # Get port from environment variable with default fallback
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Starting health check server on port {port}")
    
    # Run server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server_thread

# Check if the bot is already running by detecting conflicts
def is_bot_already_running():
    """
    Check if another instance of this bot is already running.
    Attempts to make a getUpdates request to Telegram to see if there's a conflict.
    
    Returns:
        bool: True if bot is already running, False otherwise
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return False
        
    try:
        # Try to make a getUpdates request
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url, timeout=5)
        
        # If we got a conflict error, another instance is running
        if response.status_code == 409:
            logger.info("Conflict detected: Bot is already running in another instance.")
            return True
            
        # If successful, no other instance is running
        if response.ok:
            logger.info("No conflict detected: Bot is not running elsewhere.")
            return False
            
        # If some other error, log it and assume no conflict
        logger.warning(f"Unexpected response checking bot status: {response.status_code}")
        return False
    except Exception as e:
        logger.exception(f"Error checking if bot is running: {e}")
        return False

def run_standalone_with_health_check():
    """Run the bot with a health check endpoint for containerized environments"""
    print("============================================")
    print("MIKU BOT CONTAINERIZED MODE WITH HEALTH CHECK")
    print("Running on fly.io")
    print("============================================")
    
    # Start the health check server
    health_server_thread = start_health_server()
    
    # Check if another instance is already running
    if is_bot_already_running():
        bot_status["status"] = "conflict_detected"
        logger.warning("Another instance of the bot is already running!")
        
        # Just keep this process alive without starting another bot
        try:
            while True:
                time.sleep(60)
                logger.info("Monitoring... Bot is running in another instance.")
        except KeyboardInterrupt:
            logger.info("Monitor stopped.")
        return
    
    try:
        # Initialize Reddit client
        from api_clients import initialize_reddit_client
        reddit_client = initialize_reddit_client()
        
        # Update status
        bot_status["status"] = "initializing"
        
        # Start the bot directly
        updater = setup_bot()
        
        if updater:
            # Update status to running once bot is set up
            bot_status["status"] = "running"
            
            logger.info("Bot setup successful. Starting to poll for updates...")
            logger.info("Health check server is running alongside the bot")
            
            # Keep the script running with proper signal handling
            try:
                updater.idle()
            except KeyboardInterrupt:
                logger.info("Bot shutting down...")
                bot_status["status"] = "stopping"
                updater.stop()
        else:
            bot_status["status"] = "failed"
            logger.error("Bot setup failed. Check logs for details.")
            
            # Even if bot setup fails, keep the health check server running
            # so the container doesn't immediately restart
            while True:
                time.sleep(10)
                
    except Exception as e:
        bot_status["status"] = "error"
        logger.error(f"Error running standalone bot: {e}")
        traceback.print_exc()
        
        # Sleep briefly to avoid immediate container restarts
        time.sleep(10)

if __name__ == "__main__":
    # Always run with health check when executed directly
    run_standalone_with_health_check()