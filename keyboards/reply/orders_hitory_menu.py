from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton

from localization.i18n import back_button_text


def generate_user_orders_menu(lang: str, orders: list) -> ReplyKeyboardMarkup:
    """
    Generates and returns all user's orders history including finished and unfinished orders
    :param lang: user's language
    :param orders:
    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardBuilder()

    for order in orders[::-1]:
        markup.button(text=f'№{order.get("id")} - {order.get("created_date")}')
    markup.adjust(2)
    markup.row(
        KeyboardButton(text=f"{back_button_text.get(lang)}")
    )

    return markup.as_markup(resize_keyboard=True)
