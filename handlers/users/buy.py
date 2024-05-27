from geopy.distance import geodesic

from aiogram.filters.command import Command
from aiogram import types, F
from aiogram.fsm.context import FSMContext

from router import router
from loader import db
from states.cart_holder_details import CartHolderDetails
from localization.i18n import (cart_overall_ready, request_phone_number, phone_number_invalid,
                               phone_number_valid, request_location, back_button_text, new_location_saved,
                               location_not_found, request_full_address, request_deliver_type, invalid_full_address,
                               invalid_shipping_option, distance_for_branch, final_confirmation, confirm, decline,
                               cancelled, order_saved, one_minute, clear_locations, locations_cleared)
from keyboards.reply.contacts import generate_request_contact_menu
from keyboards.reply.locations import generate_send_location_menu, generate_locations_menu
from keyboards.reply.select_deliver_type_menu import generate_select_deliver_type_menu
from keyboards.reply.confirmation_menu import generate_confirmation_menu
from keyboards.reply.main_menu import generate_main_menu
from keyboards.inline.order_status_menu import generate_order_status_menu
from validations.phone_number import validate_phone_number
from handlers.users.back import show_cart
from loader import branches_locations

PAYMENT_TOKEN = "398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065"


@router.message(Command(commands='buy', ignore_case=True))
async def send_invoice(message: types.Message):
    await message.answer_invoice(
        title="Yoour invoice title",
        description="This is your very very long description",
        prices=[types.LabeledPrice(label="Product1", amount=1000000),
                types.LabeledPrice(label="Product2", amount=2000000)],
        need_shipping_address=True,
        need_name=True,
        need_email=True,
        need_phone_number=True,
        is_flexible=True,
        currency="uzs",
        payload="Some data",
        protect_content=True,
        start_parameter="indian-food_delivery",
        suggested_tip_amounts=[500000, 1000000, 1500000],
        max_tip_amount=1500000,
        provider_token=PAYMENT_TOKEN
    )


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
        pass

    elif message.text.strip() in ["📦 Olib ketish", "📦 Заберу сам", "📦 Take away"]:
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


@router.message(CartHolderDetails.final_confirmation)
async def update_final_confirmation(message: types.Message, state: FSMContext):
    lang = db.get_user_language(message.from_user.id)

    if message.text and message.text.strip() in back_button_text.values():
        await state.set_state(CartHolderDetails.deliver_type)
        await message.answer(text=f"<b>{request_deliver_type.get(lang)}</b>",
                             reply_markup=generate_select_deliver_type_menu(lang))

    elif message.text and message.text in confirm.values():
        await message.answer(text=f"<b>{one_minute.get(lang)}</b>", reply_markup=generate_main_menu(lang))
        await message.answer(text=f"<b>{order_saved.get(lang)}</b>", reply_markup=generate_order_status_menu(lang))
        await state.clear()
        user = db.get_user(message.from_user.id)
        users_cart_products = db.get_users_cart_products(user.get('id'))
        db.add_to_orders(user.get("id"), users_cart_products)
        db.update_users_order_count(user.get("id"))
        db.clear_user_cart(user.get('id'))

    elif message.text and message.text in decline.values():
        await message.answer(text=f"<b>{cancelled.get(lang)}</b>")
        await show_cart(message)

    else:
        await message.answer(text=f"<b>{final_confirmation.get(lang)}</b>")
