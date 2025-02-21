from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from middlewares.logging_middleware import AsyncLoggingMiddleware
from handlers.random_recipe import get_random_recipe
from handlers.recipe_structure import Structurize
from keyboards.keyboards import Keyboards


router = Router()
logger = AsyncLoggingMiddleware()


class RecipeStates(StatesGroup):
    WAITING_FOR_RECIPE = State()


@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    """Greets the user and resets the state."""

    await state.clear()

    await message.answer(
        text=f"Hi {message.from_user.first_name}, I am your Cooking Assistant!\nLet's start our delicious journey!",
        reply_markup=Keyboards.main_menu_kb()
    )
    await logger.log(
        level="info", message=f"Start command handled for user {message.from_user.id}.")


@router.message(F.text == "Get a random recipe.")
async def handle_random(message: Message, state: FSMContext):
    """Sends a random recipe and prevents spamming."""

    await state.set_state(RecipeStates.WAITING_FOR_RECIPE)

    await message.answer(
        text="Alright, here is a random meal by my choice.",
        reply_markup=ReplyKeyboardRemove()
    )

    random_recipe = await get_random_recipe()

    if random_recipe:
        await message.answer_photo(photo=random_recipe.get("strMealThumb", "default_image_url"))
        await message.answer(
            text=Structurize.structurized_recipe(random_recipe),
            parse_mode="Markdown"
        )
        await message.answer(
            text="Here it is, enjoy it!",
            reply_markup=Keyboards.main_menu_kb()
        )
        await logger.log(
            level="info", message=f"Got a random recipe for user {message.from_user.id}.")

    else:
        await message.answer(text="I couldn't find a random recipe. Please try again later.")

    await state.clear()


@router.message(StateFilter(RecipeStates.WAITING_FOR_RECIPE))
async def handle_unexpected_message(message: Message):
    """Prevents users from sending irrelevant messages during the process."""

    await message.answer("Please wait while I'm preparing your recipe. This won't take long.")


@router.message()
async def handle_unrecognized_message(message: Message):
    """Handles unrecognized commands or text."""

    await message.answer("I'm not sure what you mean. Use the menu below to continue.")
