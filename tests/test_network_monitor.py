"""
Test network monitoring functionality
测试网络监控功能
"""

import pytest
import time
from unittest.mock import MagicMock, patch
from gomoku_world.utils.network import NetworkMonitor
from gomoku_world.config.settings import (
    NETWORK_CHECK_INTERVAL,
    NETWORK_CHECK_TIMEOUT,
    NETWORK_MAX_RETRIES
)

@pytest.fixture
def network_monitor():
    """Create network monitor instance"""
    monitor = NetworkMonitor(check_interval=1)
    yield monitor
    monitor.stop()

def test_network_monitor_init(network_monitor):
    """Test network monitor initialization"""
    assert not network_monitor.is_online()
    assert network_monitor._check_interval == 1
    assert not network_monitor._callbacks
    assert network_monitor._monitor_thread is None

def test_network_monitor_start_stop(network_monitor):
    """Test starting and stopping network monitor"""
    network_monitor.start()
    assert network_monitor._monitor_thread is not None
    assert network_monitor._monitor_thread.is_alive()
    
    network_monitor.stop()
    assert not network_monitor._monitor_thread.is_alive()

def test_network_monitor_callbacks(network_monitor):
    """Test callback functionality"""
    callback = MagicMock()
    network_monitor.add_callback(callback)
    assert callback in network_monitor._callbacks
    
    network_monitor.remove_callback(callback)
    assert callback not in network_monitor._callbacks

@patch('socket.socket')
def test_network_monitor_connection_check(mock_socket, network_monitor):
    """Test connection checking"""
    # Mock successful connection
    mock_socket.return_value.connect.return_value = None
    assert network_monitor.check_connection()
    
    # Mock connection failure
    mock_socket.return_value.connect.side_effect = Exception("Connection failed")
    assert not network_monitor.check_connection()

@patch('socket.socket')
def test_network_monitor_proxy_support(mock_socket, network_monitor):
    """Test proxy support"""
    # Configure proxy
    network_monitor._proxy = {
        "enabled": True,
        "host": "proxy.example.com",
        "port": 8080
    }
    
    # Mock successful proxy connection
    mock_socket.return_value.recv.return_value = b"HTTP/1.1 200 Connection established\r\n\r\n"
    assert network_monitor.check_connection()
    
    # Mock proxy connection failure
    mock_socket.return_value.recv.return_value = b"HTTP/1.1 403 Forbidden\r\n\r\n"
    assert not network_monitor.check_connection()

def test_network_monitor_connection_quality(network_monitor):
    """Test connection quality metrics"""
    # No measurements
    quality = network_monitor.get_connection_quality()
    assert quality["latency"] == float("inf")
    assert quality["jitter"] == float("inf")
    
    # Add some measurements
    network_monitor._latencies = {
        "test.host": [0.1, 0.2, 0.15, 0.18]
    }
    
    quality = network_monitor.get_connection_quality()
    assert 0.15 <= quality["latency"] <= 0.16  # Average around 0.1575
    assert 0.03 <= quality["jitter"] <= 0.04   # Standard deviation

@pytest.mark.asyncio
async def test_network_monitor_status_change():
    """Test network status change handling"""
    monitor = NetworkMonitor(check_interval=0.1)
    callback = MagicMock()
    monitor.add_callback(callback)
    
    with patch('socket.socket') as mock_socket:
        # Start with online status
        mock_socket.return_value.connect.return_value = None
        monitor.start()
        await asyncio.sleep(0.2)
        assert monitor.is_online()
        callback.assert_called_with(True)
        
        # Switch to offline
        mock_socket.return_value.connect.side_effect = Exception("Connection failed")
        await asyncio.sleep(0.2)
        assert not monitor.is_online()
        callback.assert_called_with(False)
        
    monitor.stop() 