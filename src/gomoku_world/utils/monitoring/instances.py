"""
Global instances for monitoring
监控全局实例
"""

from .metrics import MetricsCollector
from .profiler import Profiler
from .tracer import Tracer
from .health import HealthChecker

# Create global instances
metrics_collector = MetricsCollector()
profiler = Profiler()
tracer = Tracer()
health_checker = HealthChecker()

__all__ = [
    'metrics_collector',
    'profiler',
    'tracer',
    'health_checker'
] 