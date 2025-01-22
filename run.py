import asyncio
import logging
from os import environ
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

bot = Bot(token=environ["TELEGRAM_BOT_TOKEN"])
dp = Dispatcher()


@dp.message(Command("start"))
async def handle_start(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text="Welkommen!")
    logging.basicConfig(filename="logs/handlerlogs.log", level=logging.INFO)


@dp.message(Command("home"))
async def send_location(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text=f"Home.\nLongitude: {message.location.longitude}\nLatitude: {message.location.latitude}")


async def main():
    logging.basicConfig(filename="logs/bot.log", level=logging.INFO)
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        print("The bot is stopped by a keyboard action.")


asyncio.run(main())
