"""
A script to run only the Telegram bot without the Flask web interface.
This avoids port conflicts when running both services.
"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Run the bot in standalone mode"""
    print("=========================================")
    print("MIKU BOT STANDALONE MODE")
    print("Starting bot without web interface...")
    print("=========================================")
    
    # Use the completely standalone bot implementation
    import standalone_bot
    standalone_bot.run_standalone()

if __name__ == "__main__":
    main()