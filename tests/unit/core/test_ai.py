import pytest
from gomoku_world.core.ai import AI
from gomoku_world.core.board import Board

class TestAI:
    """AI类的单元测试"""
    
    @pytest.fixture
    def ai(self):
        """创建AI实例"""
        return AI(difficulty="medium")
    
    @pytest.fixture
    def board(self):
        """创建棋盘实例"""
        return Board()
    
    def test_init(self, ai):
        """测试AI初始化"""
        assert ai.difficulty == "medium"
        assert ai.depth == 4  # medium难度的搜索深度为4
        
    def test_get_depth_for_difficulty(self, ai):
        """测试不同难度级别的搜索深度"""
        ai.difficulty = "easy"
        assert ai._get_depth_for_difficulty() == 2
        
        ai.difficulty = "medium"
        assert ai._get_depth_for_difficulty() == 4
        
        ai.difficulty = "hard"
        assert ai._get_depth_for_difficulty() == 6
        
    def test_get_move(self, ai, board):
        """测试获取移动"""
        # 测试空棋盘的移动
        move = ai.get_move(board, 1)
        assert isinstance(move, tuple)
        assert len(move) == 2
        assert 0 <= move[0] < board.size
        assert 0 <= move[1] < board.size
        
        # 测试不同难度的移动
        ai.difficulty = "easy"
        move = ai.get_move(board, 1)
        assert isinstance(move, tuple)
        assert len(move) == 2
        
        ai.difficulty = "hard"
        move = ai.get_move(board, 1)
        assert isinstance(move, tuple)
        assert len(move) == 2
        
    def test_evaluate_position(self, ai, board):
        """测试位置评估"""
        # 测试空棋盘
        score = ai.evaluate_position(board, 1)
        assert score == 0
        
        # 测试有一个棋子的情况
        board.place_piece(7, 7, 1)
        score = ai.evaluate_position(board, 1)
        assert score > 0
        
    def test_set_difficulty(self, ai):
        """测试设置难度"""
        ai.set_difficulty("easy")
        assert ai.difficulty == "easy"
        assert ai.depth == 2
        
        ai.set_difficulty("medium")
        assert ai.difficulty == "medium"
        assert ai.depth == 4
        
        ai.set_difficulty("hard")
        assert ai.difficulty == "hard"
        assert ai.depth == 6
        
    def test_get_best_moves(self, ai, board):
        """测试获取最佳移动"""
        # 测试空棋盘
        moves = ai.get_best_moves(board, 1, num_moves=3)
        assert isinstance(moves, list)
        assert len(moves) <= 3
        assert all(isinstance(move, tuple) for move in moves)
        assert all(len(move) == 2 for move in moves)
        
        # 测试有棋子的情况
        board.place_piece(7, 7, 1)
        moves = ai.get_best_moves(board, 1, num_moves=3)
        assert isinstance(moves, list)
        assert len(moves) <= 3
        assert all(isinstance(move, tuple) for move in moves)
        assert all(len(move) == 2 for move in moves)