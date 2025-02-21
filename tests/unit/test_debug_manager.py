"""
Debug manager unit tests
调试管理器单元测试
"""

import pytest
import time
from gomoku_world.utils.debug.instances import debug_manager

def test_debug_manager_singleton():
    """Test debug manager singleton pattern"""
    from gomoku_world.utils.debug.manager import DebugManager
    
    # Get another instance
    another_manager = DebugManager()
    
    # Should be the same instance
    assert debug_manager is another_manager

def test_debug_manager_toggle_functions():
    """Test debug mode toggle functions"""
    # Test debug mode
    debug_manager.toggle_debug_mode()
    assert debug_manager.debug_mode is True
    debug_manager.toggle_debug_mode()
    assert debug_manager.debug_mode is False
    
    # Test FPS display
    debug_manager.toggle_fps_display()
    assert debug_manager.show_fps is True
    debug_manager.toggle_fps_display()
    assert debug_manager.show_fps is False
    
    # Test grid coordinates
    debug_manager.toggle_grid_coords()
    assert debug_manager.show_grid_coords is True
    debug_manager.toggle_grid_coords()
    assert debug_manager.show_grid_coords is False
    
    # Test debug info
    debug_manager.toggle_debug_info()
    assert debug_manager.show_debug_info is True
    debug_manager.toggle_debug_info()
    assert debug_manager.show_debug_info is False

def test_debug_manager_fps_counter():
    """Test FPS counter functionality"""
    # Reset FPS counter
    debug_manager.frame_count = 0
    debug_manager.last_time = time.time()
    
    # Simulate some frames
    for _ in range(60):
        debug_manager.update_fps()
    
    # Wait for 1 second
    time.sleep(1)
    debug_manager.update_fps()
    
    # FPS should be around 60
    assert 55 <= debug_manager.current_fps <= 65

def test_debug_manager_debug_info():
    """Test debug information updates"""
    # Update debug info
    test_info = {
        'mouse_pos': (100, 100),
        'board_pos': (5, 5),
        'last_move': (7, 7),
        'memory_usage': 1024,
        'frame_time': 16.67
    }
    
    # Set each value
    for key, value in test_info.items():
        debug_manager.debug_info[key] = value
    
    # Check values
    for key, value in test_info.items():
        assert debug_manager.debug_info[key] == value

def test_debug_manager_reset():
    """Test resetting debug manager state"""
    # Enable everything
    debug_manager.debug_mode = True
    debug_manager.show_fps = True
    debug_manager.show_grid_coords = True
    debug_manager.show_debug_info = True
    
    # Reset state
    debug_manager.reset()
    
    # Everything should be disabled
    assert debug_manager.debug_mode is False
    assert debug_manager.show_fps is False
    assert debug_manager.show_grid_coords is False
    assert debug_manager.show_debug_info is False
    assert debug_manager.frame_count == 0
    assert debug_manager.current_fps == 0 