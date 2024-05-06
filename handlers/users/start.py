from aiogram import types
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import greeting, languages_menu, main_menu_title
from keyboards.reply.language_menu import generate_language_menu
from keyboards.reply.main_menu import generate_main_menu
from states.select_language import SetLanguageState


@router.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)

    if not user:
        language_code = message.from_user.language_code
        fullname = message.from_user.full_name
        db.register_user(message.from_user.id, message.from_user.full_name, language_code)
    else:
        language_code = user.get("language_code")
        fullname = user.get("fullname")

    greet_message = greeting.get(language_code)
    request_language_message = languages_menu.get(language_code)

    await message.answer(f"<b>{greet_message}, {fullname} 👋</b>",
                         reply_markup=generate_language_menu())
    await state.set_state(SetLanguageState.lang)
    await message.answer(f"<b>{request_language_message}</b>")


@router.message(SetLanguageState.lang)
async def set_language(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    if message.text not in ["🇺🇿 O'zbek", "🇷🇺 Русский", "🇬🇧 English"]:
        await message.answer(f"<b>{languages_menu.get(lang)}</b>")
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
        await message.answer(f"<b>{main_menu_title.get(lang)}</b>", reply_markup=generate_main_menu(lang))
        db.update_language_code(message.from_user.id, lang)
