"""
System-wide performance tests
绯荤粺绾ф€ц兘娴嬭瘯
"""

import pytest
import time
import psutil
from typing import Dict, List
from gomoku_world.core import GameEngine
from gomoku_world.network import NetworkManager

class TestSystemPerformance:
    """绯荤粺鎬ц兘娴嬭瘯"""
    
    @pytest.mark.benchmark
    def test_game_engine_performance(self, benchmark):
        """娴嬭瘯娓告垙寮曟搸鎬ц兘"""
        engine = GameEngine()
        
        def run_game_cycle():
            engine.update()
            engine.render()
            engine.process_events()
        
        # 杩愯鍩哄噯娴嬭瘯
        benchmark(run_game_cycle)
    
    @pytest.mark.stress
    def test_network_stress(self):
        """缃戠粶鍘嬪姏娴嬭瘯"""
        network = NetworkManager()
        concurrent_connections = 1000
        
        start_time = time.time()
        active_connections = []
        
        try:
            # 鍒涘缓澶ч噺骞跺彂杩炴帴
            for i in range(concurrent_connections):
                conn = network.create_connection()
                active_connections.append(conn)
                
            # 楠岃瘉杩炴帴鐘舵€?
            assert len(network.get_active_connections()) == concurrent_connections
            
        finally:
            # 娓呯悊杩炴帴
            for conn in active_connections:
                conn.close()
    
    @pytest.mark.memory
    def test_memory_usage(self):
        """鍐呭瓨浣跨敤娴嬭瘯"""
        process = psutil.Process()
        
        initial_memory = process.memory_info().rss
        
        # 鎵ц瀵嗛泦鎿嶄綔
        engine = GameEngine()
        for _ in range(1000):
            engine.update()
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # 楠岃瘉鍐呭瓨澧為暱鍦ㄥ彲鎺ュ彈鑼冨洿鍐?
        assert memory_increase < 100 * 1024 * 1024  # 100MB 
