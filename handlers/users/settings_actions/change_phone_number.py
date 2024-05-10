from aiogram import types
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import phone_number_invalid, phone_number_valid, back_button_text, request_phone_number
from keyboards.reply.settings_menu import generate_settings_menu
from keyboards.reply.contact import generate_request_contact_menu
from states.set_phone_number import PhoneNumberState
from validations.phone_number import validate_phone_number
from handlers.users.back import back


@router.message(lambda message: message.text in ["📱 Raqamni o'zgartirish", "📱 Изменить номер", "📱 Change number"])
async def change_phone_number(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    await message.answer(text=f"<b>{request_phone_number.get(lang)}</b>",
                         reply_markup=generate_request_contact_menu(lang))
    await state.set_state(PhoneNumberState.phone_number)
    db.update_last_step(message.from_user.id, "settings_menu")


@router.message(PhoneNumberState.phone_number)
async def update_phone_number(message: types.Message, state: FSMContext):
    if message.text and message.text.strip() in back_button_text.values():
        await state.clear()
        await back()

    lang = db.get_user_language(message.from_user.id)

    if not message.contact:
        if validate_phone_number(phone_number=message.text):
            await message.answer(text=f"<b>{phone_number_valid.get(lang)}</b>",
                                 reply_markup=generate_settings_menu(lang))
            await state.clear()
            db.update_last_step(message.from_user, "main_menu")
            db.update_phone_number(message.from_user.id, f"{message.text.strip()}")
        else:
            await message.answer(text=f"<b>{phone_number_invalid.get(lang)}</b>")

    else:
        await message.answer(text=f"<b>{phone_number_valid.get(lang)}</b>",
                             reply_markup=generate_settings_menu(lang))
        await state.update_data(phone_number=message.contact.phone_number)
        await state.clear()
        db.update_phone_number(message.from_user.id, f"+{message.contact.phone_number}")
        db.update_last_step(message.from_user, "main_menu")
