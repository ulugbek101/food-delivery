from aiogram import types
from loader import dp, db
from localization.i18n import meals_not_found
from keyboards.inline.subcategories_menu import generate_subcategories_menu


@dp.callback_query(lambda call: "scategory" in call.data)
async def show_subcategories(call: types.CallbackQuery):
    category_id = call.data.split(":")[-1]
    subcategories = db.get_subcategories(category_id)
    lang = db.get_user_language(call.message.from_user.id)

    if len(subcategories) == 0:
        await call.answer(text=f"{meals_not_found.get(lang)}")

    else:
        await call.message.answer_photo(photo=f"{subcategories[0]['photo']}",
                                        reply_markup=generate_subcategories_menu(lang=lang, subcategories=subcategories))
        await call.message.delete()
