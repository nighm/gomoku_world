"""AI configuration constants.

AI配置常量。
"""

# AI思考时间限制（秒）
AI_THINKING_TIME = 5.0

# AI缓存大小限制
AI_CACHE_SIZE = 100000

# AI搜索深度限制
AI_MAX_SEARCH_DEPTH = {
    "easy": 2,
    "medium": 3,
    "hard": 4
}

# AI评估分数权重
AI_EVALUATION_WEIGHTS = {
    "position": 1.0,
    "mobility": 0.8,
    "threat": 1.2,
    "defense": 1.0
}

__all__ = [
    "AI_THINKING_TIME",
    "AI_CACHE_SIZE",
    "AI_MAX_SEARCH_DEPTH",
    "AI_EVALUATION_WEIGHTS"
]