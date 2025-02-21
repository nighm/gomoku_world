"""
System-wide performance tests
系统级性能测试
"""

import pytest
import time
import psutil
from typing import Dict, List
from gomoku_world.core import GameEngine
from gomoku_world.network import NetworkManager

class TestSystemPerformance:
    """系统性能测试"""
    
    @pytest.mark.benchmark
    def test_game_engine_performance(self, benchmark):
        """测试游戏引擎性能"""
        engine = GameEngine()
        
        def run_game_cycle():
            engine.update()
            engine.render()
            engine.process_events()
        
        # 运行基准测试
        benchmark(run_game_cycle)
    
    @pytest.mark.stress
    def test_network_stress(self):
        """网络压力测试"""
        network = NetworkManager()
        concurrent_connections = 1000
        
        start_time = time.time()
        active_connections = []
        
        try:
            # 创建大量并发连接
            for i in range(concurrent_connections):
                conn = network.create_connection()
                active_connections.append(conn)
                
            # 验证连接状态
            assert len(network.get_active_connections()) == concurrent_connections
            
        finally:
            # 清理连接
            for conn in active_connections:
                conn.close()
    
    @pytest.mark.memory
    def test_memory_usage(self):
        """内存使用测试"""
        process = psutil.Process()
        
        initial_memory = process.memory_info().rss
        
        # 执行密集操作
        engine = GameEngine()
        for _ in range(1000):
            engine.update()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 验证内存增长在可接受范围内
        assert memory_increase < 100 * 1024 * 1024  # 100MB 