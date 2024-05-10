from aiogram import types
from aiogram.types import InputFile
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from localization.i18n import contact_information


@router.message(lambda message: message.text in ["☎️ Biz bilan bog'laning", "☎️ Свяжитесь с нами", "☎️ Contact us"])
async def contact_us(message: types.Message):
    lang = db.get_user_language(message.from_user.id)
    await message.answer(text=f"{contact_information.get(lang)}", parse_mode="HTML")
