"""
Centralized imports management
涓績鍖栧鍏ョ鐞?
"""

import os
import importlib
from typing import Dict, Any, Optional

class ImportManager:
    """
    Manages dynamic imports for the project
    绠＄悊椤圭洰鐨勫姩鎬佸鍏?
    """
    
    _instance = None
    _modules: Dict[str, Any] = {}
    _package_name = "gomoku_world"  # Default package name
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_package_name(cls, name: str):
        """
        Set the package name
        璁剧疆鍖呭悕
        
        Args:
            name: New package name
        """
        cls._package_name = name
    
    @classmethod
    def get_package_name(cls) -> str:
        """
        Get the current package name
        鑾峰彇褰撳墠鍖呭悕
        
        Returns:
            str: Current package name
        """
        return cls._package_name
    
    @classmethod
    def import_module(cls, module_path: str) -> Optional[Any]:
        """
        Dynamically import a module
        鍔ㄦ佸鍏ユā鍧?
        
        Args:
            module_path: Relative module path (e.g. 'core.game')
            
        Returns:
            Optional[Any]: Imported module or None if import fails
        """
        if module_path in cls._modules:
            return cls._modules[module_path]
            
        try:
            full_path = f"{cls._package_name}.{module_path}"
            module = importlib.import_module(full_path)
            cls._modules[module_path] = module
            return module
        except ImportError as e:
            print(f"Error importing {module_path}: {e}")
            return None
    
    @classmethod
    def get_class(cls, module_path: str, class_name: str) -> Optional[type]:
        """
        Get a class from a module
        浠庢ā鍧椾腑鑾峰彇绫?
        
        Args:
            module_path: Relative module path
            class_name: Name of the class
            
        Returns:
            Optional[type]: Class type or None if not found
        """
        module = cls.import_module(module_path)
        if module and hasattr(module, class_name):
            return getattr(module, class_name)
        return None
    
    @classmethod
    def clear_cache(cls):
        """
        Clear the module cache
        娓呴櫎妯″潡缂撳瓨
        """
        cls._modules.clear()

# Create a global instance
import_manager = ImportManager() 
