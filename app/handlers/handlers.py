from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from middlewares.logging_middleware import LoggingMiddleware
from handlers.random_recipe import get_random_recipe
from handlers.recipe_structure import Structurize


router = Router()
logger = LoggingMiddleware()


@router.message(Command("start"))
async def handle_start(message: Message):
    """Greets the user and logs data.
    Args:
        message (Message): The '/start' command message object sent by the user.
    """

    await message.answer(
        text=f"Hi {message.from_user.first_name}, I am your Cooking Assistant!\nLet's start our delicious journey!"
    )

    logger.log(
        level="info", message=f"Start command handled for user {message.from_user.id}."
    )


@router.message(Command("random"))
async def handle_random(message: Message):
    """Sends the fetched random recipe with a photo and description.
    Args:
        message (Message): The '/random' command message object sent by the user.
    """

    random_recipe = await get_random_recipe()

    if random_recipe:
        await message.answer(text="Alright, here is a random meal by my choice.")
        await message.answer_photo(photo=random_recipe.get("strMealThumb", "default_image_url"))
        await message.answer(text=Structurize.structurized_recipe(random_recipe), parse_mode="Markdown")

        logger.log(
            level="info", message=f"Got a random recipe for user {message.from_user.id}.")
    else:
        await message.answer(text="I couldn't find a random recipe. Please try again later.")
