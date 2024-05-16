from aiogram import types
from aiogram import F

from router import router
from loader import db
from localization.i18n import categories
from keyboards.inline.root_menu import generate_root_menu
from keyboards.inline.root_menu import root_menu_callback
from keyboards.inline.categories_menu import generate_categories_menu


@router.message(F.text == "/order")
@router.message(F.text.in_({"🛍️ Buyurtma berish", "🛍 Заказать", "🛍️ Order"}))
async def order_menu(message: types.Message):
    lang = db.get_user_language(message.from_user.id)
    await message.answer_photo(
        photo="https://static.vecteezy.com/system/resources/previews/017/722/096/non_2x/cooking-cuisine-cookery-logo-restaurant-menu-cafe-diner-label-logo-design-illustration-free-vector.jpg",
        reply_markup=generate_root_menu(lang),
    )


@router.callback_query(lambda call: call.data in root_menu_callback)
async def handle_root_menu_action(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)

    if call.data == "foods":
        categories_list = db.get_categories(target="foods")
        await call.message.edit_caption(
            caption=f"{categories.get(lang)}",
            reply_markup=generate_categories_menu(lang, categories_list))

    elif call.data == "others":
        categories_list = db.get_categories(target="others")
        await call.message.edit_caption(
            caption=f"{categories.get(lang)}", reply_markup=generate_categories_menu(lang, categories_list)
        )
