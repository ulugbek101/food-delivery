from aiogram import types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import greeting, request_language, languages_menu
from keyboards.reply.language_menu import generate_language_menu
from keyboards.reply.main_menu import generate_main_menu
from states.select_language import SetLanguageState


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)

    if not user:
        language_code = message.from_user.language_code
        db.register_user(message.from_user.id, message.from_user.full_name, language_code)
    else:
        language_code = user.get("language_code")

    greet_message = greeting.get(language_code)
    request_language_message = request_language.get(language_code)

    await message.answer(f"<b>{greet_message}, {message.from_user.full_name} 👋</b>",
                         reply_markup=generate_language_menu())
    await state.set_state(SetLanguageState.lang)
    await message.answer(f"<b>{request_language_message}</b>")


@router.message(SetLanguageState.lang)
async def set_language(message: types.Message, state: FSMContext):
    if message.text not in ["🇺🇿 O'zbek", "🇷🇺 Русский", "🇺🇸 English"]:
        await message.answer(f"{request_language.get(message.from_user.language_code)}")
    else:
        lang = message.from_user.language_code
        if message.text == "🇺🇿 O'zbek":
            lang = "uz"
        if message.text == "🇷🇺 Русский":
            lang = "ru"
        if message.text == "🇺🇸 English":
            lang = "en"

        await state.update_data(lang=lang)
        await state.clear()
        db.update_language_code(message.from_user.id, lang)
        await message.answer(f"<b>{languages_menu.get(lang)}</b>", reply_markup=generate_main_menu(lang))
