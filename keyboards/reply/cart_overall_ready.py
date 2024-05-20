from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from localization.i18n import back_button_text, cart_overall_ready


def generate_cart_overall_ready_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns cart overall ready state keyboard
    :param lang: user's language
    :return: ReplyKeyboardKeyboard
    """

    markup = ReplyKeyboardBuilder()

    markup.button(text=f"{back_button_text.get(lang)}")
    markup.button(text=f"{cart_overall_ready.get(lang)}")

    return markup.as_markup(resize_keyboard=True)
