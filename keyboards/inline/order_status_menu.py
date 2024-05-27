from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from localization.i18n import check_status


def generate_order_status_menu(lang: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardBuilder()
    markup.row(
        InlineKeyboardButton(
            text=f"{check_status.get(lang)}",
            callback_data=f"check-status")
    )
    return markup.as_markup()
