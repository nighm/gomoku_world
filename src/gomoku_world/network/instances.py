"""
Global instances for networking
网络全局实例
"""

from .network import NetworkManager

# Create global instance
network_manager = NetworkManager()

__all__ = ['network_manager'] 