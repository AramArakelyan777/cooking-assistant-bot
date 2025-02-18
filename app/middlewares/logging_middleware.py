import logging
import os
from aiogram import BaseMiddleware
from aiogram.types import Update


class LoggingMiddleware(BaseMiddleware):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        self.logger = logging.getLogger("bot_logger")
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s] %(message)s"
        )

        log_dir = os.path.abspath("app/data/logs")
        os.makedirs(log_dir, exist_ok=True)

        self.debug_handler = logging.FileHandler(os.path.join(log_dir, "debug.log"))
        self.debug_handler.setLevel(logging.DEBUG)
        self.debug_handler.addFilter(lambda record: record.levelno == logging.DEBUG)
        self.info_handler = logging.FileHandler(os.path.join(log_dir, "info.log"))
        self.info_handler.setLevel(logging.INFO)
        self.info_handler.addFilter(lambda record: record.levelno == logging.INFO)
        self.error_handler = logging.FileHandler(os.path.join(log_dir, "error.log"))
        self.error_handler.setLevel(logging.ERROR)

        self.debug_handler.setFormatter(formatter)
        self.info_handler.setFormatter(formatter)
        self.error_handler.setFormatter(formatter)

        self.logger.addHandler(self.debug_handler)
        self.logger.addHandler(self.info_handler)
        self.logger.addHandler(self.error_handler)

    async def __call__(self, handler, event, data):
        if isinstance(event, Update):
            self.logger.debug(f"Received update: {event}")

        try:
            return await handler(event, data)
        except Exception as e:
            self.logger.error(f"Error while processing event: {e}", exc_info=True)
            raise e

    def log(self, level, message):
        """Utility function to log messages at different levels"""

        if level == "debug":
            self.logger.debug(message)
        elif level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        else:
            self.logger.warning(f"Unknown log level: {level} - {message}")
