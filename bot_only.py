"""
A dedicated standalone script to run only the Telegram bot without the web interface.
This script is specifically designed to be called by the 'run_miku_bot' workflow.
"""
import socket
import logging

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if __name__ == "__main__":
    print("===== Starting Miku Bot in Standalone Mode =====")
    print("This script is designed to run the bot without the web interface")
    
    # Import standalone bot functionality only (no Flask dependencies)
    import standalone_bot
    standalone_bot.run_standalone()