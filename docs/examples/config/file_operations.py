"""
Configuration file operations examples.
配置文件操作示例。

This module demonstrates various operations with configuration files:
- Loading configurations
- Saving configurations
- File format conversion
- Backup and restore
- Error handling

本模块演示配置文件的各种操作：
- 加载配置
- 保存配置
- 文件格式转换
- 备份和恢复
- 错误处理
"""

import os
from pathlib import Path
from datetime import datetime
from gomoku_world.config import game_config
from gomoku_world.config.exceptions import ConfigError, ConfigFileError

def load_config_example():
    """
    Configuration loading examples.
    配置加载示例。
    """
    try:
        # Load from default location / 从默认位置加载
        game_config.load()
        print("Default configuration loaded / 已加载默认配置")
        
        # Load from specific file / 从指定文件加载
        game_config.load_from_file("custom_config.yaml")
        print("Custom configuration loaded / 已加载自定义配置")
        
        # Load with merge / 加载并合并
        game_config.load_from_file("partial_config.yaml", merge=True)
        print("Partial configuration merged / 已合并部分配置")
        
    except ConfigFileError as e:
        print(f"File error / 文件错误: {e}")
    except ConfigError as e:
        print(f"Configuration error / 配置错误: {e}")

def save_config_example():
    """
    Configuration saving examples.
    配置保存示例。
    """
    try:
        # Save to default location / 保存到默认位置
        game_config.save()
        print("Configuration saved / 配置已保存")
        
        # Save to specific file / 保存到指定文件
        game_config.save_to_file("custom_config.yaml")
        print("Configuration saved to custom file / 配置已保存到自定义文件")
        
        # Save with backup / 保存并备份
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"config_backup_{timestamp}.yaml"
        game_config.save_to_file(backup_path)
        print(f"Backup saved to / 备份已保存到: {backup_path}")
        
    except ConfigFileError as e:
        print(f"File error / 文件错误: {e}")
    except ConfigError as e:
        print(f"Configuration error / 配置错误: {e}")

def format_conversion_example():
    """
    Configuration format conversion examples.
    配置格式转换示例。
    """
    try:
        # Convert JSON to YAML / 将JSON转换为YAML
        game_config.load_from_file("old_config.json")
        game_config.save_to_file("new_config.yaml")
        print("Configuration converted from JSON to YAML / 配置已从JSON转换为YAML")
        
        # Export as different formats / 导出为不同格式
        game_config.export_json("config.json")
        game_config.export_yaml("config.yaml")
        print("Configuration exported in multiple formats / 配置已导出为多种格式")
        
    except ConfigError as e:
        print(f"Conversion error / 转换错误: {e}")

def backup_restore_example():
    """
    Configuration backup and restore examples.
    配置备份和恢复示例。
    """
    try:
        # Create backup / 创建备份
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"config_backup_{timestamp}.yaml"
        
        # Save current state / 保存当前状态
        game_config.save_to_file(backup_path)
        print(f"Backup created / 已创建备份: {backup_path}")
        
        # Modify configuration / 修改配置
        game_config.set("game.board.size", 19)
        print("Configuration modified / 配置已修改")
        
        # Restore from backup / 从备份恢复
        game_config.load_from_file(backup_path)
        print("Configuration restored from backup / 已从备份恢复配置")
        
    except ConfigError as e:
        print(f"Backup/restore error / 备份/恢复错误: {e}")

def error_handling_example():
    """
    File operation error handling examples.
    文件操作错误处理示例。
    """
    try:
        # Try to load non-existent file / 尝试加载不存在的文件
        game_config.load_from_file("non_existent.yaml")
        
    except ConfigFileError as e:
        print(f"Expected file error / 预期的文件错误: {e}")
    
    try:
        # Try to save to invalid location / 尝试保存到无效位置
        game_config.save_to_file("/invalid/path/config.yaml")
        
    except ConfigFileError as e:
        print(f"Expected save error / 预期的保存错误: {e}")
    
    try:
        # Try to load invalid format / 尝试加载无效格式
        game_config.load_from_file("invalid_format.txt")
        
    except ConfigError as e:
        print(f"Expected format error / 预期的格式错误: {e}")

def cleanup_example_files():
    """
    Clean up example files.
    清理示例文件。
    """
    files_to_clean = [
        "custom_config.yaml",
        "partial_config.yaml",
        "config_backup_*.yaml",
        "old_config.json",
        "new_config.yaml",
        "config.json",
        "config.yaml"
    ]
    
    for pattern in files_to_clean:
        for file in Path(".").glob(pattern):
            try:
                file.unlink()
                print(f"Cleaned up / 已清理: {file}")
            except Exception as e:
                print(f"Failed to clean / 清理失败: {file} - {e}")

def main():
    """
    Main function demonstrating all examples.
    演示所有示例的主函数。
    """
    print("\n=== Loading Configurations / 加载配置 ===")
    load_config_example()
    
    print("\n=== Saving Configurations / 保存配置 ===")
    save_config_example()
    
    print("\n=== Format Conversion / 格式转换 ===")
    format_conversion_example()
    
    print("\n=== Backup and Restore / 备份和恢复 ===")
    backup_restore_example()
    
    print("\n=== Error Handling / 错误处理 ===")
    error_handling_example()
    
    print("\n=== Cleaning Up / 清理 ===")
    cleanup_example_files()

if __name__ == "__main__":
    main() 