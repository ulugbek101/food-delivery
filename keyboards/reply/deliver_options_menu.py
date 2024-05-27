from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup, KeyboardButton

from localization.i18n import deliver_options, back_button_text


def generate_deliver_options_menu(lang: str) -> ReplyKeyboardMarkup:
    """
    Generates and returns available delivery options menu
    :param lang: user's language
    :return: ReplyKeyboardMarkup
    """

    markup = ReplyKeyboardBuilder()

    for deliver_option in deliver_options.get(lang):
        markup.button(text=f"{deliver_option}")
    markup.adjust(2)
    markup.row(
        KeyboardButton(text=f"{back_button_text.get(lang)}")
    )

    return markup.as_markup(resize_keyboard=True)
