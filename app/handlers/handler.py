from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from middlewares.logging_middleware import LoggingMiddleware


router = Router()
logger = LoggingMiddleware()


@router.message(Command("start"))
async def handle_start(message: Message):
    await message.answer(text="Hi, I am your Cooking Assistant!")
    logger.log(
        level="info", message=f"Start command handled for user {message.from_user.id}."
    )
