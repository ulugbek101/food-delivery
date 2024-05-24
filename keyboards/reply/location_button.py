from aiogram.types import KeyboardButton

from localization.i18n import location_button


def request_location_button(lang: str) -> KeyboardButton:
    markup = KeyboardButton(text=f"{location_button.get(lang)}", request_location=True)
    return markup
