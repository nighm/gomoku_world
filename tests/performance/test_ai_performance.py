"""AI performance tests
五子棋AI性能测试
"""

import time
import pytest
from gomoku_world.core import AI, Board

@pytest.fixture
def empty_board():
    """Create an empty board for testing"""
    return Board(15)

def measure_move_time(ai: AI, board: Board, player: int, num_moves: int = 5):
    """Measure average time for AI moves
    测量AI移动的平均时间
    
    Args:
        ai: AI instance
        board: Game board
        player: Current player
        num_moves: Number of moves to measure
    
    Returns:
        float: Average time per move in seconds
    """
    total_time = 0
    for _ in range(num_moves):
        start_time = time.time()
        move = ai.get_move(board, player)
        total_time += time.time() - start_time
        board.place_piece(move[0], move[1], player)
    
    return total_time / num_moves

def test_ai_performance_by_difficulty():
    """Test AI performance across different difficulty levels"""
    board = empty_board()
    difficulties = ["easy", "medium", "hard"]
    results = {}
    
    for difficulty in difficulties:
        ai = AI(difficulty=difficulty)
        avg_time = measure_move_time(ai, board, 1)
        results[difficulty] = avg_time
        board.clear()
    
    # 验证难度级别与计算时间的关系
    assert results["easy"] < results["medium"]
    assert results["medium"] < results["hard"]

def test_ai_performance_with_cache():
    """Test AI performance improvement with caching"""
    board = empty_board()
    ai = AI(difficulty="medium")
    
    # 第一次移动（无缓存）
    start_time = time.time()
    first_move = ai.get_move(board, 1)
    first_time = time.time() - start_time
    
    # 清空棋盘后再次移动（有缓存）
    board.clear()
    start_time = time.time()
    second_move = ai.get_move(board, 1)
    second_time = time.time() - start_time
    
    # 验证缓存是否提高了性能
    assert second_time < first_time
    assert first_move == second_move

def test_ai_performance_under_load():
    """Test AI performance under heavy load"""
    board = empty_board()
    ai = AI(difficulty="hard")
    moves_count = 50
    max_time_per_move = 2.0  # 每步最大允许时间（秒）
    
    for i in range(moves_count):
        start_time = time.time()
        move = ai.get_move(board, 1 if i % 2 == 0 else 2)
        move_time = time.time() - start_time
        
        # 验证每步时间是否在可接受范围内
        assert move_time < max_time_per_move
        board.place_piece(move[0], move[1], 1 if i % 2 == 0 else 2)

def test_ai_memory_usage():
    """Test AI memory usage during gameplay"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    board = empty_board()
    ai = AI(difficulty="hard")
    
    # 进行多次移动
    for _ in range(20):
        move = ai.get_move(board, 1)
        board.place_piece(move[0], move[1], 1)
    
    final_memory = process.memory_info().rss
    memory_increase = final_memory - initial_memory
    
    # 验证内存增长是否在合理范围内（小于50MB）
    assert memory_increase < 50 * 1024 * 1024  # 50MB in bytes