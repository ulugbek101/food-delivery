from aiogram.fsm.state import State, StatesGroup


class LanguageState(StatesGroup):
    lang = State()
