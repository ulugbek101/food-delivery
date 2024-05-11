from aiogram import types

from router import router
from loader import db
from localization.i18n import categories
from keyboards.inline.categories_menu import generate_categories_menu


@router.message(lambda message: message.text in ["🛍️ Buyurtma berish", "🛍 Заказать", "🛍️ Order"])
async def order_menu(message: types.Message):
    lang = db.get_user_language(message.from_user.id)
    categories_list = db.get_categories()
    await message.answer_photo(
        photo="https://static.vecteezy.com/system/resources/previews/017/722/096/non_2x/cooking-cuisine-cookery-logo-restaurant-menu-cafe-diner-label-logo-design-illustration-free-vector.jpg",
        caption=f"{categories.get(lang)}", reply_markup=generate_categories_menu(lang, categories_list))
