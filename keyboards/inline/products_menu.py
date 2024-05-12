from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from localization.i18n import back_button_text


def generate_products_menu(lang: str, products: list, category_id: str) -> InlineKeyboardMarkup:
    """
    Generates and returns products menu
    :param products: products list
    :param lang: user's language
    :param category_id: category id
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardBuilder()
    languages = {
        "uz": "name_uz",
        "ru": "name_ru",
        "en": "name_en",
    }

    for product in products:
        markup.button(text=product[languages.get(lang)], callback_data=f"product:{product['id']}")
    markup.adjust(2)
    markup.row(InlineKeyboardButton(text=f"{back_button_text.get(lang)}", callback_data=f"back:to-cat:{category_id}"))

    return markup.as_markup()
