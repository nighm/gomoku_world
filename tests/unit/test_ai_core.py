"""AI class unit tests
五子棋AI类单元测试
"""

import pytest
from gomoku_world.core import AI, Board

@pytest.fixture
def ai_player():
    """Create an AI player with medium difficulty"""
    return AI(difficulty="medium")

@pytest.fixture
def board_with_moves(board_15x15):
    """Create a board with some moves"""
    # 在棋盘上放置一些棋子
    board_15x15.place_piece(7, 7, 1)  # 黑棋
    board_15x15.place_piece(7, 8, 2)  # 白棋
    board_15x15.place_piece(8, 7, 1)  # 黑棋
    return board_15x15

def test_ai_initialization():
    """Test AI initialization with different difficulty levels"""
    ai_easy = AI(difficulty="easy")
    ai_medium = AI(difficulty="medium")
    ai_hard = AI(difficulty="hard")
    
    assert ai_easy.strategy.difficulty == "easy"
    assert ai_medium.strategy.difficulty == "medium"
    assert ai_hard.strategy.difficulty == "hard"

def test_get_move(ai_player, board_15x15):
    """Test AI move generation on empty board"""
    move = ai_player.get_move(board_15x15, 1)
    assert isinstance(move, tuple)
    assert len(move) == 2
    assert 0 <= move[0] < board_15x15.size
    assert 0 <= move[1] < board_15x15.size

def test_get_move_with_existing_moves(ai_player, board_with_moves):
    """Test AI move generation with existing pieces"""
    move = ai_player.get_move(board_with_moves, 2)
    assert isinstance(move, tuple)
    assert len(move) == 2
    assert board_with_moves.is_valid_move(move[0], move[1])

def test_set_difficulty(ai_player):
    """Test difficulty level change"""
    ai_player.set_difficulty("hard")
    assert ai_player.strategy.difficulty == "hard"
    
    ai_player.set_difficulty("easy")
    assert ai_player.strategy.difficulty == "easy"

def test_cache_functionality(ai_player, board_15x15):
    """Test AI move caching"""
    # 获取第一次移动
    first_move = ai_player.get_move(board_15x15, 1)
    
    # 清空棋盘并再次获取移动
    board_15x15.clear()
    second_move = ai_player.get_move(board_15x15, 1)
    
    # 由于缓存机制，对于相同的棋盘状态应返回相同的移动
    assert first_move == second_move

def test_invalid_difficulty():
    """Test handling of invalid difficulty level"""
    ai = AI(difficulty="invalid")
    # 对于无效的难度级别，应该使用默认的medium难度
    assert ai.strategy.difficulty == "medium"

def test_consecutive_moves(ai_player, board_15x15):
    """Test AI's consecutive move generation"""
    moves = set()
    for _ in range(5):
        move = ai_player.get_move(board_15x15, 1)
        # 确保移动有效
        assert board_15x15.is_valid_move(move[0], move[1])
        # 记录移动并在棋盘上落子
        moves.add(move)
        board_15x15.place_piece(move[0], move[1], 1)
    
    # 确保生成了不同的移动
    assert len(moves) == 5