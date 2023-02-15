from aiogram import types

currency_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
currency_keyboard.add("CZK", "RUB")
currency_keyboard.add("EUR", "USD")