from aiogram import types
from aiogram.dispatcher.filters import Filter


class IsIncorrectNumber(Filter):
    async def check(self, message: types.Message):
        try:
            float(message.text)
            return False
        except ValueError:
            return True
