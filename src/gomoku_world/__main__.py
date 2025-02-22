"""
Main entry point for the Gomoku World game.

五子棋世界游戏的主入口点。

This module serves as the main entry point for starting the Gomoku World game.
It initializes logging, creates necessary directories, and launches the game GUI.

本模块作为启动五子棋世界游戏的主入口点。
它初始化日志记录，创建必要的目录，并启动游戏图形界面。
"""

import sys
import logging
from pathlib import Path

from .gui.main_window import GomokuGUI
from .utils.logger import setup_logging
from .config import LOG_DIR

def main():
    """
    Main entry point for the game.
    
    游戏的主入口点。
    
    This function:
    1. Sets up logging configuration
    2. Creates necessary directories
    3. Launches the game GUI
    4. Handles any startup errors
    
    此函数：
    1. 设置日志配置
    2. 创建必要的目录
    3. 启动游戏图形界面
    4. 处理任何启动错误
    """
    # Setup logging / 设置日志
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Create log directory if it doesn't exist / 如果日志目录不存在则创建
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        
        # Start the game / 启动游戏
        logger.info("Starting Gomoku World / 正在启动五子棋世界")
        game = GomokuGUI()
        game.run()
        
    except Exception as e:
        logger.error(f"Error running game / 运行游戏时出错: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
