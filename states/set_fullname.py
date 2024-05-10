from aiogram.fsm.state import State, StatesGroup


class FullnameState(StatesGroup):
    fullname = State()
