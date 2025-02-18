import asyncio
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher
from middlewares.logging_middleware import LoggingMiddleware

config = dotenv_values(".env")
logger = LoggingMiddleware()


async def main():
    try:
        bot = Bot(token=config["TELEGRAM_BOT_TOKEN"])
        dp = Dispatcher()
        logger.log(level="info", message="Created a bot instance.")
        await dp.start_polling(bot)

    except KeyboardInterrupt:
        logger.log(type="error", message="The bot was stopped by a keyboard action.")


if __name__ == "__main__":
    asyncio.run(main())
