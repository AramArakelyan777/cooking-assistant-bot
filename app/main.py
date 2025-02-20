import asyncio
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher
from middlewares.logging_middleware import LoggingMiddleware
from handlers.handlers import router


config = dotenv_values(".env")
logger = LoggingMiddleware()


async def main():
    try:
        bot = Bot(token=config["TELEGRAM_BOT_TOKEN"])
        dp = Dispatcher()

        dp.update.middleware(logger)
        dp.include_router(router)

        logger.log(level="info", message="Started the bot.")

        await dp.start_polling(bot)

    except KeyboardInterrupt:
        logger.log(level="error",
                   message="The bot was stopped by a keyboard action.")


if __name__ == "__main__":
    asyncio.run(main())
