"""
conftest.py – Pytest configuration.

This file is automatically loaded by pytest. We use it to add the project
root directory to sys.path so that "from utils.api_client import ..."
works regardless of how pytest is invoked.
"""

import sys
import os

# Add the project root to Python's import path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
