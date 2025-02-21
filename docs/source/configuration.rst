.. _configuration:

配置指南
=======

本节详细介绍五子棋世界的配置选项。

基本配置
-------

1. 环境变量
~~~~~~~~~

主要的环境变量配置（.env文件）::

    # 应用设置
    APP_ENV=development        # 环境类型(development/production)
    DEBUG=True                 # 调试模式
    SECRET_KEY=your-secret-key # 密钥
    
    # 数据库设置
    DB_HOST=localhost         # 数据库主机
    DB_PORT=5432             # 数据库端口
    DB_NAME=gomoku           # 数据库名
    DB_USER=postgres         # 数据库用户
    DB_PASSWORD=secret       # 数据库密码
    
    # Redis设置
    REDIS_HOST=localhost     # Redis主机
    REDIS_PORT=6379         # Redis端口
    
    # 网络设置
    HOST=localhost          # 监听地址
    PORT=5000              # 监听端口

2. 应用配置
~~~~~~~~~

应用配置文件（config/settings.py）::

    # 包信息
    PACKAGE_NAME = "Gomoku World"
    VERSION = "1.0.0"
    
    # 目录配置
    ROOT_DIR = Path(__file__).parent.parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"
    LOG_DIR = ROOT_DIR / "logs"
    SAVE_DIR = ROOT_DIR / "saves"
    
    # 游戏设置
    BOARD_SIZE = 15
    WIN_LENGTH = 5
    
    # 资源设置
    DEFAULT_THEME = "light"
    DEFAULT_LANGUAGE = "en"

游戏配置
-------

1. AI配置
~~~~~~~~

AI相关配置::

    # AI难度级别
    AI_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
    DEFAULT_AI_DIFFICULTY = "medium"
    
    # AI性能设置
    AI_THINKING_TIME = 2.0  # 思考时间(秒)
    AI_CACHE_SIZE = 1000    # 缓存大小

2. 存档配置
~~~~~~~~~

存档系统配置::

    # 自动保存设置
    AUTO_SAVE_INTERVAL = 5  # 自动保存间隔(分钟)
    MAX_AUTO_SAVES = 5      # 最大自动存档数
    MAX_SAVE_FILES = 100    # 最大存档文件数
    SAVE_FILE_FORMAT = "json"  # 存档格式

3. 排行榜配置
~~~~~~~~~~

排行系统配置::

    # 排名设置
    INITIAL_RATING = 1500    # 初始分数
    K_FACTOR = 32           # K因子
    RATING_FLOOR = 100      # 最低分数
    
    # 分数变化
    RATING_CHANGES = {
        "win": 25,
        "loss": -20,
        "draw": 5
    }
    
    # 排行榜类别
    LEADERBOARD_CATEGORIES = ["rating", "wins", "streak"]
    LEADERBOARD_LIMIT = 100  # 排行榜显示数量

网络配置
-------

1. 服务器配置
~~~~~~~~~~

服务器相关配置::

    # 网络设置
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 5000
    
    # 连接设置
    MAX_CONNECTIONS = 1000    # 最大连接数
    TIMEOUT = 30             # 超时时间(秒)
    KEEPALIVE = True         # 保持连接
    
    # 协议设置
    PROTOCOL_VERSION = "1.0"
    COMPRESSION = True       # 启用压缩
    ENCRYPTION = True        # 启用加密

2. 观战配置
~~~~~~~~~

观战系统配置::

    # 观战设置
    MAX_SPECTATORS_PER_GAME = 50     # 每局最大观战人数
    SPECTATOR_UPDATE_INTERVAL = 1.0   # 更新间隔(秒)
    SPECTATOR_CHAT_ENABLED = True     # 启用观战聊天
    SPECTATOR_CHAT_HISTORY = 100      # 聊天历史记录数

    # 观战功能
    SPECTATOR_FEATURES = {
        "chat": True,           # 聊天功能
        "game_info": True,      # 游戏信息
        "player_stats": True,   # 玩家统计
        "move_history": True    # 移动历史
    }

日志配置
-------

1. 日志设置
~~~~~~~~~

日志系统配置::

    # 日志格式
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    LOG_FILE = LOG_DIR / "gomoku_world.log"
    
    # 日志处理器
    LOG_HANDLERS = {
        "console": {
            "level": "INFO",
            "formatter": "standard"
        },
        "file": {
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "gomoku_world.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5
        }
    }

2. 监控配置
~~~~~~~~~

性能监控配置::

    # 指标收集
    METRICS_ENABLED = True
    METRICS_PORT = 9090
    
    # 追踪设置
    TRACING_ENABLED = True
    TRACING_SAMPLE_RATE = 0.1
    
    # 健康检查
    HEALTH_CHECK_INTERVAL = 60  # 秒
    HEALTH_CHECK_TIMEOUT = 5    # 秒

安全配置
-------

1. 安全设置
~~~~~~~~~

基本安全配置::

    # 会话设置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 86400  # 24小时
    
    # CSRF保护
    CSRF_ENABLED = True
    CSRF_SECRET_KEY = "your-csrf-key"
    
    # 速率限制
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "redis://localhost:6379/0"
    
    # 每分钟最大请求数
    RATELIMIT_DEFAULT = "100/minute"
    RATELIMIT_STRATEGY = "moving-window"

2. 认证配置
~~~~~~~~~

认证相关配置::

    # 认证设置
    AUTH_REQUIRED = True
    AUTH_TOKEN_EXPIRY = 3600  # 1小时
    
    # 密码策略
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_SPECIAL = True
    PASSWORD_REQUIRE_NUMBERS = True
    
    # OAuth设置
    OAUTH_PROVIDERS = {
        "google": {
            "client_id": "your-client-id",
            "client_secret": "your-client-secret"
        }
    }

开发配置
-------

1. 开发工具
~~~~~~~~~

开发环境配置::

    # 调试工具
    DEBUG_TOOLBAR_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # 测试设置
    TESTING = False
    TEST_DATABASE_URI = "sqlite:///:memory:"
    
    # 文档设置
    SWAGGER_ENABLED = True
    SWAGGER_UI_DOC_EXPANSION = "list"

2. 构建设置
~~~~~~~~~

构建相关配置::

    # 构建选项
    BUILD_NUMBER = "dev"
    BUILD_DATE = "2024-01-01"
    BUILD_COMMIT = "HEAD"
    
    # 打包设置
    PACKAGE_EXCLUDE = [
        "*.pyc",
        "__pycache__",
        "*.swp",
        ".git"
    ]
    
    # 资源编译
    COMPILE_RESOURCES = True
    MINIFY_JS = True
    MINIFY_CSS = True 