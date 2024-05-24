from aiogram.fsm.state import StatesGroup, State


class NewLocationConfirmation(StatesGroup):
    user_wants_new_location = State()