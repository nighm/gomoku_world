"""
Performance tests for manager instances
绠＄悊鍣ㄥ疄渚嬫€ц兘娴嬭瘯
"""

import pytest
import time
import asyncio
import psutil
import gc
from typing import List

from gomoku_world.config.instances import config_manager
from gomoku_world.network.instances import network_manager
from gomoku_world.utils.debug.instances import debug_manager

@pytest.mark.benchmark
def test_config_manager_performance(benchmark):
    """Test configuration manager performance"""
    def config_operations():
        # Perform a series of config operations
        for i in range(100):
            config_manager.set_value(f'TEST_KEY_{i}', f'value_{i}')
            value = config_manager.get_value(f'TEST_KEY_{i}')
            assert value == f'value_{i}'
    
    # Run benchmark
    benchmark(config_operations)
    
    # Cleanup
    config_manager.reset()

@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_network_manager_performance(benchmark):
    """Test network manager performance"""
    await network_manager.connect()
    
    async def network_operations():
        # Perform a series of network operations
        for i in range(100):
            await network_manager.send_message({
                'type': 'test',
                'data': f'test_data_{i}'
            })
    
    # Run benchmark
    benchmark(network_operations)
    
    # Cleanup
    await network_manager.disconnect()

@pytest.mark.benchmark
def test_debug_manager_performance(benchmark):
    """Test debug manager performance"""
    def debug_operations():
        # Perform a series of debug operations
        for i in range(1000):
            debug_manager.update_fps()
            debug_manager.debug_info['test_value'] = i
    
    # Run benchmark
    benchmark(debug_operations)
    
    # Cleanup
    debug_manager.reset()

@pytest.mark.benchmark
def test_manager_memory_usage():
    """Test memory usage of managers"""
    process = psutil.Process()
    
    def measure_memory() -> float:
        """Measure current memory usage"""
        gc.collect()  # Force garbage collection
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    # Measure initial memory
    initial_memory = measure_memory()
    
    # Create many configuration entries
    memory_samples: List[float] = []
    for i in range(1000):
        config_manager.set_value(f'MEMORY_TEST_KEY_{i}', 'x' * 1000)
        if i % 100 == 0:
            memory_samples.append(measure_memory())
    
    # Calculate memory growth
    final_memory = measure_memory()
    memory_growth = final_memory - initial_memory
    
    # Memory growth should be reasonable
    assert memory_growth < 100  # Less than 100MB growth
    
    # Cleanup
    config_manager.reset()
    gc.collect()
    
    # Memory should be mostly recovered
    cleanup_memory = measure_memory()
    assert cleanup_memory - initial_memory < 10  # Less than 10MB difference

@pytest.mark.asyncio
@pytest.mark.benchmark
async def test_network_latency():
    """Test network communication latency"""
    await network_manager.connect()
    
    latencies = []
    
    # Measure round-trip time for messages
    for _ in range(100):
        start_time = time.time()
        await network_manager.send_message({'type': 'ping'})
        latency = time.time() - start_time
        latencies.append(latency)
    
    # Calculate statistics
    avg_latency = sum(latencies) / len(latencies)
    max_latency = max(latencies)
    
    # Latency should be reasonable
    assert avg_latency < 0.1  # Average latency under 100ms
    assert max_latency < 0.5  # Max latency under 500ms
    
    await network_manager.disconnect()

@pytest.mark.benchmark
def test_concurrent_operations(benchmark):
    """Test performance of concurrent operations"""
    async def concurrent_operations():
        # Enable debug mode
        debug_manager.toggle_debug_mode()
        
        # Start network connection
        await network_manager.connect()
        
        # Perform concurrent operations
        tasks = []
        for i in range(100):
            tasks.append(asyncio.create_task(
                network_manager.send_message({'type': 'test', 'id': i})
            ))
            config_manager.set_value(f'TEST_KEY_{i}', f'value_{i}')
            debug_manager.debug_info[f'operation_{i}'] = time.time()
        
        # Wait for all network operations
        await asyncio.gather(*tasks)
        
        # Cleanup
        await network_manager.disconnect()
    
    # Run benchmark
    benchmark(concurrent_operations)

@pytest.mark.benchmark
def test_manager_initialization_time(benchmark):
    """Test manager initialization performance"""
    def create_managers():
        from gomoku_world.config.manager import ConfigManager
        from gomoku_world.network.network import NetworkManager
        from gomoku_world.utils.debug.manager import DebugManager
        
        # Create new instances (should use existing ones)
        config = ConfigManager()
        network = NetworkManager()
        debug = DebugManager()
        
        # Verify they are the same instances
        assert config is config_manager
        assert network is network_manager
        assert debug is debug_manager
    
    # Run benchmark
    benchmark(create_managers) 
