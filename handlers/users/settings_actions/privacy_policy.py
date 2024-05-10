from aiogram import types

from router import router


@router.message(lambda message: message.text in ["📄 Ommaviy taklif", "📄 Публичная оферта", "📄 Privacy policy"])
async def privacy_policy(message: types.Message):
    await message.answer_document(document="https://thedevu101.uz/users/download-cv/")
