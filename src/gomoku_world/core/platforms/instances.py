"""
Platform instance management
"""

import platform
import sys
from typing import Optional

from .base import PlatformBase
from .windows import WindowsPlatform
from .linux import LinuxPlatform
from .macos import MacOSPlatform
from .web import WebPlatform
from ...utils.logger import get_logger

logger = get_logger(__name__)

def get_platform() -> PlatformBase:
    """
    Get appropriate platform implementation
    
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

__all__ = ['get_platform', 'PLATFORM'] 
