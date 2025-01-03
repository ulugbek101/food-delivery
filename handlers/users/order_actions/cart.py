from aiogram import types

from loader import db
from router import router
from keyboards.inline.product_menu import generate_product_menu
from keyboards.inline.categories_menu import generate_categories_menu
from localization.i18n import cart_product_added_cart_text, cart_product_updated_text
from utils.format_price import format_price_digits


@router.callback_query(lambda call: "cart" in call.data)
async def cart_actions(call: types.CallbackQuery):
    lang = db.get_user_language(call.from_user.id)
    split_call = call.data.split(":")
    action = split_call[1]
    quantity = split_call[-1]
    product_id = split_call[-2]
    category_id = split_call[-3]

    product = db.get_product(product_id)
    user_id = db.get_user(call.from_user.id).get('id')
    cart_product = db.get_cart_product(user_id, product_id)

    if action == "show":
        await call.answer(
            text=f"💵 {product.get('price') * int(quantity)} uzs",
            show_alert=True,
        )

    elif action == "add":
        category = db.get_category(category_id)
        categories = db.get_categories(category["belongs_to"])

        if not cart_product:
            db.add_to_cart(user_id=user_id, product_id=product_id, quantity=quantity)
            await call.answer(f"{cart_product_added_cart_text.get(lang)}", show_alert=True)
        else:
            product_quantity = cart_product.get('quantity')
            new_quantity = product_quantity + int(quantity)
            db.update_cart_product_quantity(user_id=user_id, product_id=product_id, new_quantity=new_quantity)
            await call.answer(f"{cart_product_updated_text.get(lang)}", show_alert=True)

        await call.message.delete()
        await call.message.answer_photo(
            photo="https://static.vecteezy.com/system/resources/previews/017/722/096/non_2x/cooking-cuisine-cookery-logo-restaurant-menu-cafe-diner-label-logo-design-illustration-free-vector.jpg",
            reply_markup=generate_categories_menu(lang, categories)
        )

    elif action == "increment":
        quantity = int(quantity) + 1

    elif action == "decrement":
        quantity = int(quantity) - 1

    if action != "add" and action != "show" and quantity != 0:
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
        description += f"{format_price_digits(product.get('price') * int(quantity))} uzs"

        await call.message.edit_caption(
            caption=f"<b>{description}</b>",
            reply_markup=generate_product_menu(
                lang=lang,
                product_id=product_id,
                category_id=category_id,
                quantity=quantity
            )
        )
