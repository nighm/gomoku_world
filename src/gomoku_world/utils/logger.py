"""
Logging module
鏃ュ織妯″潡
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from ..config import LOG_FORMAT, LOG_LEVEL, LOG_FILE, LOG_DIR

def setup_logging():
    """
    Setup logging configuration
    璁剧疆鏃ュ織閰嶇疆
    """
    # Create log directory if it doesn't exist
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Create and configure file handler
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Log initial message
    root_logger.info("Logging system initialized")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    鑾峰彇鏃ュ織璁板綍鍣ㄥ疄渚?
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name) 
