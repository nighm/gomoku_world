# AI开发教程

## 概述

五子棋AI模块使用极小化极大算法（Minimax）和Alpha-beta剪枝实现，支持多个难度级别。本教程将详细介绍AI的实现原理和优化方法。

## 核心算法

### 极小化极大算法

```python
def minimax(board, depth, player):
    if depth == 0 or is_terminal(board):
        return evaluate_position(board)
    
    if player == 1:  # 最大化玩家
        value = float('-inf')
        for move in get_valid_moves(board):
            value = max(value, minimax(board_after_move(board, move), depth-1, 2))
        return value
    else:  # 最小化玩家
        value = float('inf')
        for move in get_valid_moves(board):
            value = min(value, minimax(board_after_move(board, move), depth-1, 1))
        return value
```

### Alpha-Beta剪枝

通过记录α（已知最大值）和β（已知最小值）来减少搜索空间：

```python
def alpha_beta(board, depth, alpha, beta, player):
    if depth == 0 or is_terminal(board):
        return evaluate_position(board)
    
    if player == 1:  # 最大化玩家
        value = float('-inf')
        for move in get_valid_moves(board):
            value = max(value, alpha_beta(board_after_move(board, move), 
                                        depth-1, alpha, beta, 2))
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Beta剪枝
        return value
    else:  # 最小化玩家
        value = float('inf')
        for move in get_valid_moves(board):
            value = min(value, alpha_beta(board_after_move(board, move), 
                                        depth-1, alpha, beta, 1))
            beta = min(beta, value)
            if alpha >= beta:
                break  # Alpha剪枝
        return value
```

## 评估函数

### 位置评估

```python
def evaluate_position(board):
    score = 0
    # 检查连续棋子
    score += check_consecutive(board, 5) * 100000  # 五连
    score += check_consecutive(board, 4) * 10000   # 活四
    score += check_consecutive(board, 3) * 1000    # 活三
    score += check_consecutive(board, 2) * 100     # 活二
    
    # 考虑棋子位置
    score += evaluate_position_weight(board)
    return score
```

### 位置权重

```python
def evaluate_position_weight(board):
    weights = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 2, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    score = 0
    for i in range(board.size):
        for j in range(board.size):
            if board[i][j] != 0:
                score += weights[i%5][j%5] * board[i][j]
    return score
```

## 性能优化

### 1. 移动排序

对可能的移动进行排序，优先考虑更有可能的好移动：

```python
def sort_moves(board, moves):
    move_scores = []
    for move in moves:
        score = quick_evaluate(board, move)
        move_scores.append((move, score))
    return [m for m, s in sorted(move_scores, key=lambda x: x[1], reverse=True)]
```

### 2. 缓存优化

使用置换表存储已经计算过的局面：

```python
from functools import lru_cache

@lru_cache(maxsize=1000000)
def get_cached_evaluation(board_hash):
    return evaluate_position(board_from_hash(board_hash))
```

### 3. 并行搜索

在较深层次使用多线程搜索：

```python
from concurrent.futures import ThreadPoolExecutor

def parallel_search(board, depth):
    moves = get_valid_moves(board)
    with ThreadPoolExecutor() as executor:
        futures = []
        for move in moves:
            new_board = board_after_move(board, move)
            futures.append(executor.submit(alpha_beta, new_board, 
                                         depth-1, float('-inf'), float('inf'), 2))
        results = [f.result() for f in futures]
    return moves[results.index(max(results))]
```

## 难度级别

### 简单模式
- 搜索深度：2
- 简化评估函数
- 不使用高级优化

### 中等模式
- 搜索深度：4
- 完整评估函数
- 使用Alpha-Beta剪枝

### 困难模式
- 搜索深度：6+
- 高级评估函数
- 所有优化方法
- 开局库支持

## 调试与测试

### 性能分析

```python
import cProfile

def profile_ai():
    board = Board()
    profiler = cProfile.Profile()
    profiler.enable()
    ai.get_move(board, 1)
    profiler.disable()
    profiler.print_stats(sort='time')
```

### 单元测试

```python
def test_evaluation():
    board = Board()
    # 测试基本局面
    assert evaluate_position(board) == 0
    
    # 测试胜利局面
    board.place_piece(7, 7, 1)
    board.place_piece(7, 8, 1)
    board.place_piece(7, 9, 1)
    board.place_piece(7, 10, 1)
    board.place_piece(7, 11, 1)
    assert evaluate_position(board) > 90000
```

## 进阶优化

1. 开局库
2. 终局数据库
3. 模式识别
4. 蒙特卡洛树搜索

## 常见问题

1. 搜索深度与性能平衡
2. 评估函数调优
3. 内存管理
4. 超时处理

## 参考资源

1. [极小化极大算法介绍](https://en.wikipedia.org/wiki/Minimax)
2. [Alpha-Beta剪枝优化](https://en.wikipedia.org/wiki/Alpha-beta_pruning)
3. [五子棋AI论文集](https://github.com/gomoku/papers)