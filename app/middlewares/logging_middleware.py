import logging
from aiogram import BaseMiddleware
from aiogram.types import Update


class LoggingMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        self.debug_handler = logging.FileHandler("app/data/logs/debug.log")
        self.debug_handler.setLevel(logging.DEBUG)
        self.info_handler = logging.FileHandler("app/data/logs/info.log")
        self.info_handler.setLevel(logging.INFO)
        self.error_handler = logging.FileHandler("app/data/logs/error.log")
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
