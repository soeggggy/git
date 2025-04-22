"""
IMPORTANT: This file is specifically for the run_miku_bot workflow.
It explicitly checks for port conflicts and runs the bot without the web interface.
"""
import os
import socket
import sys
import logging
from standalone_bot import run_standalone

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def main():
    """Run the Miku bot in standalone mode, avoiding port conflicts"""
    print("====================================================")
    print("MIKU BOT WORKFLOW RUNNER (for run_miku_bot workflow)")
    print("====================================================")
    
    # Check if port 5000 is already in use (likely by the web app)
    if is_port_in_use(5000):
        print("Port 5000 is already in use. Running bot in standalone mode...")
    else:
        print("Port 5000 is available, but still using standalone mode for consistency...")
    
    # ALWAYS run in standalone mode to avoid conflicts
    print("Starting Miku bot in standalone mode...")
    run_standalone()

if __name__ == "__main__":
    main()