"""
Retry decorator for flaky operations.

Usage:
    @retry(times=3, delay=1.0, exceptions=(TimeoutError,))
    def flaky_operation():
        ...
"""
from __future__ import annotations

import time
import logging
from functools import wraps
from typing import Callable, Type, Tuple, Any

logger = logging.getLogger("automation")


def retry(
    times: int = 3,
    delay: float = 1.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
) -> Callable:
    """
    Decorator that retries a function up to `times` on specified exceptions.

    Args:
        times:      Maximum number of attempts (default 3)
        delay:      Seconds to wait between attempts (default 1.0)
        exceptions: Tuple of exception types to catch and retry on
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exception = exc
                    logger.warning(
                        f"Attempt {attempt}/{times} failed for '{func.__name__}': {exc}"
                    )
                    if attempt < times:
                        time.sleep(delay)
            raise last_exception  # type: ignore[misc]
        return wrapper
    return decorator
