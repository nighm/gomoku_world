"""
Global instances for resource management
资源管理全局实例
"""

from .manager import ResourceManager
from .loader import ResourceLoader

# Create global instances
resource_manager = ResourceManager()
resource_loader = ResourceLoader()

__all__ = [
    'resource_manager',
    'resource_loader'
] 