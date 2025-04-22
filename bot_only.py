"""
A dedicated standalone script to run only the Telegram bot without the web interface.
This script is specifically designed to be called by the 'run_miku_bot' workflow.
"""
# Don't try to use Flask or run a web server
# Just import and run the completely standalone version
import standalone_bot

# Run the standalone bot
if __name__ == "__main__":
    standalone_bot.run_standalone()
