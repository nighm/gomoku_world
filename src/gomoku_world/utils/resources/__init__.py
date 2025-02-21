"""
Resource management module
"""

from .manager import ResourceManager

# Create a global resource manager instance
resource_manager = ResourceManager()

__all__ = ['resource_manager'] 
