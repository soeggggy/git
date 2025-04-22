import os
import logging
from telegram.ext import Updater, CommandHandler
from handlers import start_command
from scheduler import setup_scheduler

logger = logging.getLogger(__name__)

def setup_bot():
    """
    Setup and start the Telegram bot.
    """
    # Get token from environment variable
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return

    # Create the Updater and pass it the bot's token
    updater = Updater(token=token, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start_command))

    # Set up the scheduler for timed posts
    setup_scheduler(updater)

    # Start the Bot
    logger.info("Starting bot...")
    updater.start_polling()
    
    # Run the bot until the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()
