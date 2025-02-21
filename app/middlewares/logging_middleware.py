from aiogram import BaseMiddleware
from aiogram.types import Update
from aiologger import Logger


class AsyncLoggingMiddleware(BaseMiddleware):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_logger()
        return cls._instance

    def _init_logger(self):
        self.async_logger = Logger.with_default_handlers(
            name="async_bot_logger")

    async def __call__(self, handler, event, data):
        if isinstance(event, Update):
            await self.async_logger.debug(f"Received update: {event}")

        try:
            return await handler(event, data)

        except Exception as e:
            await self.async_logger.error(f"Error while processing event: {e}", exc_info=True)
            raise e

    async def log(self, level: str, message: str):
        level = level.lower()

        if level == "debug":
            await self.async_logger.debug(message)
        elif level == "info":
            await self.async_logger.info(message)
        elif level == "error":
            await self.async_logger.error(message)
        else:
            await self.async_logger.warning(f"Unknown log level: {level} - {message}")
