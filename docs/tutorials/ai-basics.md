# AI 算法基础 / AI Algorithm Basics

## 概述 / Overview

本文档介绍五子棋AI的核心算法实现，包括评估函数、搜索算法、难度级别设计等关键技术。

## 评估函数 / Evaluation Function

### 局面评估 / Position Evaluation

评估函数通过分析以下因素计算局面分数：
- 连子数量（2连、3连、4连、5连）
- 活度（两端是否被封堵）
- 位置权重（中心位置权重较高）
- 威胁度（对手形成威胁的程度）

### 实现示例 / Implementation Example

```python
def evaluate_position(board, player):
    score = 0
    # 检查所有方向的连子
    for direction in DIRECTIONS:
        score += check_line(board, player, direction)
    # 考虑位置权重
    score += evaluate_position_weight(board, player)
    return score
```

## 搜索算法 / Search Algorithm

### 极小化极大算法 / MinMax Algorithm

使用带α-β剪枝的极小化极大算法进行搜索：
1. 搜索深度由难度级别决定
2. 使用α-β剪枝优化搜索效率
3. 实现时间限制控制

### 移动排序 / Move Ordering

通过以下策略优化移动顺序：
1. 优先考虑靠近最后落子的位置
2. 优先考虑中心区域
3. 根据历史启发信息排序

## 难度级别 / Difficulty Levels

### 简单 / Easy
- 搜索深度：2层
- 评估函数简化
- 随机性较大

### 中等 / Medium
- 搜索深度：3-4层
- 完整评估函数
- 适度随机性

### 困难 / Hard
- 搜索深度：4-6层
- 优化的评估函数
- 最小随机性

## 性能优化 / Performance Optimization

### 缓存优化 / Cache Optimization
1. 局面缓存
2. 评估结果缓存
3. 最佳移动缓存

### 算法优化 / Algorithm Optimization
1. 迭代加深
2. 历史启发
3. 置换表

## 使用示例 / Usage Example

```python
from gomoku_world.core.ai import AI

# 创建AI实例
ai = AI(difficulty="medium")

# 获取AI的下一步移动
row, col = ai.get_move(board, player)

# 调整AI难度
ai.set_difficulty("hard")
```

## 进阶主题 / Advanced Topics

### 开局库 / Opening Book
- 常用开局模式
- 开局库的实现和使用

### 终局库 / Endgame Database
- 特殊终局模式识别
- 终局库的构建方法

### 自学习 / Self-Learning
- 基于对弈数据的优化
- 参数自动调整