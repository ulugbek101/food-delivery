from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.reply.back_button import generate_back_button
from keyboards.reply.location_button import request_location_button
from localization.i18n import back_button_text


def generate_send_location_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns request locations menu
    :param lang: user's language
    :return: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardMarkup(
        keyboard=[[generate_back_button(lang), request_location_button(lang)]],
        resize_keyboard=True)
    return markup


def generate_locations_menu(lang: str, locations_list: list) -> ReplyKeyboardMarkup:
    """
    Generates and returns all user's locations list
    :param lang: user's language
    :param locations_list: user's locations list
    :return: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardBuilder()

    markup.row(KeyboardButton(text=f"{back_button_text.get(lang)}"))
    markup.add(request_location_button(lang))
    for location in locations_list:
        markup.button(text=location.get("full_address"))
    markup.adjust(1)

    return markup.as_markup(resize_keyboard=True)
