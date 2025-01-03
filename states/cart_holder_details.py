from aiogram.fsm.state import StatesGroup, State


class CartHolderDetails(StatesGroup):
    phone_number = State()
    location = State()
    full_address = State()
    deliver_type = State()
    deliver_option = State()
    deliver_time = State()
    time = State()
    payment_method = State()
    final_confirmation = State()
