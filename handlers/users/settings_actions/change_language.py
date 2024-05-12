from aiogram import types
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import languages_menu
from keyboards.reply.language_menu import generate_language_menu
from states.set_language import LanguageState


@router.message(lambda message: message.text in ["🇺🇿 Tilni o'zgartirish", "🇷🇺 Изменить язык", "🇬🇧 Change language"])
async def change_language(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    await message.answer(text=f"<b>{languages_menu.get(lang)}</b>", reply_markup=generate_language_menu())
    await state.set_state(LanguageState.lang)
