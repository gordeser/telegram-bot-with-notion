from aiogram import types
from aiogram.dispatcher.filters import Filter


class IsCorrectNumber(Filter):
    async def check(self, message: types.Message):
        try:
            float(message.text)
            return True
        except ValueError:
            return False
