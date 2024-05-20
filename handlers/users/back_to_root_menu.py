from aiogram import types

from router import router
from loader import db
from keyboards.inline.root_menu import generate_root_menu


@router.callback_query(lambda call: call.data == "root_menu")
async def back_to_root_menu_button(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)

    await call.message.edit_caption(
        caption="",
        reply_markup=generate_root_menu(lang)
    )
