"""Caching utilities for fabric_dashboard using DiskCache."""

import hashlib
from pathlib import Path
from typing import Any, Optional

from diskcache import Cache

from fabric_dashboard.utils.config import get_config_dir

# Cache directory
CACHE_DIR = get_config_dir() / "cache"

# Default TTL (Time To Live) in seconds
DEFAULT_TTL = 30 * 60  # 30 minutes


class SearchCache:
    """Cache for Perplexity search results."""

    def __init__(self, ttl: int = DEFAULT_TTL):
        """
        Initialize search cache.

        Args:
            ttl: Time to live in seconds (default: 30 minutes).
        """
        self.ttl = ttl
        self.cache_dir = CACHE_DIR
        self._ensure_cache_dir()
        self._cache: Optional[Cache] = None

    def _ensure_cache_dir(self) -> None:
        """Ensure cache directory exists."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @property
    def cache(self) -> Cache:
        """Get or create cache instance."""
        if self._cache is None:
            self._cache = Cache(str(self.cache_dir))
        return self._cache

    def _make_key(self, query: str) -> str:
        """
        Create a cache key from a search query.

        Args:
            query: Search query string.

        Returns:
            Hashed cache key.
        """
        # Use SHA256 hash of query as key
        return hashlib.sha256(query.encode()).hexdigest()

    def get(self, query: str) -> Optional[Any]:
        """
        Get cached result for a query.

        Args:
            query: Search query string.

        Returns:
            Cached result if found and not expired, None otherwise.
        """
        key = self._make_key(query)
        return self.cache.get(key)

    def set(self, query: str, result: Any) -> None:
        """
        Cache a search result.

        Args:
            query: Search query string.
            result: Result to cache.
        """
        key = self._make_key(query)
        self.cache.set(key, result, expire=self.ttl)

    def has(self, query: str) -> bool:
        """
        Check if query result is cached.

        Args:
            query: Search query string.

        Returns:
            True if cached and not expired, False otherwise.
        """
        key = self._make_key(query)
        return key in self.cache

    def clear(self) -> None:
        """Clear all cached results."""
        self.cache.clear()

    def delete(self, query: str) -> bool:
        """
        Delete a specific cached result.

        Args:
            query: Search query string.

        Returns:
            True if deleted, False if not found.
        """
        key = self._make_key(query)
        return self.cache.delete(key)

    def stats(self) -> dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dictionary with cache stats.
        """
        return {
            "size": len(self.cache),
            "volume": self.cache.volume(),
            "directory": str(self.cache_dir),
        }

    def close(self) -> None:
        """Close cache connection."""
        if self._cache:
            self._cache.close()
            self._cache = None

    def __enter__(self) -> "SearchCache":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close cache."""
        self.close()


# Global cache instance (lazy initialization)
_global_cache: Optional[SearchCache] = None


def get_cache(ttl: int = DEFAULT_TTL) -> SearchCache:
    """
    Get global cache instance.

    Args:
        ttl: Time to live in seconds (default: 30 minutes).

    Returns:
        SearchCache instance.
    """
    global _global_cache
    if _global_cache is None:
        _global_cache = SearchCache(ttl=ttl)
    return _global_cache


def cache_search_result(query: str, result: Any) -> None:
    """
    Cache a search result using global cache.

    Args:
        query: Search query string.
        result: Result to cache.
    """
    cache = get_cache()
    cache.set(query, result)


def get_cached_search_result(query: str) -> Optional[Any]:
    """
    Get cached search result using global cache.

    Args:
        query: Search query string.

    Returns:
        Cached result if found, None otherwise.
    """
    cache = get_cache()
    return cache.get(query)


def clear_cache() -> None:
    """Clear all cached search results."""
    cache = get_cache()
    cache.clear()
