from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from localization.i18n import shipping_option_buttons
from keyboards.reply.back_button import generate_back_button


def generate_select_deliver_type_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns shipping options menu
    :param lang: user's language
    :return: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardBuilder()

    for shipping_option in shipping_option_buttons.get(lang):
        markup.button(text=shipping_option)
    markup.adjust(2)
    markup.row(generate_back_button(lang))

    return markup.as_markup(resize_keyboard=True)
