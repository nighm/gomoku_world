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
from ..i18n import i18n_manager

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
    - Localized status messages
    
    此类提供：
    - 连接状态监控
    - 网络质量指标
    - 状态变化事件回调
    - 自动重连处理
    - 本地化状态消息
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
        self._retry_count = 0
        
    def start(self):
        """
        Start network monitoring.
        
        启动网络监控。
        """
        if not self._is_running:
            self._is_running = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop)
            self._monitor_thread.daemon = True
            self._monitor_thread.start()
            logger.info(i18n_manager.get_text("network.status.monitoring_started"))
            
    def stop(self):
        """
        Stop network monitoring.
        
        停止网络监控。
        """
        if self._is_running:
            self._is_running = False
            if self._monitor_thread:
                self._monitor_thread.join()
            self._monitor_thread = None
            logger.info(i18n_manager.get_text("network.status.monitoring_stopped"))
            
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
        
    def get_connection_quality(self) -> Dict[str, str]:
        """
        Get localized connection quality metrics.
        
        获取本地化的连接质量指标。
        
        Returns:
            Dict[str, str]: Dictionary containing localized quality metrics:
                           包含本地化质量指标的字典：
                           - latency: Average response time
                             延迟：平均响应时间
                           - packet_loss: Packet loss percentage
                             丢包率：数据包丢失百分比
                           - uptime: Connection uptime percentage
                             正常运行时间：连接正常运行时间百分比
        """
        return {
            "latency": i18n_manager.get_text("network.metrics.latency", 
                                           ms=round(self._metrics["latency"] * 1000)),
            "packet_loss": i18n_manager.get_text("network.metrics.packet_loss",
                                               percent=round(self._metrics["packet_loss"] * 100, 1)),
            "uptime": i18n_manager.get_text("network.metrics.uptime",
                                          percent=round(self._metrics["uptime"] * 100, 1))
        }
        
    def check_connection(self) -> bool:
        """
        Check current network connection.
        
        检查当前网络连接。
        
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
                self._retry_count = 0  # Reset retry count on successful connection
            except (socket.timeout, socket.error) as e:
                logger.warning(i18n_manager.get_text("network.error.connection_failed",
                                                   host=host, error=str(e)))
                continue
                
        is_online = len(latencies) > 0
        if is_online != self._is_online:
            self._is_online = is_online
            status_key = "network.status.online" if is_online else "network.status.offline"
            logger.info(i18n_manager.get_text(status_key))
            self._notify_callbacks()
            
        if latencies:
            self._metrics["latency"] = statistics.mean(latencies)
            self._metrics["packet_loss"] = 1 - (len(latencies) / len(NETWORK_CHECK_HOSTS))
            self._metrics["uptime"] = time.time() - self._last_check_time
            
        return is_online
        
    def get_status_message(self) -> str:
        """
        Get localized network status message.
        
        获取本地化的网络状态消息。
        
        Returns:
            str: Current network status message.
                 当前网络状态消息。
        """
        if not self._is_running:
            return i18n_manager.get_text("network.status.not_monitoring")
            
        if self._is_online:
            metrics = self.get_connection_quality()
            return i18n_manager.get_text("network.status.details",
                                       latency=metrics["latency"],
                                       packet_loss=metrics["packet_loss"])
        else:
            if self._retry_count > 0:
                return i18n_manager.get_text("network.status.reconnecting",
                                           retry=self._retry_count,
                                           max_retries=NETWORK_MAX_RETRIES)
            return i18n_manager.get_text("network.status.offline")
            
    def _monitor_loop(self):
        """
        Main monitoring loop.
        
        主监控循环。
        """
        while self._is_running:
            try:
                if not self.check_connection() and self._retry_count < NETWORK_MAX_RETRIES:
                    self._retry_count += 1
                    logger.info(i18n_manager.get_text("network.status.retry",
                                                    retry=self._retry_count,
                                                    max_retries=NETWORK_MAX_RETRIES))
                    time.sleep(NETWORK_RETRY_DELAY)
                    continue
                    
                self._last_check_time = time.time()
                time.sleep(self._check_interval)
                
            except Exception as e:
                logger.error(i18n_manager.get_text("network.error.monitoring_failed",
                                                 error=str(e)))
                time.sleep(NETWORK_RETRY_DELAY)
                
    def _notify_callbacks(self):
        """
        Notify all registered callbacks of status change.
        
        通知所有注册的回调状态变化。
        """
        for callback in self._callbacks:
            try:
                callback(self._is_online)
            except Exception as e:
                logger.error(i18n_manager.get_text("network.error.callback_failed",
                                                 error=str(e)))

# Create global network monitor instance / 创建全局网络监控器实例
network_monitor = NetworkMonitor()

__all__ = ['network_monitor', 'NetworkMonitor'] 