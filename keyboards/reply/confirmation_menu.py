from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from keyboards.reply.back_button import generate_back_button
from localization.i18n import confirm, decline


def generate_confirmation_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns confirmation menu for order
    :param lang: user's language
    :return: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardBuilder()
    markup.row(generate_back_button(lang))
    markup.button(text=f"{confirm.get(lang)}")
    markup.button(text=f"{decline.get(lang)}")
    markup.adjust(2)
    return markup.as_markup(resize_keyboard=True)
