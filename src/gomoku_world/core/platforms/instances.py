"""
Global instances for platform
平台全局实例
"""

import platform
from typing import Optional

from .base import PlatformBase
from .windows import WindowsPlatform
from .linux import LinuxPlatform
from .macos import MacOSPlatform
from .web import WebPlatform

def get_platform() -> PlatformBase:
    """
    Get appropriate platform implementation
    获取适当的平台实现
    
    Returns:
        PlatformBase: Platform-specific implementation
    """
    system = platform.system().lower()
    
    if system == 'windows':
        return WindowsPlatform()
    elif system == 'linux':
        return LinuxPlatform()
    elif system == 'darwin':
        return MacOSPlatform()
    else:
        return PlatformBase()  # Fallback to base implementation

# Create global platform instance
PLATFORM = get_platform()

__all__ = ['PLATFORM'] 