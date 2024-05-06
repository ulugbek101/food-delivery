from aiogram.fsm.state import State, StatesGroup


class SetLanguageState(StatesGroup):
    lang = State()
