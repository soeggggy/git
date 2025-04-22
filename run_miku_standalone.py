"""
Special script to run ONLY the Miku bot without Flask.
This script is specifically designed for the run_miku_bot workflow.
"""
import os
import sys
import logging
import socket
from standalone_bot import run_standalone

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("==============================================")
    print("MIKU BOT STANDALONE MODE - NO WEB INTERFACE")
    print("This script does NOT use Flask or web dependencies")
    print("==============================================")
    
    # Run the bot in standalone mode
    run_standalone()