from dotenv import dotenv_values
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from middlewares.logging_middleware import AsyncLoggingMiddleware
from handlers.random_recipe import get_random_recipe
from handlers.name_search import get_recipe_by_name
from handlers.recipe_structure import Structurize
from keyboards.keyboards import Keyboards
from handlers.recipe_states import RecipeStates


router = Router()
logger = AsyncLoggingMiddleware()
main_menu = Keyboards.main_menu_kb()
recipes_by_name = None
config = dotenv_values()

# commands


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


@router.message(F.text == "Surprise me!")
async def handle_random(message: Message, state: FSMContext):
    """Sends a random recipe and prevents spamming."""

    await state.set_state(RecipeStates.WAITING_FOR_RECIPE)

    await message.answer(
        text="Alright, here is a random meal by my choice.",
        reply_markup=ReplyKeyboardRemove()
    )

    random_recipe = await get_random_recipe()

    if random_recipe:
        await message.answer_photo(photo=random_recipe.get("strMealThumb", config.get("DEFAULT_IMAGE_URL")))
        await message.answer(
            text=Structurize.structurized_recipe(random_recipe),
            parse_mode="Markdown"
        )
        await message.answer(
            text="Here it is, enjoy it!",
            reply_markup=main_menu
        )
        await logger.log(
            level="info", message=f"Got a random recipe for user {message.from_user.id}.")

    else:
        await message.answer(text="I couldn't find a random recipe.", reply_markup=main_menu)

    await state.clear()


@router.message(F.text == "Search by name")
async def handle_name_search_first(message: Message, state: FSMContext):
    """Sends the recipes searched by name and prevents spamming."""

    await state.set_state(RecipeStates.SEARCH_BY_NAME)

    await message.answer(
        text="Alright, please enter the name of a meal that you want.",
        reply_markup=ReplyKeyboardRemove()
    )


# state filtering


@router.message(StateFilter(RecipeStates.SEARCH_BY_NAME))
async def handle_name_search_second(message: Message, state: FSMContext):
    if len(message.text) < 3:
        await message.answer(text="The meal name you entered is too short.", reply_markup=main_menu)
        return

    await state.update_data(recipe_name=message.text)

    data = await state.get_data()

    global recipes_by_name
    recipes_by_name = await get_recipe_by_name(data["recipe_name"])

    if recipes_by_name:
        await message.answer(text="Here are the meals that I have found based on your input.",
                             reply_markup=await Keyboards.name_search_kb(recipes=recipes_by_name))

        await message.answer(
            text="Click on the meal you want to view its recipe!",
            reply_markup=main_menu
        )
        await logger.log(
            level="info", message=f"Got meal names searched by name for user {message.from_user.id}.")

    else:
        await message.answer(text="I couldn't find any recipes.", reply_markup=main_menu)

    await state.clear()


@router.message(StateFilter(RecipeStates.WAITING_FOR_RECIPE, RecipeStates.SEARCH_BY_NAME))
async def handle_unexpected_message(message: Message):
    """Prevents users from sending irrelevant messages during the process."""

    await message.answer("Please wait while I'm preparing your recipe.")


# callbacks


@router.callback_query()
async def handle_recipe_callback_query(callback: CallbackQuery):
    """Handles a button click with the meal name to view its recipe."""

    await callback.answer(text="")

    if recipes_by_name:
        meal_id = callback.data
        meal = next((m for m in recipes_by_name if str(
            m["idMeal"]) == meal_id), None)

        if meal:
            await callback.message.answer_photo(photo=meal.get("strMealThumb", config.get("DEFAULT_IMAGE_URL")))
            await callback.message.answer(text=Structurize.structurized_recipe(meal), parse_mode="Markdown")

            await logger.log(
                level="info", message=f"Sent a meal's recipe to user {callback.message.from_user.id}")
        else:
            await callback.message.answer(text="Meal not found.")
            await logger.log(level="error", message="Meal not found for callback.")

    else:
        await callback.message.answer(text="No meals found to show its recipe.")


# unrecognized messages


@router.message()
async def handle_unrecognized_message(message: Message):
    """Handles unrecognized commands or text."""

    await message.answer("I'm not sure what you mean.\nUse the menu or send the /help command.", reply_markup=main_menu)
