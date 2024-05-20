from aiogram import F, types

from router import router
from loader import db
from localization.i18n import cart, total
from utils.format_price import format_price_digits
from keyboards.inline.cart_overall_menu import generate_cart_overall_menu
from keyboards.reply.cart_overall_ready import generate_cart_overall_ready_menu


@router.message(F.text == "/cart")
@router.message(F.text.in_({"🛒 Korzinkam", "🛒 Моя корзина", "🛒 My cart"}))
async def show_cart(message: types.Message):
    lang = db.get_user_language(message.from_user.id)
    user = db.get_user(message.from_user.id)
    cart_products = db.get_users_cart_products(user.get('id'))
    cart_products_total_price = db.get_users_cart_total_price(user.get('id'))

    cart_product_name = {
        "uz": "name_uz",
        "ru": "name_ru",
        "en": "name_en",
    }

    text = f"<b>{cart.get(lang)}:</b>"
    await message.answer(
        text=text,
        reply_markup=generate_cart_overall_ready_menu(lang),
    )

    text = ""
    for index, cart_product in enumerate(cart_products, start=1):
        product = db.get_product(cart_product.get('product_id'))
        text += f"<b>{index}. {product.get(cart_product_name.get(lang))}, x{cart_product.get('quantity')}</b>\n"
        text += f"      {cart_product.get('quantity')} x {format_price_digits(cart_product.get('total_price') / cart_product.get('quantity'))} = {format_price_digits(cart_product.get('total_price'))} uzs\n\n"
    text += f"<b>{total.get(lang)}: {format_price_digits(cart_products_total_price)} uzs</b>"

    await message.answer(
        text=text,
        reply_markup=generate_cart_overall_menu(cart_products, user.get('id'), lang)
    )

    db.update_last_step(message.from_user.id, "cart")
