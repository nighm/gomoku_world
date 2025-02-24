"""Constants for AI and network configurations.

AI和网络配置的常量。
"""

# AI settings / AI设置
AI_THINKING_TIME = 5.0  # Maximum thinking time in seconds / AI最大思考时间（秒）
AI_CACHE_SIZE = 100000  # Maximum number of cached positions / 最大缓存局面数量
AI_DEPTH_EASY = 2      # Search depth for easy difficulty / 简单难度的搜索深度
AI_DEPTH_MEDIUM = 4    # Search depth for medium difficulty / 中等难度的搜索深度
AI_DEPTH_HARD = 6      # Search depth for hard difficulty / 困难难度的搜索深度

# Network settings / 网络设置
NETWORK_CHECK_TIMEOUT = 5.0  # Network check timeout in seconds / 网络检查超时时间（秒）
NETWORK_RETRY_INTERVAL = 1.0  # Retry interval in seconds / 重试间隔时间（秒）
NETWORK_MAX_RETRIES = 3      # Maximum number of retries / 最大重试次数

# Debug settings / 调试设置
DEBUG_ENABLED = True         # Enable debug mode / 启用调试模式
DEBUG_LOG_LEVEL = "DEBUG"    # Debug log level / 调试日志级别