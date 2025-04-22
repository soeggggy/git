"""
A dedicated script to start only the bot without any web interface.
This is called by the run_miku_bot workflow.
"""
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
    print("==============================")
    print("Miku Bot Startup Script")
    print("==============================")
    
    # Import and run the standalone bot directly
    print("Starting bot in standalone mode...")
    from standalone_bot import run_standalone
    run_standalone()
    
if __name__ == "__main__":
    main()