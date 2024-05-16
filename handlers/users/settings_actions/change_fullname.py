from aiogram import types
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import (request_authorization, request_phone_number, request_fullname, back_button_text,
                               fullname_successfull_update)
from keyboards.reply.settings_menu import generate_settings_menu
from keyboards.reply.contacts import generate_request_contact_menu
from keyboards.reply.back_button import generate_back_button
from states.set_phone_number import PhoneNumberState
from states.set_fullname import FullnameState
from handlers.users.back import back


@router.message(lambda message: message.text in ["🅰️ Ismni o'zgartirish", "🅰️ Изменить имя", "🅰️ Change name"])
async def change_fullname(message: types.Message, state: FSMContext):
    lang = db.get_user(message.from_user.id).get("language_code")
    user = db.get_user(message.from_user.id)

    if not user.get("phone_number"):
        await message.answer(text=f"<b>{request_authorization.get(lang)}</b>")
        await message.answer(text=f"<b>{request_phone_number.get(lang)}</b>",
                             reply_markup=generate_request_contact_menu(lang))
        db.update_last_step(message.from_user.id, "settings_menu")
        await state.set_state(PhoneNumberState.phone_number)

    else:
        await message.answer(text=f"<b>{request_fullname.get(lang)}</b>",
                             reply_markup=types.ReplyKeyboardMarkup(
                                 keyboard=[[generate_back_button(lang)]],
                                 resize_keyboard=True))
        db.update_last_step(message.from_user.id, "settings_menu")
        await state.set_state(FullnameState.fullname)


@router.message(FullnameState.fullname)
async def update_fullname(message: types.Message, state: FSMContext):
    if message.text.strip() in back_button_text.values():
        await back()

    else:
        lang = db.get_user_language(message.from_user.id)

        await state.clear()
        await message.answer(text=f"<b>{fullname_successfull_update.get(lang)}</b>",
                             reply_markup=generate_settings_menu(lang))
        db.update_fullname(message.from_user.id, message.text)
        db.update_last_step(message.from_user.id, "settings_menu")
