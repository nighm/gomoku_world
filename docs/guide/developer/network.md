# Network Monitoring Guide

## Overview

The network monitoring system in Gomoku World provides real-time network status tracking and quality metrics. This guide covers the implementation, configuration, and best practices for using the network monitoring features.

## Basic Concepts

### Connection Status
- Online/Offline detection
- Connection quality metrics
- Status change callbacks
- Error handling and recovery

### Network Quality
- Latency monitoring
- Bandwidth measurement
- Connection stability tracking
- Quality thresholds and alerts

### Status Callbacks
- Event-driven architecture
- Registration and deregistration
- Callback execution order
- Error handling in callbacks

## Implementation

### NetworkMonitor Class

```python
from gomoku_world.utils.network import NetworkMonitor

class NetworkMonitor:
    def __init__(self):
        self._callbacks = []
        self._is_running = False
        self._check_interval = 60  # seconds
        
    def start(self):
        """Start network monitoring"""
        self._is_running = True
        self._start_monitoring()
    
    def stop(self):
        """Stop network monitoring"""
        self._is_running = False
    
    def is_online(self):
        """Check if network is available"""
        return self._check_connection()
    
    def add_callback(self, callback):
        """Add status change callback"""
        self._callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Remove status change callback"""
        self._callbacks.remove(callback)
```

## Features

### Status Monitoring
- Periodic connection checks
- Configurable check intervals
- Multiple endpoint support
- Timeout handling

### Network Quality Metrics
- Response time tracking
- Packet loss detection
- Bandwidth measurement
- Quality score calculation

### Callback System
- Multiple callback support
- Priority-based execution
- Async callback handling
- Error isolation

### Error Handling
- Connection timeouts
- DNS resolution errors
- Authentication failures
- Rate limiting

## Integration

### System Integration
```python
from gomoku_world.utils.network import network_monitor

# Start monitoring
network_monitor.start()

# Check status
is_online = network_monitor.is_online()

# Stop monitoring
network_monitor.stop()
```

### UI Integration
```python
def update_ui_status(is_online):
    if is_online:
        status_label.config(text="Online", bg="green")
    else:
        status_label.config(text="Offline", bg="red")

# Register UI callback
network_monitor.add_callback(update_ui_status)
```

### I18n Integration
```python
def update_status_text(is_online):
    status_key = "online" if is_online else "offline"
    text = i18n_manager.get_text(f"network.status.{status_key}")
    status_label.config(text=text)

# Register i18n callback
network_monitor.add_callback(update_status_text)
```

## Configuration

### Monitor Settings
```python
from gomoku_world.config import config_manager

# Basic settings
config_manager.set("network", "check_interval", 60)
config_manager.set("network", "timeout", 5)
config_manager.set("network", "max_retries", 3)

# Quality thresholds
config_manager.set("network", "latency_threshold", 200)
config_manager.set("network", "packet_loss_threshold", 0.1)
```

### Proxy Support
```python
# Configure proxy
config_manager.set("network", "proxy", {
    "enabled": True,
    "host": "proxy.example.com",
    "port": 8080,
    "auth": {
        "username": "user",
        "password": "pass"
    }
})
```

## Best Practices

### Performance
- Optimize check intervals
- Use connection pooling
- Implement caching
- Minimize callback overhead

### Security
- Use secure endpoints
- Validate certificates
- Handle sensitive data
- Implement rate limiting

### Reliability
- Multiple endpoint fallback
- Exponential backoff
- Circuit breaker pattern
- Error recovery strategies

### Testing
- Unit test coverage
- Mock network conditions
- Stress testing
- Integration testing

## Troubleshooting

### Common Issues
1. Connection timeouts
2. DNS resolution failures
3. Proxy configuration errors
4. Callback exceptions

### Debug Tools
```python
# Enable debug logging
import logging
logging.getLogger("network").setLevel(logging.DEBUG)

# Monitor specific endpoint
network_monitor.check_endpoint("api.example.com")

# Test proxy connection
network_monitor.test_proxy_connection()
```

### Solutions
1. Check network configuration
2. Verify proxy settings
3. Update security certificates
4. Review firewall rules

## API Reference

### NetworkMonitor
- `start()`: Start monitoring
- `stop()`: Stop monitoring
- `is_online()`: Check status
- `add_callback(callback)`: Add callback
- `remove_callback(callback)`: Remove callback
- `get_quality_metrics()`: Get metrics
- `test_connection()`: Test connection

### NetworkQuality
- `get_latency()`: Get latency
- `get_packet_loss()`: Get loss rate
- `get_bandwidth()`: Get bandwidth
- `get_quality_score()`: Get score

### NetworkConfig
- `load_config()`: Load config
- `save_config()`: Save config
- `get_proxy_settings()`: Get proxy
- `set_proxy_settings()`: Set proxy 