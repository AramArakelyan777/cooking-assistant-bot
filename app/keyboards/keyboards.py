from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class Keyboards:
    @staticmethod
    def main_menu_kb():
        """Creates and returns the main menu keyboard.
        Returns:
            ReplyKeyboardMarkup: The reply keyboard to be returned.
        """

        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Get a random recipe.")]], resize_keyboard=True)
