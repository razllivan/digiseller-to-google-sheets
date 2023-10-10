import sys
import time
from functools import wraps

from loguru import logger


def retry_intervals(*intervals):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i, interval in enumerate(intervals):
                try:
                    return func(*args, **kwargs)
                except Exception:  # noqa
                    logger.warning(f"An error occurred, "
                                   f"Retry after {interval} seconds...")
                    time.sleep(interval)
            logger.critical('Forced termination, number of attempts exceeded.')
            sys.exit(1)

        return wrapper

    return decorator
