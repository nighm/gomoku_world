"""
Logging module for the Gomoku World game.

五子棋世界游戏的日志模块。

This module provides logging functionality with:
- File and console output
- Log rotation
- Different log levels
- Formatted log messages

本模块提供以下日志功能：
- 文件和控制台输出
- 日志轮转
- 不同的日志级别
- 格式化的日志消息
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

from ..config import LOG_FORMAT, LOG_LEVEL, LOG_FILE, LOG_DIR

def setup_logging():
    """
    Setup logging configuration.
    
    设置日志配置。
    
    This function:
    - Creates log directory if needed
    - Sets up root logger
    - Configures file handler with rotation
    - Configures console handler
    - Sets log format and level
    
    此函数：
    - 如果需要则创建日志目录
    - 设置根日志记录器
    - 配置带轮转的文件处理器
    - 配置控制台处理器
    - 设置日志格式和级别
    """
    # Create log directory if it doesn't exist / 如果日志目录不存在则创建
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create root logger / 创建根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(LOG_LEVEL)
    
    # Create formatters / 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Create and configure file handler / 创建并配置文件处理器
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024*1024,  # 1MB / 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Create and configure console handler / 创建并配置控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Log initial message / 记录初始消息
    root_logger.info("Logging system initialized / 日志系统已初始化")

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    获取日志记录器实例。
    
    Args:
        name (str): Name of the logger, typically __name__.
                   日志记录器的名称，通常为__name__。
                   
    Returns:
        logging.Logger: Logger instance with the specified name.
                       具有指定名称的日志记录器实例。
    """
    return logging.getLogger(name) 
