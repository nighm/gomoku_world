import pytest
from gomoku_world.core.ai import AI
from gomoku_world.core.board import Board

class TestAIIntegration:
    """AI集成测试"""
    
    @pytest.fixture
    def ai_black(self):
        """创建黑方AI实例"""
        return AI(difficulty="medium")
    
    @pytest.fixture
    def ai_white(self):
        """创建白方AI实例"""
        return AI(difficulty="medium")
    
    @pytest.fixture
    def board(self):
        """创建棋盘实例"""
        return Board()
    
    def test_ai_vs_ai_game(self, ai_black, ai_white, board):
        """测试AI对战"""
        moves_count = 0
        current_player = 1  # 黑方先手
        
        while not board.is_full():
            # 获取当前AI
            current_ai = ai_black if current_player == 1 else ai_white
            
            # 获取并执行移动
            row, col = current_ai.get_move(board, current_player)
            board.place_piece(row, col, current_player)
            moves_count += 1
            
            # 检查获胜
            if board.check_win(row, col):
                break
                
            # 切换玩家
            current_player = 3 - current_player
        
        # 验证游戏是否正常结束
        assert moves_count > 0
        assert board.check_win(row, col) or board.is_full()
    
    def test_ai_difficulty_comparison(self):
        """测试不同难度AI的表现差异"""
        easy_ai = AI(difficulty="easy")
        hard_ai = AI(difficulty="hard")
        board = Board()
        
        # 记录两个AI的决策时间
        easy_time_start = time.time()
        easy_move = easy_ai.get_move(board, 1)
        easy_time = time.time() - easy_time_start
        
        board = Board()  # 重置棋盘
        
        hard_time_start = time.time()
        hard_move = hard_ai.get_move(board, 1)
        hard_time = time.time() - hard_time_start
        
        # 验证难度更高的AI会花费更多时间思考
        assert hard_time > easy_time
    
    def test_ai_defensive_play(self, ai_black, board):
        """测试AI的防守能力"""
        # 创建威胁局面（对手即将连成四子）
        for i in range(4):
            board.place_piece(7, i, 2)  # 对手（白方）连续放置四子
        
        # AI应该选择防守位置
        row, col = ai_black.get_move(board, 1)
        assert (row == 7 and col == 4) or (row == 7 and col == -1)
    
    def test_ai_offensive_play(self, ai_black, board):
        """测试AI的进攻能力"""
        # 创建进攻局面（AI即将连成四子）
        for i in range(4):
            board.place_piece(7, i, 1)  # AI（黑方）连续放置四子
        
        # AI应该选择进攻位置完成五子连珠
        row, col = ai_black.get_move(board, 1)
        assert row == 7 and col == 4
    
    def test_ai_performance_stability(self, ai_black, board):
        """测试AI性能稳定性"""
        moves = []
        times = []
        
        # 连续进行多次决策
        for _ in range(10):
            start_time = time.time()
            move = ai_black.get_move(board, 1)
            end_time = time.time()
            
            moves.append(move)
            times.append(end_time - start_time)
            
            # 执行移动
            board.place_piece(move[0], move[1], 1)
        
        # 验证决策时间的稳定性
        avg_time = sum(times) / len(times)
        max_deviation = max(abs(t - avg_time) for t in times)
        
        # 时间波动不应过大（这里设定阈值为平均时间的50%）
        assert max_deviation <= avg_time * 0.5