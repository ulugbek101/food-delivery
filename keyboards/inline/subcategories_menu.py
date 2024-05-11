from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate_subcategories_menu(lang: str, subcategories: list) -> InlineKeyboardMarkup:
    """
    Generates and returns subcategories menu as an InlineKeyboardMarkup
    :param lang: user's language
    :param subcategories: subcategories list
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardBuilder()
    languages = {
        "uz": "name_uz",
        "ru": "name_ru",
        "en": "name_en",
    }

    for subcategory in subcategories:
        markup.row(
            InlineKeyboardButton(text=subcategory[languages.get(lang)], callback_data=f"subcategory:{subcategory['id']}")
        )
    markup.adjust(2)

    return markup.as_markup()
