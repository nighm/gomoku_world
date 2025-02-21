.. _configuration:

Configuration Guide
=================

This section details the configuration options for Gomoku World.

Basic Configuration
-----------------

1. Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Main environment variables configuration (.env file)::

    # Application Settings
    APP_ENV=development        # Environment type (development/production)
    DEBUG=True                 # Debug mode
    SECRET_KEY=your-secret-key # Secret key
    
    # Database Settings
    DB_HOST=localhost         # Database host
    DB_PORT=5432             # Database port
    DB_NAME=gomoku           # Database name
    DB_USER=postgres         # Database user
    DB_PASSWORD=secret       # Database password
    
    # Redis Settings
    REDIS_HOST=localhost     # Redis host
    REDIS_PORT=6379         # Redis port
    
    # Network Settings
    HOST=localhost          # Listen address
    PORT=5000              # Listen port

2. Application Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Application configuration file (config/settings.py)::

    # Package Information
    PACKAGE_NAME = "Gomoku World"
    VERSION = "1.0.0"
    
    # Directory Configuration
    ROOT_DIR = Path(__file__).parent.parent.parent
    RESOURCES_DIR = ROOT_DIR / "resources"
    LOG_DIR = ROOT_DIR / "logs"
    SAVE_DIR = ROOT_DIR / "saves"
    
    # Game Settings
    BOARD_SIZE = 15
    WIN_LENGTH = 5
    
    # Resource Settings
    DEFAULT_THEME = "light"
    DEFAULT_LANGUAGE = "en"

Game Configuration
---------------

1. AI Configuration
~~~~~~~~~~~~~~~~

AI-related configuration::

    # AI Difficulty Levels
    AI_DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
    DEFAULT_AI_DIFFICULTY = "medium"
    
    # AI Performance Settings
    AI_THINKING_TIME = 2.0  # Thinking time (seconds)
    AI_CACHE_SIZE = 1000    # Cache size

2. Save Configuration
~~~~~~~~~~~~~~~~~~

Save system configuration::

    # Auto Save Settings
    AUTO_SAVE_INTERVAL = 5  # Auto save interval (minutes)
    MAX_AUTO_SAVES = 5      # Maximum auto saves
    MAX_SAVE_FILES = 100    # Maximum save files
    SAVE_FILE_FORMAT = "json"  # Save format

3. Leaderboard Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

Ranking system configuration::

    # Ranking Settings
    INITIAL_RATING = 1500    # Initial score
    K_FACTOR = 32           # K factor
    RATING_FLOOR = 100      # Minimum score
    
    # Score Changes
    RATING_CHANGES = {
        "win": 25,
        "loss": -20,
        "draw": 5
    }
    
    # Leaderboard Categories
    LEADERBOARD_CATEGORIES = ["rating", "wins", "streak"]
    LEADERBOARD_LIMIT = 100  # Leaderboard display limit

Network Configuration
------------------

1. Server Configuration
~~~~~~~~~~~~~~~~~~~~

Server-related configuration::

    # Network Settings
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 5000
    
    # Connection Settings
    MAX_CONNECTIONS = 1000    # Maximum connections
    TIMEOUT = 30             # Timeout (seconds)
    KEEPALIVE = True         # Keep connection alive
    
    # Protocol Settings
    PROTOCOL_VERSION = "1.0"
    COMPRESSION = True       # Enable compression
    ENCRYPTION = True        # Enable encryption

2. Spectator Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Spectator system configuration::

    # Spectator Settings
    MAX_SPECTATORS_PER_GAME = 50     # Maximum spectators per game
    SPECTATOR_UPDATE_INTERVAL = 1.0   # Update interval (seconds)
    SPECTATOR_CHAT_ENABLED = True     # Enable spectator chat
    SPECTATOR_CHAT_HISTORY = 100      # Chat history size

    # Spectator Features
    SPECTATOR_FEATURES = {
        "chat": True,           # Chat functionality
        "game_info": True,      # Game information
        "player_stats": True,   # Player statistics
        "move_history": True    # Move history
    }

Logging Configuration
------------------

1. Log Settings
~~~~~~~~~~~~

Logging system configuration::

    # Log Format
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL = "INFO"
    LOG_FILE = LOG_DIR / "gomoku_world.log"
    
    # Log Handlers
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

2. Monitoring Configuration
~~~~~~~~~~~~~~~~~~~~~~~

Performance monitoring configuration::

    # Metrics Collection
    METRICS_ENABLED = True
    METRICS_PORT = 9090
    
    # Tracing Settings
    TRACING_ENABLED = True
    TRACING_SAMPLE_RATE = 0.1
    
    # Health Check
    HEALTH_CHECK_INTERVAL = 60  # seconds
    HEALTH_CHECK_TIMEOUT = 5    # seconds

Security Configuration
-------------------

1. Security Settings
~~~~~~~~~~~~~~~~~

Basic security configuration::

    # Session Settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # CSRF Protection
    CSRF_ENABLED = True
    CSRF_SECRET_KEY = "your-csrf-key"
    
    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = "redis://localhost:6379/0"
    
    # Maximum Requests per Minute
    RATELIMIT_DEFAULT = "100/minute"
    RATELIMIT_STRATEGY = "moving-window"

2. Authentication Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authentication-related configuration::

    # Authentication Settings
    AUTH_REQUIRED = True
    AUTH_TOKEN_EXPIRY = 3600  # 1 hour
    
    # Password Policy
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_SPECIAL = True
    PASSWORD_REQUIRE_NUMBERS = True
    
    # OAuth Settings
    OAUTH_PROVIDERS = {
        "google": {
            "client_id": "your-client-id",
            "client_secret": "your-client-secret"
        }
    }

Development Configuration
----------------------

1. Development Tools
~~~~~~~~~~~~~~~~~

Development environment configuration::

    # Debug Tools
    DEBUG_TOOLBAR_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    
    # Test Settings
    TESTING = False
    TEST_DATABASE_URI = "sqlite:///:memory:"
    
    # Documentation Settings
    SWAGGER_ENABLED = True
    SWAGGER_UI_DOC_EXPANSION = "list"

2. Build Settings
~~~~~~~~~~~~~~

Build-related configuration::

    # Build Options
    BUILD_NUMBER = "dev"
    BUILD_DATE = "2024-01-01"
    BUILD_COMMIT = "HEAD"
    
    # Package Settings
    PACKAGE_EXCLUDE = [
        "*.pyc",
        "__pycache__",
        "*.swp",
        ".git"
    ]
    
    # Resource Compilation
    COMPILE_RESOURCES = True
    MINIFY_JS = True
    MINIFY_CSS = True 