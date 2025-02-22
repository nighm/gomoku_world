"""
Debug management module for the Gomoku World game.

五子棋世界游戏的调试管理模块。

This module provides debugging functionality:
- Performance monitoring (FPS, memory)
- Visual debugging aids
- Debug information display
- Debug mode controls
- Debug snapshot creation

本模块提供调试功能：
- 性能监控（帧率、内存）
- 可视化调试辅助
- 调试信息显示
- 调试模式控制
- 调试快照创建
"""

import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import pygame
from pathlib import Path

from ..config import DEBUG_DIR
from .logger import get_logger

logger = get_logger(__name__)

class DebugManager:
    """
    Debug manager for handling debugging features.
    
    调试管理器，用于处理调试功能。
    
    This class provides:
    - FPS monitoring and display
    - Grid coordinate visualization
    - Memory usage tracking
    - Debug information overlay
    - Debug snapshot creation
    
    此类提供：
    - 帧率监控和显示
    - 网格坐标可视化
    - 内存使用跟踪
    - 调试信息叠加层
    - 调试快照创建
    """
    
    def __init__(self):
        """
        Initialize the debug manager.
        
        初始化调试管理器。
        
        Sets up:
        - Debug flags
        - Performance monitors
        - Debug information storage
        - Display settings
        
        设置：
        - 调试标志
        - 性能监视器
        - 调试信息存储
        - 显示设置
        """
        self.debug_mode = False
        self.show_fps = False
        self.show_grid_coords = False
        self.show_debug_info = False
        self.fps_clock = pygame.time.Clock()
        self.frame_count = 0
        self.last_time = time.time()
        self.current_fps = 0
        
        # Debug information / 调试信息
        self.debug_info: Dict[str, Any] = {
            'mouse_pos': (0, 0),  # Mouse position / 鼠标位置
            'board_pos': (0, 0),  # Board coordinates / 棋盘坐标
            'last_move': None,    # Last game move / 最后一步
            'memory_usage': 0,    # Memory usage in MB / 内存使用（MB）
            'frame_time': 0,      # Frame processing time / 帧处理时间
            'game_state': None,   # Current game state / 当前游戏状态
            'network_status': None  # Network connection status / 网络连接状态
        }
        
        # Create debug directory / 创建调试目录
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.info("Debug manager initialized / 调试管理器已初始化")
    
    def toggle_debug_mode(self):
        """
        Toggle debug mode on/off.
        
        切换调试模式开/关。
        """
        self.debug_mode = not self.debug_mode
        logger.info(f"Debug mode {'enabled' if self.debug_mode else 'disabled'} / "
                   f"调试模式已{'启用' if self.debug_mode else '禁用'}")
    
    def toggle_fps_display(self):
        """
        Toggle FPS display on/off.
        
        切换帧率显示开/关。
        """
        self.show_fps = not self.show_fps
        logger.info(f"FPS display {'enabled' if self.show_fps else 'disabled'} / "
                   f"帧率显示已{'启用' if self.show_fps else '禁用'}")
    
    def toggle_grid_coords(self):
        """
        Toggle grid coordinate display on/off.
        
        切换网格坐标显示开/关。
        """
        self.show_grid_coords = not self.show_grid_coords
        logger.info(f"Grid coordinates {'enabled' if self.show_grid_coords else 'disabled'} / "
                   f"网格坐标已{'启用' if self.show_grid_coords else '禁用'}")
    
    def toggle_debug_info(self):
        """
        Toggle debug information overlay on/off.
        
        切换调试信息叠加层开/关。
        """
        self.show_debug_info = not self.show_debug_info
        logger.info(f"Debug info {'enabled' if self.show_debug_info else 'disabled'} / "
                   f"调试信息已{'启用' if self.show_debug_info else '禁用'}")
    
    def update_fps(self):
        """
        Update FPS counter.
        
        更新帧率计数器。
        """
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time > 1.0:
            self.current_fps = self.frame_count / (current_time - self.last_time)
            self.frame_count = 0
            self.last_time = current_time
    
    def update_debug_info(self, mouse_pos: Tuple[int, int], board_pos: Tuple[int, int], 
                         last_move: Optional[Tuple[int, int]]):
        """
        Update debug information.
        
        更新调试信息。
        
        Args:
            mouse_pos (Tuple[int, int]): Current mouse position.
                                       当前鼠标位置。
            board_pos (Tuple[int, int]): Current board coordinates.
                                       当前棋盘坐标。
            last_move (Optional[Tuple[int, int]]): Last move coordinates.
                                                 最后一步坐标。
        """
        self.debug_info.update({
            'mouse_pos': mouse_pos,
            'board_pos': board_pos,
            'last_move': last_move,
            'memory_usage': self._get_memory_usage(),
            'frame_time': 1000 / self.current_fps if self.current_fps > 0 else 0
        })
    
    def draw_debug_overlay(self, screen: pygame.Surface, font: pygame.font.Font):
        """
        Draw debug information overlay.
        
        绘制调试信息叠加层。
        
        Args:
            screen (pygame.Surface): Game screen surface.
                                   游戏屏幕表面。
            font (pygame.font.Font): Font for debug text.
                                   调试文本字体。
        """
        if not self.debug_mode:
            return
            
        y_offset = 10
        text_color = (255, 255, 0)  # Yellow / 黄色
        
        # Draw FPS / 绘制帧率
        if self.show_fps:
            fps_text = f"FPS: {self.current_fps:.1f}"
            fps_surface = font.render(fps_text, True, text_color)
            screen.blit(fps_surface, (10, y_offset))
            y_offset += 20
        
        # Draw debug info / 绘制调试信息
        if self.show_debug_info:
            for key, value in self.debug_info.items():
                info_text = f"{key}: {value}"
                info_surface = font.render(info_text, True, text_color)
                screen.blit(info_surface, (10, y_offset))
                y_offset += 20
    
    def save_debug_snapshot(self):
        """
        Save current debug information to a file.
        
        将当前调试信息保存到文件。
        
        Creates a timestamped file containing:
        - System information
        - Game state
        - Debug metrics
        - Error logs
        
        创建包含以下内容的带时间戳的文件：
        - 系统信息
        - 游戏状态
        - 调试指标
        - 错误日志
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            snapshot_file = DEBUG_DIR / f"debug_snapshot_{timestamp}.txt"
            
            with open(snapshot_file, "w", encoding="utf-8") as f:
                # Write system info / 写入系统信息
                f.write("=== System Information / 系统信息 ===\n")
                f.write(f"Python version / Python版本: {sys.version}\n")
                f.write(f"Pygame version / Pygame版本: {pygame.version.ver}\n")
                f.write(f"Platform / 平台: {sys.platform}\n\n")
                
                # Write debug info / 写入调试信息
                f.write("=== Debug Information / 调试信息 ===\n")
                for key, value in self.debug_info.items():
                    f.write(f"{key}: {value}\n")
                
            logger.info(f"Debug snapshot saved to {snapshot_file} / "
                       f"调试快照已保存到{snapshot_file}")
            
        except Exception as e:
            logger.error(f"Failed to save debug snapshot: {e} / "
                        f"保存调试快照失败：{e}")
    
    def _get_memory_usage(self) -> float:
        """
        Get current memory usage in MB.
        
        获取当前内存使用量（MB）。
        
        Returns:
            float: Memory usage in megabytes.
                  内存使用量（兆字节）。
        """
        try:
            import psutil
            process = psutil.Process(os.getpid())
            return process.memory_info().rss / 1024 / 1024  # Convert to MB / 转换为MB
        except ImportError:
            return 0.0

# Create global debug manager instance / 创建全局调试管理器实例
debug_manager = DebugManager()

__all__ = ['debug_manager', 'DebugManager'] 
