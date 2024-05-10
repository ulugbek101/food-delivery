from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from localization.i18n import contact_button


def request_contact_button(lang: str) -> KeyboardButton:
    """
    Generates and returns request contact button to get user's phone number
    :param lang: user's language
    :return: KeyboardButton
    """

    return KeyboardButton(text=f"{contact_button.get(lang)}", request_contact=True)
