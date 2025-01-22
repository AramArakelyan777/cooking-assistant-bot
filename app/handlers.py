import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(text="Welcome!")
    logging.basicConfig(filename="logs/handlerlogs.log", level=logging.INFO)


@router.message(Command("help"))
async def handle_help(message: Message):
    await message.reply(text="This is the help command handler.")
    logging.basicConfig(filename="logs/handlerlogs.log", level=logging.INFO)
