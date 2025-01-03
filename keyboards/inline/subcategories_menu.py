from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.i18n import back_button_text


def generate_subcategories_menu(lang: str, subcategories: list, category_id: str) -> InlineKeyboardMarkup:
    """
    Generates and returns subcategories menu as an InlineKeyboardMarkup
    :param lang: user's language
    :param subcategories: subcategories list
    :param category_id: category id
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
            InlineKeyboardButton(text=subcategory[languages.get(lang)], callback_data=f"category:{subcategory['id']}")
        )
    markup.adjust(2)
    markup.row(InlineKeyboardButton(text=f"{back_button_text.get(lang)}", callback_data=f"back:to-cat:{category_id}"))

    return markup.as_markup()
