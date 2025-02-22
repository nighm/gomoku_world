"""
Network monitoring and management module.

网络监控和管理模块。
"""

import socket
import threading
import time
import statistics
from typing import List, Optional, Callable, Dict
from ..config.settings import (
    NETWORK_CHECK_TIMEOUT,
    NETWORK_CHECK_HOSTS,
    NETWORK_CHECK_INTERVAL,
    NETWORK_MAX_RETRIES,
    NETWORK_RETRY_DELAY,
    NETWORK_PROXY_SETTINGS
)
from ..utils.logger import get_logger

logger = get_logger(__name__)

class NetworkMonitor:
    """
    Network status monitoring and management class.
    
    网络状态监控和管理类。
    """
    
    def __init__(self, check_interval: int = NETWORK_CHECK_INTERVAL):
        """
        Initialize network monitor.
        
        初始化网络监控器。
        """
        self._is_online = True
        self._check_interval = check_interval
        self._stop_event = threading.Event()
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[bool], None]] = []
        self._lock = threading.Lock()
        self._latencies: Dict[str, List[float]] = {}
        self._proxy = NETWORK_PROXY_SETTINGS if NETWORK_PROXY_SETTINGS.get('enabled') else None
        self._metrics: Dict[str, float] = {
            "latency": 0.0,
            "packet_loss": 0.0,
            "bandwidth": 0.0
        }
        
    def start(self):
        """
        Start network monitoring.
        
        启动网络监控。
        """
        if self._monitor_thread is not None:
            return
            
        self._stop_event.clear()
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        logger.info("Network monitor started / 网络监控已启动")
        
    def stop(self):
        """
        Stop network monitoring.
        
        停止网络监控。
        """
        if self._monitor_thread is None:
            return
            
        self._stop_event.set()
        self._monitor_thread.join()
        self._monitor_thread = None
        logger.info("Network monitor stopped / 网络监控已停止")
        
    def add_callback(self, callback: Callable[[bool], None]):
        """
        Add network status change callback.
        
        添加网络状态变化回调函数。
        """
        with self._lock:
            self._callbacks.append(callback)
            
    def remove_callback(self, callback: Callable[[bool], None]):
        """
        Remove network status change callback.
        
        移除网络状态变化回调函数。
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
        
    def get_connection_quality(self) -> Dict[str, float]:
        """
        Get connection quality metrics
        
        Returns:
            Dict with average latency and jitter
        """
        if not self._latencies:
            return {'latency': float('inf'), 'jitter': float('inf')}
            
        # Calculate average latency across all hosts
        all_latencies = []
        for host_latencies in self._latencies.values():
            if host_latencies:
                all_latencies.extend(host_latencies)
                
        if not all_latencies:
            return {'latency': float('inf'), 'jitter': float('inf')}
            
        avg_latency = statistics.mean(all_latencies)
        jitter = statistics.stdev(all_latencies) if len(all_latencies) > 1 else 0
        
        return {
            'latency': avg_latency,
            'jitter': jitter
        }
        
    def check_connection(self) -> bool:
        """
        Check network connection with retries
        
        Returns:
            bool: True if connection available
        """
        for attempt in range(NETWORK_MAX_RETRIES):
            if attempt > 0:
                time.sleep(NETWORK_RETRY_DELAY)
                
            for host in NETWORK_CHECK_HOSTS:
                try:
                    # Extract host and port
                    if "://" in host:
                        host = host.split("://")[1]
                    port = 80 if ":" not in host else int(host.split(":")[1])
                    host = host.split(":")[0]
                    
                    # Create socket with timeout
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(NETWORK_CHECK_TIMEOUT)
                    
                    # Apply proxy settings if configured
                    if self._proxy and self._proxy.get('enabled'):
                        proxy_host = self._proxy['host']
                        proxy_port = self._proxy['port']
                        sock.connect((proxy_host, proxy_port))
                        # Send CONNECT request through proxy
                        connect_str = f"CONNECT {host}:{port} HTTP/1.1\r\n\r\n"
                        sock.send(connect_str.encode())
                        response = sock.recv(4096)
                        if not response.startswith(b"HTTP/1.1 200"):
                            continue
                    else:
                        # Direct connection
                        start_time = time.time()
                        sock.connect((host, port))
                        latency = time.time() - start_time
                        
                        # Update latency measurements
                        with self._lock:
                            if host not in self._latencies:
                                self._latencies[host] = []
                            self._latencies[host].append(latency)
                            # Keep only recent measurements
                            self._latencies[host] = self._latencies[host][-10:]
                            
                    sock.close()
                    return True
                except Exception as e:
                    logger.debug(f"Connection attempt {attempt + 1} to {host} failed: {e}")
                    continue
                    
        return False
        
    def get_metrics(self) -> Dict[str, float]:
        """
        Get current network metrics.
        
        获取当前网络指标。
        """
        return self._metrics.copy()
        
    def _monitor_loop(self):
        """
        Main monitoring loop.
        
        主监控循环。
        """
        while not self._stop_event.is_set():
            try:
                # Check connection
                is_online = self.check_connection()
                
                # If status changed
                if is_online != self._is_online:
                    self._is_online = is_online
                    logger.info(f"Network status changed: {'online' if is_online else 'offline'}")
                    
                    # Get connection quality if online
                    if is_online:
                        quality = self.get_connection_quality()
                        logger.info(f"Connection quality - Latency: {quality['latency']:.2f}ms, Jitter: {quality['jitter']:.2f}ms")
                    
                    # Notify callbacks
                    with self._lock:
                        for callback in self._callbacks:
                            try:
                                callback(is_online)
                            except Exception as e:
                                logger.error(f"Error in network status callback: {e}")
                                
                # Update metrics / 更新指标
                self._update_metrics()
                
            except Exception as e:
                logger.error(f"Network monitoring error / 网络监控错误: {e}")
                
            # Wait for next check
            self._stop_event.wait(self._check_interval)
        
    def _update_metrics(self):
        """
        Update network performance metrics.
        
        更新网络性能指标。
        """
        # Implementation here / 在此实现
        pass
        
    def _notify_callbacks(self):
        """
        Notify all registered callbacks of status change.
        
        通知所有已注册的回调函数状态变化。
        """
        for callback in self._callbacks:
            try:
                callback(self._is_online)
            except Exception as e:
                logger.error(f"Callback error / 回调错误: {e}")

# Global instance / 全局实例
network_monitor = NetworkMonitor()

__all__ = ['network_monitor'] 