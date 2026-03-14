import logging
import logging.config
import functools
from typing import Callable, Any
from src.logging_tools.config import LOGGING_CONFIG

class LoggingManager:
    _initialized = False
    logger = logging.getLogger("TaskScheduler")

    @classmethod
    def setup(cls):
        if not cls._initialized:
            logging.config.dictConfig(LOGGING_CONFIG)
            cls._initialized = True
            cls.logger.info("=== Configuration of logging tools is done ===")

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

    @staticmethod
    def log_task_sources(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cls_name = args[0].__class__.__name__ if args else "unknown"

            LoggingManager.logger.info(f"Started collecting tasks from {cls_name}...")
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                LoggingManager.logger.error(f"Exception in source {cls_name}: {e}")
                raise

        return wrapper