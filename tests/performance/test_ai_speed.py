"""
AI performance tests
AI 鎬ц兘娴嬭瘯
"""

import time
import pytest
from gomoku_world.core import Board, AI

def test_ai_move_speed():
    """Test AI move generation speed"""
    board = Board(size=15)
    ai = AI()
    
    # Place some pieces to create a more realistic position
    pieces = [
        (7, 7, 1), (7, 8, 2),
        (8, 7, 1), (8, 8, 2),
        (6, 6, 1), (6, 7, 2),
    ]
    for row, col, player in pieces:
        board.place_piece(row, col, player)
    
    # Measure AI move generation time
    start_time = time.time()
    ai_move = ai.get_move(board, 1)
    end_time = time.time()
    
    # AI should make a move within 1 second
    assert end_time - start_time < 1.0
    assert isinstance(ai_move, tuple)
    assert len(ai_move) == 2

def test_ai_performance_under_load():
    """Test AI performance with many pieces on board"""
    board = Board(size=15)
    ai = AI()
    
    # Fill 70% of the board randomly
    import random
    positions = [(i, j) for i in range(15) for j in range(15)]
    random.shuffle(positions)
    
    # Place pieces
    num_pieces = int(15 * 15 * 0.7)  # 70% of board
    for i in range(num_pieces):
        row, col = positions[i]
        player = 1 if i % 2 == 0 else 2
        board.place_piece(row, col, player)
    
    # Measure AI move generation time
    start_time = time.time()
    ai_move = ai.get_move(board, 1)
    end_time = time.time()
    
    # AI should make a move within 2 seconds even with many pieces
    assert end_time - start_time < 2.0
    assert isinstance(ai_move, tuple)
    assert len(ai_move) == 2

@pytest.mark.benchmark
def test_ai_move_benchmark(benchmark):
    """Benchmark AI move generation"""
    board = Board(size=15)
    ai = AI()
    
    # Place some pieces
    pieces = [
        (7, 7, 1), (7, 8, 2),
        (8, 7, 1), (8, 8, 2),
    ]
    for row, col, player in pieces:
        board.place_piece(row, col, player)
    
    # Benchmark AI move generation
    result = benchmark(lambda: ai.get_move(board, 1))
    
    assert isinstance(result, tuple)
    assert len(result) == 2 
