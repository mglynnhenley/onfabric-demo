"""Shared utilities for API clients."""

import asyncio
from typing import Any, Callable, TypeVar
from fabric_dashboard.utils import logger

T = TypeVar("T")


async def retry_with_backoff(
    coro_func: Callable[..., Any],
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
) -> T:
    """
    Retry async function with exponential backoff.

    Args:
        coro_func: Async function to retry.
        max_attempts: Maximum retry attempts.
        initial_delay: Initial delay in seconds.
        backoff_factor: Multiplier for each retry.

    Returns:
        Result from successful call.

    Raises:
        Last exception if all retries fail.
    """
    delay = initial_delay

    for attempt in range(max_attempts):
        try:
            return await coro_func()
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"All {max_attempts} attempts failed: {e}")
                raise

            logger.warning(
                f"Attempt {attempt + 1}/{max_attempts} failed: {e}. "
                f"Retrying in {delay}s..."
            )
            await asyncio.sleep(delay)
            delay *= backoff_factor


class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class RateLimitError(APIError):
    """Raised when API rate limit is exceeded."""

    pass


class AuthenticationError(APIError):
    """Raised when API authentication fails."""

    pass
