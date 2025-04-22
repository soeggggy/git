"""
Run the web dashboard on port 8080 while the main bot runs on port 5000.
This script should be used by the run_miku_bot workflow.
"""
import logging
import time
from web_dashboard import app

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    """Run the web dashboard on port 8080"""
    print("====================================================")
    print("MIKU BOT WEB DASHBOARD")
    print("Running on port 8080 to avoid conflict with main app")
    print("====================================================")
    
    # Run the web dashboard
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    main()