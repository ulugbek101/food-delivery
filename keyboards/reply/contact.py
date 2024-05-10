from aiogram.types import ReplyKeyboardMarkup

from keyboards.reply.back_button import generate_back_button
from keyboards.reply.contact_button import request_contact_button


def generate_request_contact_menu(lang: str) -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(
        keyboard=[[generate_back_button(lang), request_contact_button(lang)]],
        resize_keyboard=True)
    return markup
