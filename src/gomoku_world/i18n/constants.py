"""
Internationalization constants
国际化常量
"""

from typing import Dict, List

# Standard language codes (ISO 639-1)
LANGUAGE_CODES = {
    "en": {
        "name": "English",
        "native_name": "English",
        "fallbacks": ["en-US", "en-GB"]
    },
    "zh": {
        "name": "Chinese",
        "native_name": "中文",
        "fallbacks": ["zh-CN", "zh-TW"]
    },
    "ja": {
        "name": "Japanese",
        "native_name": "日本語",
        "fallbacks": ["ja-JP"]
    },
    "ko": {
        "name": "Korean",
        "native_name": "한국어",
        "fallbacks": ["ko-KR"]
    }
}

# Region codes (ISO 3166-1)
REGION_CODES = {
    "CN": "China",
    "TW": "Taiwan",
    "HK": "Hong Kong",
    "JP": "Japan",
    "KR": "Korea",
    "US": "United States",
    "GB": "United Kingdom"
}

# Default language settings
DEFAULT_LANGUAGE = "en"
DEFAULT_REGION = "US"
FALLBACK_LANGUAGE = "en"

# Resource categories
RESOURCE_CATEGORIES = [
    "common",    # Common texts
    "game",      # Game-related texts
    "ui",        # UI elements
    "error",     # Error messages
    "help",      # Help texts
    "tutorial"   # Tutorial texts
]

# Date and time formats
DATE_FORMATS = {
    "en": "%Y-%m-%d",
    "zh": "%Y年%m月%d日",
    "ja": "%Y年%m月%d日",
    "ko": "%Y년%m월%d일"
}

TIME_FORMATS = {
    "en": "%H:%M:%S",
    "zh": "%H时%M分%S秒",
    "ja": "%H時%M分%S秒",
    "ko": "%H시%M분%S초"
}

# Number formats
NUMBER_FORMATS = {
    "en": {"decimal": ".", "thousands": ","},
    "zh": {"decimal": ".", "thousands": ","},
    "ja": {"decimal": ".", "thousands": ","},
    "ko": {"decimal": ".", "thousands": ","}
}

# Character sets
CHAR_SETS = {
    "en": "latin",
    "zh": "cjk",
    "ja": "cjk",
    "ko": "cjk"
}

# Font families
FONT_FAMILIES = {
    "latin": ["Arial", "Helvetica", "sans-serif"],
    "cjk": ["Microsoft YaHei", "SimHei", "sans-serif"]
} 