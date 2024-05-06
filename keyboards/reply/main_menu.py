from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from localization.i18n import main_menu


def generate_main_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns main menu keyboard
    :param lang: user's language code
    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardBuilder()

    menu_buttons = main_menu.get(lang)

    for menu_button_text in menu_buttons:
        markup.button(text=menu_button_text)

    markup.adjust(2)
    return markup.as_markup(resize_keyboard=True, one_time_keyboard=True)
