from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Keyboards:
    @staticmethod
    def main_menu_kb() -> ReplyKeyboardMarkup:
        """Creates and returns the main menu keyboard.
        Returns:
            ReplyKeyboardMarkup: The reply keyboard to be returned.
        """

        return ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text="Surprise me!"),
             KeyboardButton(text="Search by name")]
        ],
            resize_keyboard=True
        )

    @staticmethod
    async def name_search_kb(recipes):
        if len(recipes) == 0 or not recipes:
            return None

        keyboard = InlineKeyboardBuilder()

        for meal in recipes:
            keyboard.add(InlineKeyboardButton(text=meal.get(
                "strMeal", "N/A"), callback_data=str(meal["idMeal"])))

        return keyboard.adjust(1).as_markup()
