import logging
from bot import setup_bot

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    logging.info("Starting Miku bot in standalone mode...")
    # Start the bot
    setup_bot()
    logging.info("Bot is running. Press Ctrl+C to stop.")