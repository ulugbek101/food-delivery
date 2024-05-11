from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


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
        has_subcategory = category['has_subcategory'] == 1

        if has_subcategory:
            prefix = f"scategory:{category['id']}"
        else:
            prefix = f"category:{category['id']}"

        markup.button(text=category[language.get(lang)], callback_data=prefix)

    markup.adjust(2)
    return markup.as_markup()
