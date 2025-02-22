"""Integration tests for AI module.

五子棋AI模块的集成测试。

Tests cover:
- AI interaction with board
- Game flow with AI
- Strategy integration
- Evaluation system integration

测试覆盖：
- AI与棋盘的交互
- AI参与的游戏流程
- 策略系统集成
- 评估系统集成
"""

import pytest
from gomoku_world.core.ai import AI
from gomoku_world.core.board import Board
from gomoku_world.core.ai.strategy import AIStrategy
from gomoku_world.core.ai.evaluation import AIEvaluation

@pytest.fixture
def game_setup():
    """Set up game components for testing.
    
    设置用于测试的游戏组件。
    """
    board = Board()
    ai = AI("medium")
    return board, ai

def test_ai_board_interaction(game_setup):
    """Test AI interaction with game board.
    
    测试AI与游戏棋盘的交互。
    """
    board, ai = game_setup
    
    # Make several moves
    for _ in range(5):
        move = ai.get_move(board, 1)
        board.place_piece(move[0], move[1], 1)
        assert board.get_piece(move[0], move[1]) == 1

def test_ai_strategy_integration(game_setup):
    """Test AI strategy system integration.
    
    测试AI策略系统集成。
    """
    board, ai = game_setup
    
    # Test strategy adaptation
    ai.set_difficulty("hard")
    assert ai.strategy.max_depth > ai.strategy._get_depth_for_difficulty("easy")
    
    # Verify move priorities
    center = board.size // 2
    edge = 0
    center_priority = ai.strategy.get_move_priority(board, center, center)
    edge_priority = ai.strategy.get_move_priority(board, edge, edge)
    assert center_priority > edge_priority

def test_ai_evaluation_integration(game_setup):
    """Test AI evaluation system integration.
    
    测试AI评估系统集成。
    """
    board, ai = game_setup
    
    # Place pieces to create advantage
    board.place_piece(7, 7, 1)
    board.place_piece(7, 8, 1)
    board.place_piece(7, 9, 1)
    
    # AI should prefer moves near the sequence
    move = ai.get_move(board, 1)
    assert abs(move[0] - 7) <= 1  # Should be close to the sequence

def test_game_flow_with_ai(game_setup):
    """Test complete game flow with AI.
    
    测试与AI的完整游戏流程。
    """
    board, ai = game_setup
    current_player = 1
    
    # Play until game ends or max moves reached
    for _ in range(25):  # Reasonable number of moves for testing
        move = ai.get_move(board, current_player)
        board.place_piece(move[0], move[1], current_player)
        
        if board.check_win(move[0], move[1], current_player):
            break
            
        current_player = 3 - current_player  # Switch player

def test_ai_cache_integration(game_setup):
    """Test AI cache system integration.
    
    测试AI缓存系统集成。
    """
    board, ai = game_setup
    
    # Make some moves to populate cache
    moves_and_scores = []
    for _ in range(3):
        move = ai.get_move(board, 1)
        moves_and_scores.append(move)
        board.place_piece(move[0], move[1], 1)
    
    # Clear cache and verify new moves
    ai.cache.clear()
    new_board = Board()
    new_moves = []
    for _ in range(3):
        move = ai.get_move(new_board, 1)
        new_moves.append(move)
        new_board.place_piece(move[0], move[1], 1)
    
    # Moves should be different after cache clear
    assert moves_and_scores != new_moves

def test_ai_difficulty_effects(game_setup):
    """Test effects of different difficulty levels.
    
    测试不同难度级别的效果。
    """
    board, ai = game_setup
    
    moves = {}
    for diff in ["easy", "medium", "hard"]:
        ai.set_difficulty(diff)
        board_copy = Board()  # Fresh board for each difficulty
        moves[diff] = ai.get_move(board_copy, 1)
    
    # Verify different difficulties make different choices
    # in at least some cases
    assert len(set(str(move) for move in moves.values())) > 1