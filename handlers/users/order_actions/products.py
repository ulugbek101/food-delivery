from aiogram import types

from router import router
from loader import db
from utils.format_price import format_price_digits
from keyboards.inline.product_menu import generate_product_menu


@router.callback_query(lambda call: "product" in call.data)
async def show_product_details(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)
    product_id = call.data.split(":")[-1]
    product = db.get_product(product_id)

    product_name = {
        "uz": "name_uz",
        "ru": "name_ru",
        "en": "name_en",
    }
    product_desc = {
        "uz": "desc_uz",
        "ru": "desc_ru",
        "en": "desc_en",
    }

    description = f"{product[product_name.get(lang)]}\n\n"
    description += f"{product[product_desc.get(lang)]}\n\n"
    description += f"{format_price_digits(product['price'])} uzs"

    await call.message.delete()
    await call.message.answer_photo(
        photo=product['photo'],
        caption=f"<b>{description}</b>",
        reply_markup=generate_product_menu(lang, product_id, product['category_id'])
    )
