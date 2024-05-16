from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.i18n import back_button_text


def generate_categories_menu(lang: str, categories_list: tuple | list) -> InlineKeyboardMarkup:
    """
    Generates and returns categories menu as an InlineKeyboardMarkup
    :param lang: user's language
    :param categories_list: categories list from a database
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardBuilder()
    language = {
        "uz": "name_uz",
        "ru": "name_ru",
        "en": "name_en",
    }

    for category in categories_list:
        markup.button(text=category[language.get(lang)], callback_data=f"category:{category['id']}")
    markup.adjust(2)
    markup.row(
        InlineKeyboardButton(text=f"{back_button_text.get(lang)}", callback_data="root_menu")
    )

    return markup.as_markup()
