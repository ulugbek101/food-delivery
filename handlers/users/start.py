from aiogram import types
from aiogram.filters.command import CommandStart

from router import router
from loader import db
from localization.greeting import greeting


@router.message(CommandStart())
async def start(message: types.Message):
    user = db.get_user(message.from_user.id)

    if not user:
        language_code = message.from_user.language_code
        greet_message = greeting.get(language_code) or greeting['en']
        db.register_user(message.from_user.id, message.from_user.full_name, language_code)
    else:
        greet_message = greeting.get(user['language_code'])

    await message.answer(f"{greet_message}, {message.from_user.full_name} 👋")
