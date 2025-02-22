# 五子棋规则和基本概念 / Game Rules and Core Concepts

## 游戏概述 / Game Overview

五子棋是一种两人对弈的棋类游戏，玩家轮流在棋盘上放置棋子，先将五个或更多棋子连成一线的玩家获胜。

### 基本规则 / Basic Rules

1. 棋盘：标准 15×15 格
2. 棋子：黑白两色
3. 回合：黑先白后，轮流落子
4. 胜利条件：形成五子连珠（横、竖、斜）

## 核心概念实现 / Core Concepts Implementation

### 1. 棋盘表示 / Board Representation

```python
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [[None] * size for _ in range(size)]
        self.current_player = Player.BLACK
        self.history = []
```

关键属性：
- `size`: 棋盘大小
- `board`: 二维数组表示棋盘状态
- `current_player`: 当前玩家
- `history`: 落子历史记录

### 2. 坐标系统 / Coordinate System

```python
class Position:
    def __init__(self, x: int, y: int):
        self.x = x  # 横坐标 (0-14)
        self.y = y  # 纵坐标 (0-14)

    def is_valid(self, board_size: int) -> bool:
        return 0 <= self.x < board_size and 0 <= self.y < board_size
```

### 3. 落子规则 / Move Rules

```python
def make_move(self, position: Position) -> bool:
    """尝试在指定位置落子"""
    if not self._is_valid_move(position):
        return False
    
    self.board[position.y][position.x] = self.current_player
    self.history.append(position)
    self._switch_player()
    return True
```

### 4. 胜负判定 / Win Condition

```python
def check_win(self, last_move: Position) -> bool:
    """检查最后一手是否形成胜局"""
    directions = [
        [(0, 1), (0, -1)],   # 垂直
        [(1, 0), (-1, 0)],   # 水平
        [(1, 1), (-1, -1)],  # 主对角线
        [(1, -1), (-1, 1)]   # 副对角线
    ]
    
    for dir_pair in directions:
        count = 1  # 当前位置的棋子
        for dx, dy in dir_pair:
            count += self._count_direction(last_move, dx, dy)
        if count >= 5:
            return True
    return False
```

## 游戏状态 / Game States

### 1. 玩家枚举 / Player Enumeration

```python
from enum import Enum

class Player(Enum):
    BLACK = 1
    WHITE = 2
```

### 2. 游戏状态 / Game State

```python
class GameState(Enum):
    ONGOING = 0
    BLACK_WIN = 1
    WHITE_WIN = 2
    DRAW = 3
```

## 高级规则变体 / Advanced Rule Variants

### 1. 禁手规则 / Forbidden Moves

在某些规则变体中，黑方有以下禁手：
- 长连：超过五子相连
- 双三：同时形成两个活三
- 双四：同时形成两个活四

```python
def check_forbidden_moves(self, position: Position) -> bool:
    """检查是否违反禁手规则"""
    if self.current_player != Player.BLACK:
        return False
        
    if self._check_overline(position):
        return True
    if self._check_double_three(position):
        return True
    if self._check_double_four(position):
        return True
    return False
```

### 2. 比赛规则 / Tournament Rules

- 计时规则
- 悔棋规则
- 判负条件

## 实战技巧 / Practical Tips

### 1. 基本棋型 / Basic Patterns

- 活四：\[ ○○○○\_ \]
- 冲四：\[ ○○○○× \]
- 活三：\[ \_○○○\_ \]
- 眠三：\[ ×○○○\_ \]

### 2. 开局策略 / Opening Strategies

- 天元开局
- 花月开局
- 星月开局

### 3. 进攻防守 / Attack and Defense

- 连续进攻
- 防守反击
- 局势判断

## 练习题 / Exercises

1. 实现基本的落子功能
2. 编写胜负判定算法
3. 添加禁手规则检查
4. 设计简单的 AI 对手

## 进阶学习 / Advanced Learning

1. AI 算法
   - 极大极小算法
   - Alpha-Beta 剪枝
   - 蒙特卡洛树搜索

2. 性能优化
   - 位运算优化
   - 缓存优化
   - 并行计算

## 参考资料 / References

1. [五子棋规则](https://en.wikipedia.org/wiki/Gomoku)
2. [竞赛规则](https://renjuoffline.com/rules.html)
3. [开发指南](../developer-guide.md)
4. [API 文档](../api-reference.md) 