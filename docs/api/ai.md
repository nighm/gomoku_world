# AI 模块 API 文档

## 概述

本文档详细说明了五子棋AI模块的接口设计和使用方法。AI模块提供了智能对手的核心功能实现。

## 核心类

### AI

主要的AI玩家类，实现了智能对手的核心功能。

#### 构造函数

```python
def __init__(self, difficulty: str = "medium")
```

**参数：**
- difficulty: AI难度级别，可选值：
  - "easy": 简单
  - "medium": 中等
  - "hard": 困难

#### 方法

##### get_move

```python
def get_move(self, board: Board, player: int) -> Tuple[int, int]
```

获取AI的下一步最佳移动。

**参数：**
- board: 当前棋盘状态
- player: 当前玩家（1为黑棋，2为白棋）

**返回：**
- Tuple[int, int]: 最佳移动的行列坐标

**异常：**
- RuntimeError: 当没有有效移动时抛出

##### set_difficulty

```python
def set_difficulty(self, difficulty: str)
```

设置AI难度级别。

**参数：**
- difficulty: 新的难度级别（"easy"、"medium"、"hard"）

### AIStrategy

AI策略管理类，负责难度级别和时间控制。

#### 构造函数

```python
def __init__(self, difficulty: str = "medium")
```

**参数：**
- difficulty: AI难度级别

#### 方法

##### get_move_priority

```python
def get_move_priority(self, board: Board, x: int, y: int) -> float
```

计算移动的优先级分数。

**参数：**
- board: 当前棋盘状态
- x: X坐标
- y: Y坐标

**返回：**
- float: 移动的优先级分数

### AISearch

AI搜索系统类，实现了极小化极大算法。

#### 构造函数

```python
def __init__(self, strategy: AIStrategy, evaluation: AIEvaluation)
```

**参数：**
- strategy: 策略管理器
- evaluation: 评估系统

#### 方法

##### get_best_move

```python
def get_best_move(self, board: Board, player: int) -> Tuple[int, int]
```

使用极小化极大算法获取最佳移动。

**参数：**
- board: 当前棋盘状态
- player: 当前玩家

**返回：**
- Tuple[int, int]: 最佳移动坐标

### AICache

AI缓存管理类，用于优化性能。

#### 构造函数

```python
def __init__(self, max_size: int = 100000)
```

**参数：**
- max_size: 最大缓存局面数量

#### 方法

##### get_best_move

```python
def get_best_move(self, board: Board, player: int) -> Optional[Tuple[int, int]]
```

从缓存获取最佳移动。

**参数：**
- board: 当前棋盘状态
- player: 当前玩家

**返回：**
- Optional[Tuple[int, int]]: 缓存的最佳移动，如果不存在则返回None

## 使用示例

```python
from gomoku_world.core.ai import AI
from gomoku_world.core.board import Board

# 创建15x15棋盘
board = Board(15)

# 创建AI实例（中等难度）
ai = AI(difficulty="medium")

# 获取AI的下一步移动（假设AI执黑）
row, col = ai.get_move(board, player=1)

# 在棋盘上落子
board.place_piece(row, col, 1)

# 调整AI难度
ai.set_difficulty("hard")
```

## 注意事项

1. AI的思考时间会随难度级别增加而增加
2. 建议在单独的线程中运行AI，避免阻塞主线程
3. 可以通过缓存机制优化性能
4. 高难度级别下内存占用较大