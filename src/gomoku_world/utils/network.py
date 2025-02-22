"""
Network status monitoring service
网络状态监控服务
"""

import socket
import threading
import time
from typing import List, Optional, Callable
from ..config.settings import NETWORK_CHECK_TIMEOUT, NETWORK_CHECK_HOSTS
from .logger import get_logger

logger = get_logger(__name__)

class NetworkMonitor:
    """Network status monitoring service"""
    
    def __init__(self, check_interval: int = 60):
        """
        Initialize network monitor
        
        Args:
            check_interval: Interval between checks in seconds
        """
        self._is_online = False
        self._check_interval = check_interval
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[bool], None]] = []
        self._lock = threading.Lock()
        
    def start(self):
        """Start network monitoring"""
        if self._monitor_thread is not None:
            return
            
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("Network monitoring started")
        
    def stop(self):
        """Stop network monitoring"""
        if self._monitor_thread is None:
            return
            
        self._stop_event.set()
        self._monitor_thread.join()
        self._monitor_thread = None
        logger.info("Network monitoring stopped")
        
    def add_callback(self, callback: Callable[[bool], None]):
        """
        Add status change callback
        
        Args:
            callback: Callback function receiving online status
        """
        with self._lock:
            self._callbacks.append(callback)
            
    def remove_callback(self, callback: Callable[[bool], None]):
        """
        Remove status change callback
        
        Args:
            callback: Callback function to remove
        """
        with self._lock:
            self._callbacks.remove(callback)
            
    def is_online(self) -> bool:
        """
        Get current online status
        
        Returns:
            bool: True if online
        """
        return self._is_online
        
    def check_connection(self) -> bool:
        """
        Check network connection
        
        Returns:
            bool: True if connection available
        """
        for host in NETWORK_CHECK_HOSTS:
            try:
                # Extract host and port
                if "://" in host:
                    host = host.split("://")[1]
                port = 80 if ":" not in host else int(host.split(":")[1])
                host = host.split(":")[0]
                
                # Try connection
                socket.create_connection((host, port), timeout=NETWORK_CHECK_TIMEOUT)
                return True
            except:
                continue
                
        return False
        
    def _monitor_loop(self):
        """Network monitoring loop"""
        while not self._stop_event.is_set():
            try:
                # Check connection
                is_online = self.check_connection()
                
                # If status changed
                if is_online != self._is_online:
                    self._is_online = is_online
                    logger.info(f"Network status changed: {'online' if is_online else 'offline'}")
                    
                    # Notify callbacks
                    with self._lock:
                        for callback in self._callbacks:
                            try:
                                callback(is_online)
                            except Exception as e:
                                logger.error(f"Error in network status callback: {e}")
                                
            except Exception as e:
                logger.error(f"Error in network monitoring: {e}")
                
            # Wait for next check
            self._stop_event.wait(self._check_interval)
            
# Create global network monitor instance
network_monitor = NetworkMonitor() 