"""
Logging configuration for the Gomoku game.
"""

import os
import logging.config
from datetime import datetime
from .settings import LOG_LEVEL, LOG_FORMAT

# Create logs directory if it doesn't exist
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOGS_DIR, exist_ok=True)

# Generate log filename with timestamp
LOG_FILENAME = f"gomoku_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
LOG_FILE_PATH = os.path.join(LOGS_DIR, LOG_FILENAME)

# Logging configuration dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        },
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.FileHandler',
            'filename': LOG_FILE_PATH,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': LOG_LEVEL,
            'propagate': True
        },
    }
}

def setup_logging():
    """Configure logging settings for the application"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.info("Logging system initialized") 