"""
Network monitoring and management module.

网络监控和管理模块。

This module provides network status monitoring and management functionality:
- Real-time connection status monitoring
- Connection quality metrics
- Network event callbacks
- Automatic reconnection handling

本模块提供网络状态监控和管理功能：
- 实时连接状态监控
- 连接质量指标
- 网络事件回调
- 自动重连处理
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
    Network monitoring class.
    
    网络监控类。
    
    This class provides:
    - Connection status monitoring
    - Network quality metrics
    - Event callbacks for status changes
    - Automatic reconnection handling
    
    此类提供：
    - 连接状态监控
    - 网络质量指标
    - 状态变化事件回调
    - 自动重连处理
    """
    
    def __init__(self, check_interval: int = NETWORK_CHECK_INTERVAL):
        """
        Initialize network monitor.
        
        初始化网络监控器。
        
        Args:
            check_interval (int): Interval between connection checks in seconds.
                                连接检查间隔（秒）。
        """
        self._check_interval = check_interval
        self._is_running = False
        self._is_online = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._callbacks: List[Callable[[bool], None]] = []
        self._metrics: Dict[str, float] = {
            "latency": 0.0,
            "packet_loss": 0.0,
            "uptime": 0.0
        }
        self._last_check_time = 0.0
        
    def start(self):
        """
        Start network monitoring.
        
        启动网络监控。
        
        This method:
        - Starts the monitoring thread
        - Initializes connection checks
        - Begins collecting metrics
        
        此方法：
        - 启动监控线程
        - 初始化连接检查
        - 开始收集指标
        """
        if not self._is_running:
            self._is_running = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop)
            self._monitor_thread.daemon = True
            self._monitor_thread.start()
            logger.info("Network monitoring started / 网络监控已启动")
            
    def stop(self):
        """
        Stop network monitoring.
        
        停止网络监控。
        
        This method:
        - Stops the monitoring thread
        - Cleans up resources
        - Notifies callbacks
        
        此方法：
        - 停止监控线程
        - 清理资源
        - 通知回调函数
        """
        if self._is_running:
            self._is_running = False
            if self._monitor_thread:
                self._monitor_thread.join()
            self._monitor_thread = None
            logger.info("Network monitoring stopped / 网络监控已停止")
            
    def add_callback(self, callback: Callable[[bool], None]):
        """
        Add a status change callback.
        
        添加状态变化回调。
        
        Args:
            callback: Function to call when network status changes.
                     当网络状态改变时调用的函数。
        """
        if callback not in self._callbacks:
            self._callbacks.append(callback)
            
    def remove_callback(self, callback: Callable[[bool], None]):
        """
        Remove a status change callback.
        
        移除状态变化回调。
        
        Args:
            callback: Callback function to remove.
                     要移除的回调函数。
        """
        if callback in self._callbacks:
            self._callbacks.remove(callback)
            
    def is_online(self) -> bool:
        """
        Get current online status.
        
        获取当前在线状态。
        
        Returns:
            bool: True if network is available, False otherwise.
                 如果网络可用则为True，否则为False。
        """
        return self._is_online
        
    def get_connection_quality(self) -> Dict[str, float]:
        """
        Get connection quality metrics.
        
        获取连接质量指标。
        
        Returns:
            Dict[str, float]: Dictionary containing quality metrics:
                             包含质量指标的字典：
                             - latency: Average response time
                               延迟：平均响应时间
                             - packet_loss: Packet loss percentage
                               丢包率：数据包丢失百分比
                             - uptime: Connection uptime percentage
                               正常运行时间：连接正常运行时间百分比
        """
        return self._metrics.copy()
        
    def check_connection(self) -> bool:
        """
        Check current network connection.
        
        检查当前网络连接。
        
        This method:
        - Tests connection to multiple hosts
        - Updates connection metrics
        - Handles connection failures
        - Triggers callbacks if status changes
        
        此方法：
        - 测试与多个主机的连接
        - 更新连接指标
        - 处理连接失败
        - 在状态改变时触发回调
        
        Returns:
            bool: True if connection is available, False otherwise.
                 如果连接可用则为True，否则为False。
        """
        latencies = []
        for host in NETWORK_CHECK_HOSTS:
            try:
                start_time = time.time()
                socket.create_connection((host, 80), NETWORK_CHECK_TIMEOUT)
                latency = time.time() - start_time
                latencies.append(latency)
            except (socket.timeout, socket.error) as e:
                logger.warning(f"Connection check failed for {host}: {e}")
                continue
                
        is_online = len(latencies) > 0
        if is_online != self._is_online:
            self._is_online = is_online
            self._notify_callbacks()
            
        if latencies:
            self._metrics["latency"] = statistics.mean(latencies)
            self._metrics["packet_loss"] = 1 - (len(latencies) / len(NETWORK_CHECK_HOSTS))
            
        return is_online
        
    def get_metrics(self) -> Dict[str, float]:
        """
        Get all network metrics.
        
        获取所有网络指标。
        
        Returns:
            Dict[str, float]: Dictionary containing all network metrics.
                             包含所有网络指标的字典。
        """
        return {
            **self.get_connection_quality(),
            "last_check": self._last_check_time
        }
        
    def _monitor_loop(self):
        """
        Main monitoring loop.
        
        主监控循环。
        
        This method runs in a separate thread and:
        - Periodically checks connection
        - Updates metrics
        - Handles reconnection attempts
        
        此方法在单独的线程中运行，并：
        - 定期检查连接
        - 更新指标
        - 处理重连尝试
        """
        while self._is_running:
            try:
                self._last_check_time = time.time()
                self.check_connection()
                self._update_metrics()
                time.sleep(self._check_interval)
            except Exception as e:
                logger.error(f"Error in monitor loop / 监控循环出错: {e}")
                time.sleep(NETWORK_RETRY_DELAY)
                
    def _update_metrics(self):
        """
        Update network metrics.
        
        更新网络指标。
        """
        if self._is_online:
            self._metrics["uptime"] = min(1.0, self._metrics["uptime"] + 0.1)
        else:
            self._metrics["uptime"] = max(0.0, self._metrics["uptime"] - 0.2)
            
    def _notify_callbacks(self):
        """
        Notify all registered callbacks of status change.
        
        通知所有已注册的回调函数状态变化。
        """
        for callback in self._callbacks:
            try:
                callback(self._is_online)
            except Exception as e:
                logger.error(f"Error in callback / 回调函数出错: {e}")

# Create global network monitor instance / 创建全局网络监控器实例
network_monitor = NetworkMonitor()

__all__ = ['network_monitor', 'NetworkMonitor'] 