from aiogram.fsm.state import StatesGroup, State


class RecipeStates(StatesGroup):
    WAITING_FOR_RECIPE = State()
    SEARCH_BY_NAME = State()