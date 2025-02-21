"""
Global instances for networking
缃戠粶鍏ㄥ眬瀹炰緥
"""

from .network import NetworkManager

# Create global instance
network_manager = NetworkManager()

__all__ = ['network_manager'] 
