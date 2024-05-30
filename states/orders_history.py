from aiogram.fsm.state import StatesGroup, State


class OrdersHistory(StatesGroup):
    name = State()
