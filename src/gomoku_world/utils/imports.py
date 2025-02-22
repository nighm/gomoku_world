"""
Import management module for the Gomoku World game.

五子棋世界游戏的导入管理模块。

This module provides centralized import management:
- Dynamic module loading
- Class importing
- Import caching
- Package management
- Error handling

本模块提供集中的导入管理：
- 动态模块加载
- 类导入
- 导入缓存
- 包管理
- 错误处理
"""

import os
import importlib
import sys
from typing import Dict, Any, Optional, Type
from pathlib import Path

from .logger import get_logger

logger = get_logger(__name__)

class ImportManager:
    """
    Import manager for handling dynamic module loading.
    
    动态模块加载的导入管理器。
    
    This class provides:
    - Dynamic module importing
    - Class loading
    - Import caching
    - Package configuration
    - Error handling
    
    此类提供：
    - 动态模块导入
    - 类加载
    - 导入缓存
    - 包配置
    - 错误处理
    """
    
    _instance = None
    _modules: Dict[str, Any] = {}
    _package_name = "gomoku_world"  # Default package name / 默认包名
    
    def __new__(cls):
        """
        Create or return the singleton instance.
        
        创建或返回单例实例。
        
        Returns:
            ImportManager: Singleton instance.
                         单例实例。
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_package_name(cls, name: str):
        """
        Set the base package name.
        
        设置基础包名。
        
        Args:
            name (str): New package name.
                       新的包名。
                       
        Raises:
            ValueError: If package name is invalid.
                       如果包名无效。
        """
        if not name or not isinstance(name, str):
            raise ValueError("Invalid package name / 无效的包名")
        cls._package_name = name
        logger.info(f"Package name set to: {name} / 包名已设置为：{name}")
    
    @classmethod
    def get_package_name(cls) -> str:
        """
        Get the current package name.
        
        获取当前包名。
        
        Returns:
            str: Current package name.
                 当前包名。
        """
        return cls._package_name
    
    @classmethod
    def import_module(cls, module_path: str) -> Optional[Any]:
        """
        Dynamically import a module.
        
        动态导入模块。
        
        Args:
            module_path (str): Relative module path (e.g. 'core.game').
                             相对模块路径（例如'core.game'）。
                             
        Returns:
            Optional[Any]: Imported module or None if import fails.
                          导入的模块，如果导入失败则为None。
                          
        Example:
            >>> game_module = ImportManager.import_module('core.game')
            >>> game = game_module.Game()
        """
        try:
            # Check cache first / 首先检查缓存
            if module_path in cls._modules:
                return cls._modules[module_path]
            
            # Import module / 导入模块
            full_path = f"{cls._package_name}.{module_path}"
            module = importlib.import_module(full_path)
            
            # Cache the module / 缓存模块
            cls._modules[module_path] = module
            logger.info(f"Successfully imported module: {module_path} / "
                       f"成功导入模块：{module_path}")
            
            return module
            
        except ImportError as e:
            logger.error(f"Failed to import module {module_path}: {e} / "
                        f"导入模块{module_path}失败：{e}")
            return None
    
    @classmethod
    def get_class(cls, module_path: str, class_name: str) -> Optional[Type]:
        """
        Get a class from a module.
        
        从模块中获取类。
        
        Args:
            module_path (str): Relative module path.
                             相对模块路径。
            class_name (str): Name of the class to import.
                            要导入的类名。
                            
        Returns:
            Optional[Type]: Class type or None if not found.
                           类型，如果未找到则为None。
                           
        Example:
            >>> Game = ImportManager.get_class('core.game', 'Game')
            >>> game = Game()
        """
        module = cls.import_module(module_path)
        if module is None:
            return None
            
        try:
            class_type = getattr(module, class_name)
            logger.info(f"Successfully loaded class: {class_name} from {module_path} / "
                       f"成功从{module_path}加载类：{class_name}")
            return class_type
        except AttributeError as e:
            logger.error(f"Class {class_name} not found in {module_path}: {e} / "
                        f"在{module_path}中未找到类{class_name}：{e}")
            return None
    
    @classmethod
    def clear_cache(cls):
        """
        Clear the module import cache.
        
        清除模块导入缓存。
        
        This can be useful for:
        - Reloading modified modules
        - Freeing memory
        - Debugging
        
        这对以下情况有用：
        - 重新加载修改的模块
        - 释放内存
        - 调试
        """
        cls._modules.clear()
        logger.info("Import cache cleared / 导入缓存已清除")
    
    @classmethod
    def reload_module(cls, module_path: str) -> Optional[Any]:
        """
        Reload a previously imported module.
        
        重新加载之前导入的模块。
        
        Args:
            module_path (str): Relative module path.
                             相对模块路径。
                             
        Returns:
            Optional[Any]: Reloaded module or None if reload fails.
                          重新加载的模块，如果重新加载失败则为None。
        """
        try:
            if module_path in cls._modules:
                module = cls._modules[module_path]
                reloaded_module = importlib.reload(module)
                cls._modules[module_path] = reloaded_module
                logger.info(f"Successfully reloaded module: {module_path} / "
                           f"成功重新加载模块：{module_path}")
                return reloaded_module
            else:
                return cls.import_module(module_path)
                
        except Exception as e:
            logger.error(f"Failed to reload module {module_path}: {e} / "
                        f"重新加载模块{module_path}失败：{e}")
            return None

# Create global import manager instance / 创建全局导入管理器实例
import_manager = ImportManager()

__all__ = ['import_manager', 'ImportManager'] 
