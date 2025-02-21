"""
Global instances for resource management
璧勬簮绠＄悊鍏ㄥ眬瀹炰緥
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
