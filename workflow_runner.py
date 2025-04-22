#!/usr/bin/env python
"""
IMPORTANT: This is a special script designed ONLY for the run_miku_bot workflow.
It does NOT import Flask or any web components to avoid port conflicts.
"""
import os
import sys
import logging
import socket

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

print("===============================================")
print("MIKU BOT WORKFLOW RUNNER")
print("Running in standalone mode only")
print("===============================================")

# Run the standalone bot implementation directly
# This avoids importing any Flask/web components
from bot_runner import run_standalone_bot
run_standalone_bot()