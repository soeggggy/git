"""
Dedicated script for running ONLY the Miku bot in the run_miku_bot workflow.
This completely skips the Flask app to avoid port conflicts.
"""
import os
import logging
from bot_runner import run_standalone_bot

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

print("=========================================")
print("MIKU BOT STANDALONE RUNNER")
print("Running bot WITHOUT web interface")
print("This avoids port conflicts with other services")
print("=========================================")

# Directly run the standalone bot without any Flask/web components
run_standalone_bot()