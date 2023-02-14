from aiogram.dispatcher.filters.state import State, StatesGroup


class IncomeForm(StatesGroup):
    currency = State()
    amount = State()
    comment = State()
