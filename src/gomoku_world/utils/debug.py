"""
Debug manager module for the Gomoku game.
Provides debugging tools and features.
"""

import logging
import os
import sys
import time
from datetime import datetime
from typing import Dict, Any, Optional
import pygame

class DebugManager:
    """Debug manager class for handling debug features"""
    
    def __init__(self):
        """Initialize debug manager"""
        self.debug_mode = False
        self.show_fps = False
        self.show_grid_coords = False
        self.show_debug_info = False
        self.fps_clock = pygame.time.Clock()
        self.frame_count = 0
        self.last_time = time.time()
        self.current_fps = 0
        
        # Debug information
        self.debug_info: Dict[str, Any] = {
            'mouse_pos': (0, 0),
            'board_pos': (0, 0),
            'last_move': None,
            'memory_usage': 0,
            'frame_time': 0,
        }
    
    def toggle_debug_mode(self):
        """Toggle debug mode"""
        self.debug_mode = not self.debug_mode
        logging.info(f"Debug mode {'enabled' if self.debug_mode else 'disabled'}")
    
    def toggle_fps_display(self):
        """Toggle FPS display"""
        self.show_fps = not self.show_fps
    
    def toggle_grid_coords(self):
        """Toggle grid coordinates display"""
        self.show_grid_coords = not self.show_grid_coords
    
    def toggle_debug_info(self):
        """Toggle debug information display"""
        self.show_debug_info = not self.show_debug_info
    
    def update_fps(self):
        """Update FPS counter"""
        self.frame_count += 1
        current_time = time.time()
        if current_time - self.last_time > 1.0:
            self.current_fps = self.frame_count
            self.frame_count = 0
            self.last_time = current_time
    
    def update_debug_info(self, mouse_pos: tuple, board_pos: tuple, last_move: Optional[tuple]):
        """Update debug information"""
        import psutil
        
        self.debug_info.update({
            'mouse_pos': mouse_pos,
            'board_pos': board_pos,
            'last_move': last_move,
            'memory_usage': psutil.Process().memory_info().rss / 1024 / 1024,  # MB
            'frame_time': self.fps_clock.get_time(),
        })
    
    def draw_debug_overlay(self, screen: pygame.Surface, font: pygame.font.Font):
        """Draw debug information overlay"""
        if not self.debug_mode:
            return
        
        y_offset = 10
        x_pos = 10
        line_height = 20
        
        if self.show_fps:
            fps_text = f"FPS: {self.current_fps}"
            fps_surface = font.render(fps_text, True, (255, 255, 0))
            screen.blit(fps_surface, (x_pos, y_offset))
            y_offset += line_height
        
        if self.show_debug_info:
            debug_lines = [
                f"Mouse: {self.debug_info['mouse_pos']}",
                f"Board: {self.debug_info['board_pos']}",
                f"Last Move: {self.debug_info['last_move']}",
                f"Memory: {self.debug_info['memory_usage']:.1f} MB",
                f"Frame Time: {self.debug_info['frame_time']:.1f} ms",
            ]
            
            for line in debug_lines:
                text_surface = font.render(line, True, (255, 255, 0))
                screen.blit(text_surface, (x_pos, y_offset))
                y_offset += line_height
    
    def save_debug_snapshot(self):
        """Save current debug information to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'debug')
        os.makedirs(debug_dir, exist_ok=True)
        
        filename = os.path.join(debug_dir, f"debug_snapshot_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("=== Gomoku Debug Snapshot ===\n")
            f.write(f"Time: {timestamp}\n")
            f.write(f"Python Version: {sys.version}\n")
            f.write(f"Pygame Version: {pygame.version.ver}\n\n")
            
            f.write("=== Debug Information ===\n")
            for key, value in self.debug_info.items():
                f.write(f"{key}: {value}\n")
            
            f.write("\n=== System Information ===\n")
            import psutil
            memory = psutil.virtual_memory()
            f.write(f"Total Memory: {memory.total / 1024 / 1024:.1f} MB\n")
            f.write(f"Available Memory: {memory.available / 1024 / 1024:.1f} MB\n")
            f.write(f"CPU Usage: {psutil.cpu_percent()}%\n")
        
        logging.info(f"Debug snapshot saved to {filename}")
        return filename 
