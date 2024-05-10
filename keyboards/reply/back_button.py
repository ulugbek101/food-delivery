from aiogram.types import KeyboardButton

from localization.i18n import back_button_text


def generate_back_button(lang: str) -> KeyboardButton:
    """
    Generates and returns back button
    :param lang:
    :return: KeyboardButton
    """

    return KeyboardButton(text=f"{back_button_text[lang]}")
