from datetime import datetime

from geopy.distance import geodesic

from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from keyboards.reply.payment_method_menu import generate_payment_method_menu
from router import router
from loader import db
from states.cart_holder_details import CartHolderDetails
from localization.i18n import (cart_overall_ready, request_phone_number, phone_number_invalid,
                               phone_number_valid, request_location, back_button_text, new_location_saved,
                               location_not_found, request_full_address, request_deliver_type, invalid_full_address,
                               invalid_shipping_option, distance_for_branch, final_confirmation, confirm, decline,
                               cancelled, order_saved, one_minute, clear_locations, locations_cleared,
                               deliver_type_text, delivery_time_select, incorrect_deliver_time, order_history_text,
                               order_status, card_payments_not_being_served, select_payment_method, payment_method_menu,
                               cart)
from keyboards.reply.contacts import generate_request_contact_menu
from keyboards.reply.locations import generate_send_location_menu, generate_locations_menu
from keyboards.reply.select_deliver_type_menu import generate_select_deliver_type_menu
from keyboards.reply.confirmation_menu import generate_confirmation_menu
from keyboards.reply.main_menu import generate_main_menu
from keyboards.reply.deliver_options_menu import generate_deliver_options_menu
from keyboards.reply.deliver_time_menu import generate_deliver_time_menu
from keyboards.inline.order_status_menu import generate_order_status_menu
from utils.format_price import format_price_digits
from validations.phone_number import validate_phone_number
from handlers.users.back import show_cart
from loader import branches_locations, PAYMENT_PROVIDER_TOKEN


# @router.message(Command(commands='buy', ignore_case=True))
# async def send_invoice(message: types.Message):
#     await message.answer_invoice(
#         title="Yoour invoice title",
#         description="This is your very very long description",
#         prices=[types.LabeledPrice(label="Product1", amount=1000000),
#                 types.LabeledPrice(label="Product2", amount=2000000)],
#         need_shipping_address=True,
#         need_name=True,
#         need_email=True,
#         need_phone_number=True,
#         is_flexible=True,
#         currency="uzs",
#         payload="Some data",
#         start_parameter="indian-food_delivery",
#         suggested_tip_amounts=[500000, 1000000, 1500000],
#         max_tip_amount=1500000,
#         provider_token=PAYMENT_PROVIDER_TOKEN
#     )

@router.message(F.text.in_(cart_overall_ready.values()))
async def start_shipping(message: types.Message, state: FSMContext):
    user = db.get_user(message.from_user.id)
    lang = user.get('language_code')

    if not user.get('phone_number'):
        await state.set_state(CartHolderDetails.phone_number)
        await message.answer(text=f"<b>{request_phone_number.get(lang)}</b>",
                             reply_markup=generate_request_contact_menu(lang))

    else:
        await state.update_data(phone_number=user.get('phone_number'))
        await state.set_state(CartHolderDetails.location)

        user_locations = db.get_user_locations(user.get("id"))

        if user_locations:
            await message.answer(text=f"<b>{phone_number_valid.get(lang)}</b>")
            await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                 reply_markup=generate_locations_menu(lang, locations_list=user_locations))
        else:
            await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                 reply_markup=generate_send_location_menu(lang))

    db.update_last_step(message.from_user.id, "cart_overall")


@router.message(CartHolderDetails.phone_number)
async def update_phone_number(message: types.Message, state: FSMContext):
    if message.text and message.text.strip() in back_button_text.values():
        await state.clear()
        await show_cart(message)

    else:
        lang = db.get_user_language(message.from_user.id)
        user_id = db.get_user(message.from_user.id).get('id')
        user_locations = db.get_user_locations(user_id)

        if not message.contact:
            if validate_phone_number(phone_number=message.text):
                phone_number = message.text
            else:
                await message.answer(text=f"<b>{phone_number_invalid.get(lang)}</b>")
                phone_number = None

        else:
            phone_number = f"+{message.contact.phone_number}"

        if phone_number:
            if user_locations:
                await message.answer(text=f"<b>{phone_number_valid.get(lang)}</b>")
                await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                     reply_markup=generate_locations_menu(lang, locations_list=user_locations))
            else:
                await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                     reply_markup=generate_send_location_menu(lang))

            await state.update_data(phone_number=phone_number)
            await state.set_state(CartHolderDetails.location)


@router.message(CartHolderDetails.location)
async def update_location(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)
    user = db.get_user(message.from_user.id)

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.phone_number)
        await message.answer(text=f"<b>{request_phone_number.get(lang)}</b>",
                             reply_markup=generate_request_contact_menu(lang))

    elif message.text and message.text.strip() in clear_locations.values():
        db.clear_locations_list(user.get("id"))
        locations_list = db.get_user_locations(message.from_user.id)
        markup = generate_locations_menu(lang, locations_list)
        markup.keyboard.pop(-1)
        await message.answer(text=f"{locations_cleared.get(lang)}", reply_markup=markup)

    else:
        user_locations = db.get_user_locations(user.get('id'))

        if message.text and message.text.strip() in [user_location.get('full_address') for user_location in
                                                     user_locations]:
            await state.update_data(location=())
            await state.update_data(full_address=message.text)
            await state.set_state(CartHolderDetails.deliver_type)
            await message.answer(text=f"<b>{request_deliver_type.get(lang)}</b>",
                                 reply_markup=generate_select_deliver_type_menu(lang))

        elif message.location:
            latitude = message.location.latitude
            longitude = message.location.longitude

            # TODO: isolate to a separate file
            markup = types.ReplyKeyboardMarkup(
                keyboard=[[types.KeyboardButton(text=f"{back_button_text.get(lang)}")]],
                resize_keyboard=True,
            )

            await state.update_data(location=(latitude, longitude))
            await state.set_state(CartHolderDetails.full_address)
            await message.answer(text=f"<b>{new_location_saved.get(lang)}</b>")
            await message.answer(text=f"<b>{request_full_address.get(lang)}</b>", reply_markup=markup)

        else:
            await message.answer(text=f"<b>{location_not_found.get(lang)}</b>")


@router.message(CartHolderDetails.full_address)
async def update_full_address(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)
    full_address = message.text

    if message.text and message.text.strip() in back_button_text.values():
        user = db.get_user(message.from_user.id)
        user_locations = db.get_user_locations(user.get('id'))
        await state.set_state(CartHolderDetails.location)

        if user_locations:
            await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                 reply_markup=generate_locations_menu(lang, locations_list=user_locations))
        else:
            await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                 reply_markup=generate_send_location_menu(lang))

    elif message.text:
        user = db.get_user(message.from_user.id)
        fsm_state = await state.get_data()
        coordinates = fsm_state.get("location")
        coordinates = f"{coordinates[0]},{coordinates[1]}"

        await state.update_data(full_address=full_address)
        await state.set_state(CartHolderDetails.deliver_type)
        await message.answer(text=f"<b>{request_deliver_type.get(lang)}</b>",
                             reply_markup=generate_select_deliver_type_menu(lang))
        db.add_to_locations(user.get("id"), coordinates, full_address)

    else:
        await message.answer(text=f"<b>{invalid_full_address.get(lang)}</b>")


@router.message(CartHolderDetails.deliver_type)
async def update_delivery_type(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)
    user = db.get_user(message.from_user.id)
    user_locations = db.get_user_locations(user.get('id'))

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.location)

        if user_locations:
            await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                 reply_markup=generate_locations_menu(lang, locations_list=user_locations))
        else:
            await message.answer(text=f"<b>{request_location.get(lang)}</b>",
                                 reply_markup=generate_send_location_menu(lang))

    elif message.text.strip() in ["🚚 Yetkazib berish", "🚚 Доставка", "🚚 Delivery"]:
        await state.update_data(deliver_type="deliver")
        await state.set_state(CartHolderDetails.deliver_option)
        await message.answer(text=f"<b>{deliver_type_text.get(lang)}</b>",
                             reply_markup=generate_deliver_options_menu(lang))

    elif message.text.strip() in ["📦 Olib ketish", "📦 Заберу сам", "📦 Take away"]:
        await state.update_data(deliver_type="take away")
        users_state = await state.get_data()

        if users_state.get('location'):
            location = users_state.get('location')
        else:
            location = db.get_user_location(user.get("id"), users_state.get("full_address")).split(",")

        distance = geodesic(location, branches_locations[0]).kilometers
        await message.answer(text=f"<b>{distance_for_branch.get(lang).format(round(distance, 2))}</b>")
        await message.answer_location(latitude=branches_locations[0][0],
                                      longitude=branches_locations[0][1])
        await message.answer(text=f"<b>{final_confirmation.get(lang)}</b>",
                             reply_markup=generate_confirmation_menu(lang))
        await state.set_state(CartHolderDetails.final_confirmation)

    else:
        await message.answer(text=f"<b>{invalid_shipping_option.get(lang)}</b>")


@router.message(CartHolderDetails.deliver_option)
async def update_deliver_option(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.deliver_type)
        await message.answer(text=f"<b>{request_deliver_type.get(lang)}</b>",
                             reply_markup=generate_select_deliver_type_menu(lang))

    elif message.text in ["🚕 Zudlik bilan yetkazish", "🚕 Срочная доставка", "🚕 Instant delivery"]:
        await state.update_data(deliver_option="instant")
        await state.set_state(CartHolderDetails.final_confirmation)
        await message.answer(text=f"<b>{final_confirmation.get(lang)}</b>",
                             reply_markup=generate_confirmation_menu(lang))
        await state.set_state(CartHolderDetails.final_confirmation)

    elif message.text in ["🚚 Standart yetkizish", "🚚 Стандартная доставка", "🚚 Standart delivery"]:
        await state.update_data(deliver_option="standart")
        await state.set_state(CartHolderDetails.deliver_time)
        await message.answer(text=f"<b>{delivery_time_select.get(lang)}</b>",
                             reply_markup=generate_deliver_time_menu(lang))

    else:
        await message.answer(text=f"<b>{deliver_type_text.get(lang)}</b>")


@router.message(CartHolderDetails.deliver_time)
async def update_deliver_time(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.deliver_type)
        await message.answer(text=f"<b>{deliver_type_text.get(lang)}</b>",
                             reply_markup=generate_deliver_options_menu(lang))

    elif message.text:
        time = message.text[:2]
        now = datetime.now().time().hour

        if message.text.replace(":", "").isdigit():
            time = int(time)

            if time in [now + 3, now + 4, now + 5, now + 6]:
                await state.update_data(deliver_time=message.text)
                await state.set_state(CartHolderDetails.final_confirmation)
                await message.answer(text=f"<b>{final_confirmation.get(lang)}</b>",
                                     reply_markup=generate_confirmation_menu(lang))
                await state.set_state(CartHolderDetails.final_confirmation)

            else:
                await message.answer(text=f"<b>{incorrect_deliver_time.get(lang)}</b>")

        else:
            await message.answer(text=f"<b>{incorrect_deliver_time.get(lang)}</b>")

    else:
        await message.answer(text=f"<b>{delivery_time_select.get(lang)}</b>")


@router.message(CartHolderDetails.final_confirmation)
async def update_final_confirmation(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.deliver_type)
        await message.answer(text=f"<b>{request_deliver_type.get(lang)}</b>",
                             reply_markup=generate_select_deliver_type_menu(lang))

    elif message.text and message.text in confirm.values():
        lang = db.get_user_language(message.from_user.id)

        await message.answer(text=f"<b>{select_payment_method.get(lang)}</b>",
                             reply_markup=generate_payment_method_menu(lang))
        await state.set_state(CartHolderDetails.payment_method)

    elif message.text and message.text in decline.values():
        await message.answer(text=f"<b>{cancelled.get(lang)}</b>")
        await show_cart(message)

    else:
        await message.answer(text=f"<b>{final_confirmation.get(lang)}</b>")


@router.message(CartHolderDetails.payment_method)
async def update_payment_method(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.final_confirmation)
        await message.answer(text=f"<b>{final_confirmation.get(lang)}</b>",
                             reply_markup=generate_confirmation_menu(lang))

    elif message.text and message.text in payment_method_menu.get(lang):
        state_obj = await state.get_data()

        await message.answer(text=f"<b>{one_minute.get(lang)}</b>", reply_markup=generate_main_menu(lang))

        if message.text == payment_method_menu.get(lang)[0]:  # Cash
            payment_method="cash"

        elif message.text == payment_method_menu.get(lang)[1]:  # Card
            payment_method="card"

        user = db.get_user(message.from_user.id)
        users_cart_products = db.get_users_cart_products(user.get('id'))


        # Add user's cart products to orders list and create a new order with delivery time and shipping option
        db.add_to_orders(user.get("id"),
                         users_cart_products,
                         state_obj.get("deliver_type"),
                         state_obj.get("deliver_time"),
                         payment_method)

        # Get the latest order that was created
        order = db.get_last_user_order(user.get("id"))

        order_text = order_history_text.get(lang)
        text = f"{order_text.get('title')}: №{order.get('id')}\n\n\n"
        products = db.get_order_products(order.get('id'))

        overall_price = 0
        for index, product_object in enumerate(products, start=1):
            product = db.get_product(product_object.get('product_id'))
            quantity = product_object.get("quantity")
            total_price = product_object.get("total_price")

            overall_price += total_price

            text += f"{index}) {product.get(f'name_{lang}')}, x{quantity} - {format_price_digits(int(total_price))} UZS\n\n"

        date = order.get("created_date")
        status = order.get("status")
        text += f"\n{'💸' if order.get('payment_method') == 'cash' else '💳'} {order_text.get('payment_method').get(order.get('payment_method'))}"
        text += f"\n🏁 {order_status.get(status).get(lang)}"
        text += f"\n🗓️ {date} | {order.get('created_time')}"
        text += f"\n\n{order_text.get('total')}: {format_price_digits(int(overall_price))} UZS"

        if payment_method == "card":
            prices = [
                types.LabeledPrice(label=f"x{product.get('quantity')} {db.get_product(product.get('product_id')).get(f'name_{lang}')}",
                                   amount=int(product.get('total_price')) * 100)
                for product in users_cart_products
            ]

            products_names = []
            for product in users_cart_products:
                product_name = db.get_product(product.get("product_id")).get(f"name_{lang}")
                products_names.append(product_name)

            description = ", ".join([product_name for product_name in products_names])

            await message.answer_invoice(
                title=f"{cart.get(lang)}",
                description=description,
                prices=prices,
                need_shipping_address=True,
                need_name=True,
                need_phone_number=True,
                is_flexible=True,
                currency="UZS",
                payload="Some data",
                start_parameter="indian-food_delivery",
                # suggested_tip_amounts=[100000, 200000, 500000, 700000, 1000000, 1500000],
                # max_tip_amount=1500000,
                provider_token=PAYMENT_PROVIDER_TOKEN)
        else:
            await message.answer(text=f"<b>{text}</b>")
            await message.answer(text=f"<b>{order_saved.get(lang)}</b>",
                                 reply_markup=generate_order_status_menu(lang, order.get("id")))

        # Update user's orders count in users table
        db.update_users_order_count(user.get("id"))

        # Clear user's cart products
        db.clear_user_cart(user.get('id'))

        # Clear state
        await state.clear()

    else:
        await message.answer(text=f"<b>{select_payment_method.get(lang)}</b>")


@router.shipping_query()
async def show_shipping_options(shipping_query: types.ShippingQuery):
    await shipping_query.answer(ok=True,
                                error_message="Some error happened",
                                shipping_options=[
                                    types.ShippingOption(id="express", title="As soon as fast", prices=[
                                        types.LabeledPrice(label="Express shipping", amount=1500000)]),
                                    types.ShippingOption(id="normal", title="Normal delivery", prices=[
                                        types.LabeledPrice(label="Normal shipping", amount=500000),
                                    ])
                                ])


@router.pre_checkout_query(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    lang = db.get_user_language(pre_checkout_query.from_user.id)
    await pre_checkout_query.answer(ok=False, error_message=f"{card_payments_not_being_served.get(lang)}")
