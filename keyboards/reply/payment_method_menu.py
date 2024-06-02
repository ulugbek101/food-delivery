from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup

from keyboards.reply.back_button import generate_back_button
from localization.i18n import payment_method_menu


def generate_payment_method_menu(lang: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardBuilder()

    for button in payment_method_menu.get(lang):
        markup.button(text=button)
    markup.adjust(2)
    markup.row(
        generate_back_button(lang)
    )

    return markup.as_markup(resize_keyboard=True)
