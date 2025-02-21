import os
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import Update
from aiologger import Logger
from aiologger.handlers.files import AsyncFileHandler


class AsyncLoggingMiddleware(BaseMiddleware):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        log_dir = os.path.abspath("app/data/logs")
        os.makedirs(log_dir, exist_ok=True)

        self.debug_logger = Logger.with_default_handlers(name="debug_logger")
        self.info_logger = Logger.with_default_handlers(name="info_logger")
        self.error_logger = Logger.with_default_handlers(name="error_logger")

        self.debug_logger.add_handler(
            AsyncFileHandler(os.path.join(log_dir, "debug.log")))
        self.info_logger.add_handler(
            AsyncFileHandler(os.path.join(log_dir, "info.log")))
        self.error_logger.add_handler(
            AsyncFileHandler(os.path.join(log_dir, "error.log")))

    async def __call__(self, handler, event, data):
        if isinstance(event, Update):
            await self.debug_logger.debug(self._format_message("DEBUG", f"Received update: {event}"))

        try:
            return await handler(event, data)

        except Exception as e:
            await self.error_logger.error(self._format_message("ERROR", f"Error while processing event: {e}"), exc_info=True)
            raise e

    async def log(self, level: str, message: str):
        """Logs a message at a specific level asynchronously.
        Args:
            level (str): Logging level (debug, info, error).
            message (str): Logging message.
        """

        level = level.lower()
        formatted_message = self._format_message(level.upper(), message)

        if level == "debug":
            await self.debug_logger.debug(formatted_message)
        elif level == "info":
            await self.info_logger.info(formatted_message)
        elif level == "error":
            await self.error_logger.error(formatted_message)
        else:
            await self.error_logger.warning(self._format_message("WARNING", f"Unknown log level: {level} - {message}"))

    def _format_message(self, level: str, message: str) -> str:
        """Formats the log message to include logging date, level and message."""

        return f"{datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]} [{level}] {message}"
