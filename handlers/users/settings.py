from aiogram import types

from router import router
from loader import db
from localization.i18n import settings_title
from keyboards.reply.settings_menu import generate_settings_menu


@router.message(lambda message: message.text in ["⚙️ Sozlamalar", "⚙️ Настройки", "⚙️ Settings"])
async def settings(message: types.Message):
    lang = db.get_user(message.from_user.id).get("language_code")
    await message.answer(text=f"<b>{settings_title.get(lang)}</b>", reply_markup=generate_settings_menu(lang))
    db.update_last_step(message.from_user.id, "main_menu")
