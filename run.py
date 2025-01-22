import asyncio
import logging
from os import environ
from aiogram import Bot, Dispatcher
from app.handlers import router

bot = Bot(token=environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher()


async def main():
    dp.include_router(router)
    logging.basicConfig(filename="logs/bot.log", level=logging.INFO)
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("The bot is stopped by a keyboard action.")


asyncio.run(main())
