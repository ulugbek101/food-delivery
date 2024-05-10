from aiogram import types
from aiogram import F

from localization.i18n import main_menu_title, settings_title, back_button_text
from router import router
from loader import db
from keyboards.reply.main_menu import generate_main_menu
from keyboards.reply.settings_menu import generate_settings_menu


@router.message(F.text.in_(back_button_text.values()))
async def back(message: types.Message):

    user = db.get_user(message.from_user.id)
    lang = user.get("language_code")
    last_visited_place = user.get("last_visited_place")

    if last_visited_place == "main_menu":
        await message.answer(f"<b>{main_menu_title.get(lang)}</b>", reply_markup=generate_main_menu(lang))

    elif last_visited_place == "settings_menu":
        await message.answer(f"<b>{settings_title.get(lang)}</b>", reply_markup=generate_settings_menu(lang))
        db.update_last_step(message.from_user.id, "main_menu")
