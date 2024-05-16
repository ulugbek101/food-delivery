from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.i18n import root_menu

root_menu_callback = ["foods", "others"]


def generate_root_menu(lang: str) -> InlineKeyboardMarkup:
    """
    Returns 2 buttons: 'Foods' and 'Others' buttons
    :param lang: user's language
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardBuilder()
    for index, button in enumerate(iterable=root_menu.get(lang), start=0):
        markup.button(text=button, callback_data=f"{root_menu_callback[index]}")

    return markup.as_markup()
