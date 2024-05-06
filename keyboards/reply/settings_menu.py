from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from localization.i18n import settings
from keyboards.reply.back_button import generate_back_button


def generate_settings_menu(lang: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()

    settings_buttons = settings.get(lang)

    for text in settings_buttons:
        markup.button(text=text)

    markup.adjust(2)
    markup.row(generate_back_button(lang))
    return markup.as_markup(resize_keyboard=True, one_time_keyboard=True)
