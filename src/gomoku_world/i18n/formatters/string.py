"""
String formatter implementation.

字符串格式化器实现。

This module provides string formatting implementations:
- DefaultFormatter: Uses Python's str.format()
- SafeFormatter: Adds error handling and fallback
- NamedFormatter: Supports named format arguments only

本模块提供字符串格式化实现：
- DefaultFormatter：使用Python的str.format()
- SafeFormatter：添加错误处理和回退
- NamedFormatter：仅支持命名格式参数
"""

import logging
from typing import Any, Dict, Optional
from ..base import StringFormatter
from ..exceptions import FormatterError

logger = logging.getLogger(__name__)

class DefaultFormatter(StringFormatter):
    """
    Default string formatter using Python's str.format().
    使用Python的str.format()的默认字符串格式化器。
    """
    
    def format(self, template: str, **kwargs: Any) -> str:
        """
        Format a string using Python's str.format().
        使用Python的str.format()格式化字符串。
        
        Args:
            template (str): String template to format
                          要格式化的字符串模板
            **kwargs: Format arguments
                     格式化参数
            
        Returns:
            str: Formatted string
                 格式化后的字符串
                 
        Raises:
            FormatterError: If formatting fails
                           如果格式化失败
        """
        try:
            return template.format(**kwargs)
        except Exception as e:
            logger.error(f"Formatting error: {e}")
            raise FormatterError(template, kwargs, str(e))

class SafeFormatter(StringFormatter):
    """
    Safe string formatter with error handling and fallback.
    具有错误处理和回退的安全字符串格式化器。
    """
    
    def __init__(self, fallback_template: Optional[str] = None):
        """
        Initialize safe formatter.
        初始化安全格式化器。
        
        Args:
            fallback_template (Optional[str]): Template to use when formatting fails
                                             格式化失败时使用的模板
        """
        self._fallback = fallback_template
        
    def format(self, template: str, **kwargs: Any) -> str:
        """
        Safely format a string with fallback.
        安全地格式化字符串，具有回退机制。
        
        Args:
            template (str): String template to format
                          要格式化的字符串模板
            **kwargs: Format arguments
                     格式化参数
            
        Returns:
            str: Formatted string or fallback
                 格式化后的字符串或回退值
        """
        try:
            return template.format(**kwargs)
        except Exception as e:
            logger.warning(f"Formatting failed: {e}")
            if self._fallback:
                try:
                    return self._fallback.format(**kwargs)
                except Exception:
                    pass
            return template

class NamedFormatter(StringFormatter):
    """
    Formatter that only supports named format arguments.
    仅支持命名格式参数的格式化器。
    """
    
    def format(self, template: str, **kwargs: Any) -> str:
        """
        Format a string using only named arguments.
        仅使用命名参数格式化字符串。
        
        Args:
            template (str): String template to format
                          要格式化的字符串模板
            **kwargs: Named format arguments
                     命名格式化参数
            
        Returns:
            str: Formatted string
                 格式化后的字符串
                 
        Raises:
            FormatterError: If formatting fails or positional args are used
                           如果格式化失败或使用了位置参数
        """
        try:
            # Check for positional arguments in template
            if "{}" in template:
                raise ValueError("Positional arguments are not supported")
            return template.format(**kwargs)
        except Exception as e:
            logger.error(f"Named formatting error: {e}")
            raise FormatterError(template, kwargs, str(e)) 