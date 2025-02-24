"""Default configuration values.
默认配置值。
"""

GAME_DEFAULTS = {
    "board": {
        "size": 15,
        "win_count": 5
    },
    "display": {
        "theme": "light",
        "animations_enabled": True,
        "window_size": {
            "width": 800,
            "height": 600
        }
    },
    "sound": {
        "enabled": True,
        "volume": 50
    },
    "ai": {
        "difficulty": "medium",
        "search_depth": 3
    },
    "debug": {
        "enabled": False,
        "log_level": "INFO"
    },
    "test": {
        "string": "value",
        "integer": 42,
        "float": 3.14,
        "boolean": True,
        "nested": {
            "key": "value"
        }
    }
}

I18N_DEFAULTS = {
    "default_language": "en",
    "fallback_language": "en",
    "cache_enabled": True,
    "cache_ttl": 3600,
    "online_features_enabled": True
}

__all__ = ["GAME_DEFAULTS", "I18N_DEFAULTS"]