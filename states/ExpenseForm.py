from aiogram.dispatcher.filters.state import State, StatesGroup


class ExpenseForm(StatesGroup):
    name = State()
    currency = State()
    amount = State()
    comment = State()
