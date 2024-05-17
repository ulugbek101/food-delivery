from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.i18n import back_button_text, add_to_cart


def generate_product_menu(lang: str, product_id: int | str, category_id: int | str,
                          quantity: int = 1) -> types.InlineKeyboardMarkup:
    """
    Generates and returns product menu
    :param lang: user's language
    :param product_id: product id
    :param category_id: product's category id
    :param quantity: product quantity
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardBuilder()

    markup.row(
        types.InlineKeyboardButton(
            text="-",
            callback_data=f"cart:decrement:{category_id}:{product_id}:{quantity}"
        ),
        types.InlineKeyboardButton(
            text=f"{quantity}",
            callback_data=f"cart:show:{category_id}:{product_id}:{quantity}"
        ),
        types.InlineKeyboardButton(
            text="+",
            callback_data=f"cart:increment:{category_id}:{product_id}:{quantity}"
        ),
    )
    markup.row(
        types.InlineKeyboardButton(text=f"{add_to_cart.get(lang)}", callback_data=f"cart:add:{category_id}:{product_id}:{quantity}")
    )
    markup.row(
        types.InlineKeyboardButton(text=f"{back_button_text.get(lang)}", callback_data=f"back:to-cat:{category_id}")
    )

    return markup.as_markup()
