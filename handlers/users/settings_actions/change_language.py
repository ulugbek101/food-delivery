from aiogram import types
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import (request_authorization, request_phone_number, request_fullname, back_button_text,
                               languages_menu)
from keyboards.reply.language_menu import generate_language_menu
from keyboards.reply.contact import generate_request_contact_menu
from keyboards.reply.back_button import generate_back_button
from keyboards.reply.language_menu import generate_language_menu
from states.set_phone_number import PhoneNumberState
from states.set_language import LanguageState
from handlers.users.back import back


@router.message(lambda message: message.text in ["🇺🇿 Tilni o'zgartirish", "🇷🇺 Изменить язык", "🇬🇧 Change language"])
async def change_language(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    await message.answer(text=f"<b>{languages_menu.get(lang)}</b>", reply_markup=generate_language_menu())
    await state.set_state(LanguageState.lang)
