from aiogram import types, F
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from states.orders_history import OrdersHistory
from keyboards.reply.orders_hitory_menu import generate_user_orders_menu
from keyboards.reply.main_menu import generate_main_menu
from keyboards.inline.order_status_menu import generate_order_status_menu
from localization.i18n import (select_order_from_orders, back_button_text, main_menu_title, order_not_found,
                               order_history_text, order_status, no_orders_history)
from utils.format_price import format_price_digits


@router.message(lambda message: message.text in ["📃 Buyurtmalar tarixi", "📃 История заказов", "📃 Orders history"])
async def orders_history(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    lang = user.get("language_code")
    orders_list = db.get_user_orders(user.get("id"))
    db.update_last_step(message.from_user.id, "my_orders")

    if len(orders_list):
        await state.set_state(OrdersHistory.name)
        await message.answer(text=f"<b>{select_order_from_orders.get(lang)}</b>",
                             reply_markup=generate_user_orders_menu(lang, orders_list))
    else:
        await message.answer(text=f"<b>{no_orders_history.get(lang)}</b>")


@router.message(OrdersHistory.name)
async def show_order(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    lang = user.get("language_code")

    if message.text.strip() in back_button_text.values():
        await state.clear()
        await message.answer(text=f"{main_menu_title.get(lang)}",
                             reply_markup=generate_main_menu(lang))
    else:
        try:
            order_id = int(message.text[:message.text.index("-")].strip().replace("№", ""))
        except:
            order_id = None

        if order_id:
            await state.update_data(name=message.text)
            order = db.get_user_order(order_id)

            if order:
                products = db.get_order_products(order.get("id"))
                order_text = order_history_text.get(lang)
                response_text = f"{order_text.get('title')}: №{order.get('id')} | {order.get('created_date')} | {order.get('created_time')}\n\n\n"

                overall_price = 0
                for index, product_object in enumerate(products, start=1):
                    product = db.get_product(product_object.get("product_id"))
                    quantity = product_object.get("quantity")
                    total_price = product_object.get("total_price")
                    overall_price += total_price

                    response_text += f"{index}) {product.get(f'name_{lang}')}, x{quantity} - {format_price_digits(int(total_price))} UZS\n\n"

                date = order.get("created_date")
                status = order.get("status")
                response_text += f"\n🗓️ {date}"
                response_text += f"\n🏁 {order_status.get(status).get(lang)}"
                response_text += f"\n\n{order_text.get('total')}: {format_price_digits(int(overall_price))} UZS"

                await message.answer(text=f"<b>{response_text}</b>",
                                     reply_markup=generate_order_status_menu(lang, order.get("id")))

            else:
                await message.answer(text=f"{order_not_found.get(lang)}")
        else:
            await message.answer(text=f"{order_not_found.get(lang)}")
