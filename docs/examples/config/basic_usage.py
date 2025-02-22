"""
Basic usage examples of the configuration system.
配置系统基本用法示例。

This module demonstrates the basic operations of the configuration system:
- Initialization
- Getting and setting values
- Using dot notation
- Configuration validation
- Error handling

本模块演示配置系统的基本操作：
- 初始化
- 获取和设置值
- 使用点号表示法
- 配置验证
- 错误处理
"""

from gomoku_world.config import game_config, ConfigValidator
from gomoku_world.config.exceptions import ConfigError, ConfigValueError

def basic_operations():
    """
    Basic configuration operations.
    基本配置操作。
    """
    try:
        # Get configuration value / 获取配置值
        board_size = game_config.get("game.board.size")
        print(f"Board size / 棋盘大小: {board_size}")
        
        # Set configuration value / 设置配置值
        game_config.set("game.board.size", 19)
        print(f"New board size / 新棋盘大小: {game_config.get('game.board.size')}")
        
        # Get with default value / 使用默认值获取
        theme = game_config.get("game.display.theme", default="light")
        print(f"Theme / 主题: {theme}")
        
        # Update multiple values / 更新多个值
        game_config.update({
            "game.display.theme": "dark",
            "game.sound.volume": 80
        })
        print("Configuration updated / 配置已更新")
        
    except ConfigError as e:
        print(f"Configuration error / 配置错误: {e}")

def validation_example():
    """
    Configuration validation example.
    配置验证示例。
    """
    validator = ConfigValidator()
    
    try:
        # Validate single value / 验证单个值
        result = validator.validate_value("game.board.size", 15)
        if result.is_valid:
            print("Valid board size / 有效的棋盘大小")
        else:
            print(f"Invalid board size / 无效的棋盘大小: {result.errors}")
        
        # Validate entire configuration / 验证整个配置
        result = validator.validate_config(game_config.to_dict())
        if result.is_valid:
            print("Configuration is valid / 配置有效")
        else:
            print(f"Configuration errors / 配置错误: {result.errors}")
            
    except ConfigValueError as e:
        print(f"Validation error / 验证错误: {e}")

def error_handling():
    """
    Error handling examples.
    错误处理示例。
    """
    try:
        # Try to get non-existent key / 尝试获取不存在的键
        value = game_config.get("non.existent.key")
        
    except ConfigError as e:
        print(f"Expected error / 预期的错误: {e}")
    
    try:
        # Try to set invalid value / 尝试设置无效的值
        game_config.set("game.board.size", "invalid")
        
    except ConfigValueError as e:
        print(f"Expected validation error / 预期的验证错误: {e}")

def reset_example():
    """
    Configuration reset example.
    配置重置示例。
    """
    # Save current value / 保存当前值
    old_size = game_config.get("game.board.size")
    
    # Change value / 更改值
    game_config.set("game.board.size", 19)
    
    # Reset configuration / 重置配置
    game_config.reset()
    
    # Verify reset / 验证重置
    new_size = game_config.get("game.board.size")
    print(f"Original size / 原始大小: {old_size}")
    print(f"After reset / 重置后: {new_size}")

def main():
    """
    Main function demonstrating all examples.
    演示所有示例的主函数。
    """
    print("\n=== Basic Operations / 基本操作 ===")
    basic_operations()
    
    print("\n=== Validation / 验证 ===")
    validation_example()
    
    print("\n=== Error Handling / 错误处理 ===")
    error_handling()
    
    print("\n=== Reset Example / 重置示例 ===")
    reset_example()

 