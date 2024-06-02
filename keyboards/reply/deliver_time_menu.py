from datetime import datetime

from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton

from localization.i18n import back_button_text


def generate_deliver_time_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns deliver time menu with available times
    :param lang: user's language
    :return: ReplyKeyboardMarkup
    """

    now = datetime.now().time().hour

    markup = ReplyKeyboardBuilder()
    times = [now + 3, now + 4, now + 5, now + 6]

    for time in times:
        time = f"0{time}" if time < 10 else f"{time}"
        markup.button(text=f"{time}:00")
    markup.adjust(2)
    markup.row(
        KeyboardButton(text=f"{back_button_text.get(lang)}")
    )

    return markup.as_markup(resize_keyboard=True)
