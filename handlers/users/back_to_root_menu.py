from aiogram import types
from aiogram import F
from aiogram.fsm.context import FSMContext

from localization.i18n import main_menu_title, settings_title, back_button_text
from router import router
from loader import db
from keyboards.reply.main_menu import generate_main_menu
from keyboards.reply.settings_menu import generate_settings_menu
from keyboards.inline.subcategories_menu import generate_subcategories_menu
from keyboards.inline.categories_menu import generate_categories_menu

from keyboards.inline.root_menu import generate_root_menu


@router.callback_query(lambda call: call.data == "root_menu")
async def back_to_root_menu_button(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)

    await call.message.edit_caption(
        caption="",
        reply_markup=generate_root_menu(lang)
    )
