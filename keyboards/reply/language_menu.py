from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def generate_language_menu() -> ReplyKeyboardMarkup:
    """
    Generates returns languages menu as a reply keyboard to set language
    :return: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardBuilder()

    languages_list = [
        "🇺🇿 O'zbek",
        "🇷🇺 Русский",
        "🇺🇸 English",
    ]

    for language in languages_list:
        markup.button(text=language)

    markup.adjust(3)
    return markup.as_markup(resize_keyboard=True, one_time_keyboard=True)
