"""
Base translation loader interface.

翻译加载器基础接口。
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any

class TranslationLoader(ABC):
    """
    Abstract base class for translation loaders.
    翻译加载器的抽象基类。
    """
    
    @abstractmethod
    def load(self, path: Path) -> Dict[str, Any]:
        """
        Load translations from a file or directory.
        从文件或目录加载翻译。
        
        Args:
            path (Path): Path to translation file or directory
                        翻译文件或目录的路径
            
        Returns:
            Dict[str, Any]: Dictionary of translations
                           翻译字典
            
        Raises:
            FileNotFoundError: If file or directory doesn't exist
                              如果文件或目录不存在
        """
        pass 