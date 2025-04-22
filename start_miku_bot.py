"""
Start only the Miku bot in standalone mode. 
This script is designed to be run by the run_miku_bot workflow.
It ONLY starts the bot without any web interface to avoid port conflicts.
"""
import logging
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Main entry point
if __name__ == "__main__":
    print("===============================================")
    print("RUNNING MIKU BOT IN DEDICATED STANDALONE MODE")
    print("Web interface is disabled to avoid port conflicts")
    print("===============================================")
    
    # Import and run the bot directly
    from bot_runner import run_standalone_bot
    run_standalone_bot()