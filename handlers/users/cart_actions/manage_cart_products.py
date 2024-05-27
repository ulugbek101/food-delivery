from aiogram import types

from keyboards.inline.cart_overall_menu import generate_cart_overall_menu
from keyboards.reply.cart_overall_ready import generate_cart_overall_ready_menu
from keyboards.reply.main_menu import generate_main_menu
from loader import db
from localization.i18n import total, cart_empty
from router import router
from utils.format_price import format_price_digits


@router.callback_query(lambda call: "order" in call.data)
async def manage_cart(call: types.CallbackQuery):
    splitted_call = call.data.split(":")
    action = splitted_call[1]
    product_id = splitted_call[2]
    quantity = int(splitted_call[3])
    user_id = splitted_call[4]

    lang = db.get_user_language(call.from_user.id)
    user = db.get_user(call.from_user.id)

    if action == "increment":
        db.update_cart_product_quantity(user_id, product_id, quantity + 1)

    if action == "decrement":
        if quantity - 1 != 0:
            db.update_cart_product_quantity(user_id, product_id, quantity - 1)

    if action == "delete":
        db.delete_from_cart(user_id, product_id)

    cart_products = db.get_users_cart_products(user.get('id'))
    cart_products_total_price = db.get_users_cart_total_price(user.get('id'))

    if len(cart_products) > 0:
        cart_product_name = {
            "uz": "name_uz",
            "ru": "name_ru",
            "en": "name_en",
        }

        text = ""
        for index, cart_product in enumerate(cart_products, start=1):
            product = db.get_product(cart_product.get('product_id'))
            text += f"<b>{index}. {product.get(cart_product_name.get(lang))}, x{cart_product.get('quantity')}</b>\n"
            text += f"      {cart_product.get('quantity')} x {format_price_digits(cart_product.get('total_price') / cart_product.get('quantity'))} = {format_price_digits(cart_product.get('total_price'))} uzs\n\n"
        text += f"<b>{total.get(lang)}: {format_price_digits(cart_products_total_price)} uzs</b>"

        await call.message.edit_text(
            text=text,
            reply_markup=generate_cart_overall_menu(cart_products, user.get('id'), lang)
        )

    else:
        await call.message.answer(text=f"{cart_empty.get(lang)}", reply_markup=generate_main_menu(lang))
        await call.message.delete()
