"""
Platform-specific implementations
平台特定实现
"""

import platform
import sys
from typing import Optional

from .base import PlatformBase
from .windows import WindowsPlatform
from .linux import LinuxPlatform
from .macos import MacOSPlatform
from .web import WebPlatform
from .instances import PLATFORM

__all__ = [
    'PlatformBase',
    'WindowsPlatform',
    'LinuxPlatform',
    'MacOSPlatform',
    'WebPlatform',
    'get_platform',
    'PLATFORM'
]

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