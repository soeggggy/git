"""
Special bot runner designed to avoid port conflicts.
This script is specifically created to be called by the 'run_miku_bot' workflow.
"""
import os
import sys
import socket
import logging
import subprocess
import time

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def run_standalone_bot():
    """Run the bot in standalone mode, ensuring no port conflicts"""
    print("==== Miku Bot Special Runner ====")
    
    # Check if port 5000 is in use
    if is_port_in_use(5000):
        print("Port 5000 is already in use. Running bot in standalone mode...")
        # Import and run the standalone bot without using Flask
        import standalone_bot
        standalone_bot.run_standalone()
    else:
        print("Port 5000 is available. Starting web interface and bot...")
        # Start the combined mode with web interface
        os.system("python main.py")

if __name__ == "__main__":
    run_standalone_bot()