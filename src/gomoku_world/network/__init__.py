"""
Network module
网络模块
"""

from .network import NetworkManager
from .errors import NetworkError, ConnectionError, MessageError
from .instances import network_manager

__all__ = [
    # Classes
    'NetworkManager',
    'NetworkError',
    'ConnectionError',
    'MessageError',
    # Global instances
    'network_manager'
]
