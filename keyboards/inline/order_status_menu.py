from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.i18n import check_status


def generate_order_status_menu(lang: str, order_id: int) -> InlineKeyboardMarkup:
    """
    Generates and returns order status button
    :param lang: user's language
    :param order_id: order's id
    :return: InlineKeyboardMarkup
    """

    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(
            text=f"{check_status.get(lang)}",
            callback_data=f"check-order-status:{order_id}")
    )
    return markup.as_markup()
