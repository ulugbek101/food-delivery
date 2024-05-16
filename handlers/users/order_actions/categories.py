from aiogram import types

from loader import dp, db
from localization.i18n import meals_not_found
from keyboards.inline.subcategories_menu import generate_subcategories_menu
from keyboards.inline.products_menu import generate_products_menu


@dp.callback_query(lambda call: "category" in call.data)
async def show_categories(call: types.CallbackQuery):
    category_id = call.data.split(":")[-1]
    category = db.get_category(category_id)
    lang = db.get_user_language(call.from_user.id)

    if int(category['has_subcategory']) == 1:
        subcategories = db.get_subcategories(category_id)

        if len(subcategories) == 0:
            await call.answer(text=f"{meals_not_found.get(lang)}", show_alert=True)

        else:
            await call.message.answer_photo(photo=f"{subcategories[0]['photo']}",
                                            reply_markup=generate_subcategories_menu(lang=lang,
                                                                                     subcategories=subcategories,
                                                                                     category_id=category_id))
            await call.message.delete()

    else:
        products = db.get_products(category_id)

        if len(products) == 0:
            await call.answer(text=f"{meals_not_found.get(lang)}", show_alert=True)

        else:
            await call.message.delete()
            await call.message.answer_photo(photo=f"{products[0]['photo']}",
                                            reply_markup=generate_products_menu(lang=lang,
                                                                                products=products,
                                                                                category_id=category_id))
