"""
Configuration management system.

配置管理系统。

This package provides a unified configuration management system for the Gomoku World project.
Features:
- YAML-based configuration files
- Default configurations for game and i18n
- Dot notation for accessing nested configuration values
- Configuration persistence
- Automatic merging of user configurations with defaults
- Type hints and bilingual documentation

本包为五子棋世界项目提供统一的配置管理系统。
特性：
- 基于YAML的配置文件
- 游戏和国际化的默认配置
- 使用点号表示法访问嵌套配置值
- 配置持久化
- 自动合并用户配置和默认配置
- 类型提示和双语文档
"""

from .base import ConfigManager, game_config, i18n_config

__all__ = ["ConfigManager", "game_config", "i18n_config"]
