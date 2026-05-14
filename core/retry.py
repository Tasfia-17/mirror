"""Retry utilities with exponential backoff."""
import time
import functools
from typing import Callable, TypeVar, Any

T = TypeVar("T")


def with_retry(max_attempts: int = 3, base_delay: float = 1.0,
               backoff_factor: float = 2.0, exceptions: tuple = (Exception,)):
    """Decorator that retries a function with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts before raising.
        base_delay: Initial delay in seconds between retries.
        backoff_factor: Multiplier applied to delay after each attempt.
        exceptions: Tuple of exception types to catch and retry.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = base_delay
            last_exc = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        delay *= backoff_factor
            raise last_exc
        return wrapper
    return decorator
