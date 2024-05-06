from aiogram import types
from aiogram import F

from localization.i18n import main_menu_title
from router import router
from loader import db
from keyboards.reply.main_menu import generate_main_menu


@router.message(F.text == "👈 Orqaga")
@router.message(F.text == "👈 Назад")
@router.message(F.text == "👈 Back")
async def back(message: types.Message):
    user = db.get_user(message.from_user.id)
    lang = user.get("language_code")
    last_visited_place = user.get("last_visited_place")

    if last_visited_place == "main_menu":
        await message.answer(f"<b>{main_menu_title.get(lang)}</b>", reply_markup=generate_main_menu(lang))
