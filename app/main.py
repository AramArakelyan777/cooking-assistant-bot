import asyncio
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher

config = dotenv_values(".env")


async def main():
    try:
        bot = Bot(token=config["TELEGRAM_BOT_TOKEN"])
        dp = Dispatcher()
        await dp.start_polling(bot)

    except KeyboardInterrupt:
        print("The bot was stopped by a keyboard action.")


if __name__ == "__main__":
    asyncio.run(main())
