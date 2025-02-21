"""
Configuration package for the Gomoku game.
"""

from .settings import *
from .logging_config import setup_logging

# Initialize logging when the config package is imported
setup_logging() 
