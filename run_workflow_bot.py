"""
Special script specifically designed for the run_miku_bot workflow.
This ensures the bot runs in standalone mode without Flask to avoid port conflicts.
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """
    Entry point for the run_miku_bot workflow.
    Force standalone mode to avoid port conflicts.
    """
    print("======================================")
    print("MIKU BOT WORKFLOW RUNNER")
    print("Running in dedicated standalone mode")
    print("======================================")
    
    # Force the environment variable to indicate we're in the workflow
    os.environ['REPL_WORKFLOW'] = 'run_miku_bot'
    
    # Import and run the standalone bot directly
    import standalone_bot
    standalone_bot.run_standalone()

if __name__ == "__main__":
    main()