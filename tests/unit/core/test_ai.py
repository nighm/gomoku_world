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
        assert ai.max_depth == 3
        
    def test_get_depth_for_difficulty(self, ai):
        """测试不同难度级别的搜索深度"""
        ai.difficulty = "easy"
        assert ai._get_depth_for_difficulty() == 2
        
        ai.difficulty = "medium"
        assert ai._get_depth_for_difficulty() == 3
        
        ai.difficulty = "hard"
        assert ai._get_depth_for_difficulty() == 4
        
    def test_get_move(self, ai, board):
        """测试获取移动"""
        # 测试空棋盘的移动
        move = ai.get_move(board, 1)
        assert isinstance(move, tuple)
        assert len(move) == 2
        assert 0 <= move[0] < board.size
        assert 0 <= move[1] < board.size
        
        # 测试简单难度的随机移动
        ai.difficulty = "easy"
        move = ai.get_move(board, 1)
        assert isinstance(move, tuple)
        assert len(move) == 2
        
    def test_evaluate_position(self, ai, board):
        """测试位置评估"""
        # 测试空棋盘
        score = ai._evaluate_position(board, 1)
        assert score == 0
        
        # 测试有一个棋子的情况
        board.place_piece(7, 7, 1)
        score = ai._evaluate_position(board, 1)
        assert score > 0
        
    def test_count_consecutive(self, ai, board):
        """测试连续棋子计数"""
        # 放置三个连续的棋子
        board.place_piece(7, 7, 1)
        board.place_piece(7, 8, 1)
        board.place_piece(7, 9, 1)
        
        count = ai._count_consecutive(board, 7, 7, 0, 1, 1)
        assert count == 3
        
    def test_score_sequence(self, ai):
        """测试序列评分"""
        assert ai._score_sequence(5, 1) == 1000000  # 胜利
        assert ai._score_sequence(4, 1) == 10000   # 四子连珠
        assert ai._score_sequence(3, 1) == 1000    # 三子连珠
        assert ai._score_sequence(2, 1) == 100     # 两子连珠
        assert ai._score_sequence(1, 1) == 10      # 单子
        
    def test_is_terminal(self, ai, board):
        """测试终局判断"""
        assert not ai._is_terminal(board)  # 空棋盘
        
        # 创建获胜局面
        for i in range(5):
            board.place_piece(7, 7+i, 1)
        assert ai._is_terminal(board)
        
    def test_check_win(self, ai, board):
        """测试获胜判断"""
        assert not ai._check_win(board, 7, 7)  # 空位置
        
        # 创建水平获胜线
        for i in range(5):
            board.place_piece(7, 7+i, 1)
        assert ai._check_win(board, 7, 7)
        
    def test_get_prioritized_moves(self, ai, board):
        """测试移动优先级排序"""
        moves = ai._get_prioritized_moves(board)
        assert isinstance(moves, list)
        assert all(isinstance(move, tuple) for move in moves)
        assert all(len(move) == 2 for move in moves)
        
    def test_score_move_position(self, ai, board):
        """测试移动位置评分"""
        # 测试中心位置
        center_score = ai._score_move_position(board, board.size//2, board.size//2)
        edge_score = ai._score_move_position(board, 0, 0)
        assert center_score > edge_score  # 中心位置应该得分更高
        
    def test_get_random_move(self, ai, board):
        """测试随机移动"""
        move = ai._get_random_move(board)
        assert isinstance(move, tuple)
        assert len(move) == 2
        assert 0 <= move[0] < board.size
        assert 0 <= move[1] < board.size