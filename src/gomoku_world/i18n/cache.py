"""
Translation cache implementation.

翻译缓存实现。

This module provides a memory-based cache implementation for translations with:
- Size limit to prevent memory leaks
- Time-to-live (TTL) for entries
- Thread-safe operations
- Automatic cleanup of expired entries

本模块提供基于内存的翻译缓存实现，具有：
- 大小限制以防止内存泄漏
- 条目生存时间（TTL）
- 线程安全操作
- 自动清理过期条目
"""

import time
import threading
from typing import Dict, Optional, Tuple, Any
from .base import TranslationCache, TranslationKey, TranslationValue
from .exceptions import CacheError

class MemoryCache(TranslationCache):
    """
    Memory-based translation cache with TTL and size limit.
    具有TTL和大小限制的基于内存的翻译缓存。
    """
    
    def __init__(self, max_size: int = 1000, ttl: int = 3600):
        """
        Initialize translation cache.
        初始化翻译缓存。
        
        Args:
            max_size (int): Maximum number of entries in cache
                           缓存中的最大条目数
            ttl (int): Time to live in seconds for cache entries
                      缓存条目的生存时间（秒）
        """
        self._cache: Dict[TranslationKey, Tuple[TranslationValue, float]] = {}
        self._max_size = max_size
        self._ttl = ttl
        self._lock = threading.RLock()
        
    def get(self, key: TranslationKey) -> Optional[TranslationValue]:
        """
        Get a value from cache.
        从缓存获取值。
        
        Args:
            key (TranslationKey): Cache key
                                缓存键
            
        Returns:
            Optional[TranslationValue]: Cached value if exists and not expired, None otherwise
                                      如果存在且未过期则返回缓存的值，否则返回None
        """
        with self._lock:
            if key not in self._cache:
                return None
                
            value, timestamp = self._cache[key]
            if time.time() - timestamp > self._ttl:
                del self._cache[key]
                return None
                
            return value

    def set(self, key: TranslationKey, value: TranslationValue) -> None:
        """
        Set a value in cache.
        在缓存中设置值。
        
        Args:
            key (TranslationKey): Cache key
                                缓存键
            value (TranslationValue): Value to cache
                                    要缓存的值
                                    
        Raises:
            ValueError: If value is not a string
                       如果值不是字符串
        """
        if not isinstance(value, str):
            raise ValueError(f"Cache value must be a string, got {type(value)}")
            
        with self._lock:
            self._cleanup_if_needed()
            self._cache[key] = (value, time.time())

    def remove(self, key: TranslationKey) -> None:
        """
        Remove a specific entry from cache.
        从缓存中移除特定条目。
        
        Args:
            key (TranslationKey): Cache key to remove
                                要移除的缓存键
        """
        with self._lock:
            self._cache.pop(key, None)

    def clear(self) -> None:
        """
        Clear all entries from cache.
        清除缓存中的所有条目。
        """
        with self._lock:
            self._cache.clear()

    def _cleanup_if_needed(self) -> None:
        """
        Clean up expired entries if cache is full.
        如果缓存已满，清理过期条目。
        """
        if len(self._cache) < self._max_size:
            return
            
        now = time.time()
        # Remove expired entries
        expired = [k for k, (_, ts) in self._cache.items() 
                  if now - ts > self._ttl]
        for k in expired:
            del self._cache[k]
            
        # If still at max size, remove oldest entries
        if len(self._cache) >= self._max_size:
            sorted_items = sorted(self._cache.items(), key=lambda x: x[1][1])
            to_remove = len(self._cache) - self._max_size + 1
            for k, _ in sorted_items[:to_remove]:
                del self._cache[k] 