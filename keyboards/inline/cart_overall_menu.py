from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loader import db


def generate_cart_overall_menu(cart_products: list, user_id: int, lang: str) -> InlineKeyboardMarkup:
    """
    Generates and returns cart overall menu to remove, increment or decrement cart products
    :param cart_products:
    :param user_id:
    :param lang:
    :return:
    """

    markup = InlineKeyboardBuilder()

    cart_product_name = {
        "uz": "name_uz",
        "ru": "name_ru",
        "en": "name_en",
    }

    for cart_product in cart_products:
        product = db.get_product(cart_product.get('product_id'))

        markup.row(InlineKeyboardButton(text=f"❌ {product.get(cart_product_name.get(lang))}", callback_data="..."))
        markup.row(
            InlineKeyboardButton(text="-", callback_data="..."),
            InlineKeyboardButton(text=f"{cart_product.get('quantity')}",
                                 callback_data="..."),
            InlineKeyboardButton(text="+", callback_data="...")
        )

    return markup.as_markup()
