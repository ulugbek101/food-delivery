from aiogram.fsm.state import State, StatesGroup


class PhoneNumberState(StatesGroup):
    phone_number = State()
