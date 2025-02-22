"""
Game configuration tests.

游戏配置测试。
"""

import pytest
from pathlib import Path
import yaml

from gomoku_world.config import game_config
from gomoku_world.config.exceptions import ConfigValueError

def test_game_board_settings():
    """
    Test game board configuration settings.
    测试游戏棋盘配置设置。
    """
    # Test board size / 测试棋盘大小
    assert game_config.get("board.size") == 15
    assert game_config.get("board.win_count") == 5
    
    # Test invalid board size / 测试无效的棋盘大小
    with pytest.raises(ConfigValueError):
        game_config.set("board.size", 8)  # Too small
    with pytest.raises(ConfigValueError):
        game_config.set("board.size", 30)  # Too large

def test_game_ai_settings():
    """
    Test AI configuration settings.
    测试AI配置设置。
    """
    # Test AI difficulty / 测试AI难度
    assert game_config.get("ai.difficulty") in ["easy", "medium", "hard"]
    
    # Test invalid AI difficulty / 测试无效的AI难度
    with pytest.raises(ConfigValueError):
        game_config.set("ai.difficulty", "impossible")
    
    # Test AI search depth / 测试AI搜索深度
    assert isinstance(game_config.get("ai.search_depth"), int)
    assert game_config.get("ai.search_depth") > 0

def test_game_display_settings():
    """
    Test display configuration settings.
    测试显示配置设置。
    """
    # Test theme settings / 测试主题设置
    assert game_config.get("display.theme") in ["light", "dark"]
    
    # Test animation settings / 测试动画设置
    assert isinstance(game_config.get("display.animations_enabled"), bool)
    
    # Test window size / 测试窗口大小
    window_size = game_config.get("display.window_size")
    assert isinstance(window_size["width"], int)
    assert isinstance(window_size["height"], int)

def test_game_sound_settings():
    """
    Test sound configuration settings.
    测试声音配置设置。
    """
    # Test sound volume / 测试声音音量
    assert 0 <= game_config.get("sound.volume") <= 100
    
    # Test invalid volume / 测试无效的音量
    with pytest.raises(ConfigValueError):
        game_config.set("sound.volume", 101)
    with pytest.raises(ConfigValueError):
        game_config.set("sound.volume", -1)
    
    # Test sound enabled setting / 测试声音启用设置
    assert isinstance(game_config.get("sound.enabled"), bool)

def test_game_debug_settings():
    """
    Test debug configuration settings.
    测试调试配置设置。
    """
    # Test debug mode / 测试调试模式
    assert isinstance(game_config.get("debug.enabled"), bool)
    
    # Test log level / 测试日志级别
    assert game_config.get("debug.log_level") in ["DEBUG", "INFO", "WARNING", "ERROR"]
    
    # Test invalid log level / 测试无效的日志级别
    with pytest.raises(ConfigValueError):
        game_config.set("debug.log_level", "INVALID")

def test_game_config_persistence(tmp_path):
    """
    Test game configuration persistence.
    测试游戏配置持久化。
    """
    # Save current config / 保存当前配置
    config_file = tmp_path / "game.yaml"
    game_config.export(config_file)
    
    # Modify some settings / 修改一些设置
    original_theme = game_config.get("display.theme")
    game_config.set("display.theme", "dark" if original_theme == "light" else "light")
    
    # Reset config / 重置配置
    game_config.reset()
    
    # Verify reset / 验证重置
    assert game_config.get("display.theme") == original_theme

def test_game_config_validation():
    """
    Test game configuration validation.
    测试游戏配置验证。
    """
    # Test board size validation / 测试棋盘大小验证
    with pytest.raises(ConfigValueError):
        game_config.set("board.size", "invalid")
    
    # Test AI difficulty validation / 测试AI难度验证
    with pytest.raises(ConfigValueError):
        game_config.set("ai.difficulty", 123)
    
    # Test theme validation / 测试主题验证
    with pytest.raises(ConfigValueError):
        game_config.set("display.theme", "invalid_theme")
    
    # Test volume validation / 测试音量验证
    with pytest.raises(ConfigValueError):
        game_config.set("sound.volume", "full") 