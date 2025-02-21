import asyncio
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher
from middlewares.logging_middleware import AsyncLoggingMiddleware
from handlers.handlers import router
from handlers.http.session_manager import init_session, close_session


config = dotenv_values(".env")
logger = AsyncLoggingMiddleware()


async def main():
    """Entry point for the whole app, where the bot and the dispatcher are created and configured."""

    try:
        await init_session()

        bot_token = config["TELEGRAM_BOT_TOKEN"]

        if bot_token:
            bot = Bot(token=bot_token)
        else:
            await logger.log(level="error", message="Unable to create the bot. The token is invalid.")

        dp = Dispatcher()

        dp.update.middleware(logger)
        dp.include_router(router)

        await logger.log(level="info", message="Started the bot.")
        await dp.start_polling(bot)

    except KeyboardInterrupt:
        await logger.log(level="error",
                         message="The bot was stopped by a keyboard action.")

    finally:
        await close_session()


if __name__ == "__main__":
    asyncio.run(main())
