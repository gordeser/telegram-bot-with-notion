from config import TG_API_TOKEN

from notion import getAmountOfCurrencies

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TG_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class IncomeForm(StatesGroup):
    currency = State()
    amount = State()
    comment = State()


@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands='balance')
async def show_balance(message: types.Message):
    currencies = getAmountOfCurrencies()

    to_send = f"""
Your balances
<b>CZK</b>: <i>{currencies['CZK']:.2f}</i>
<b>RUB</b>: <i>{currencies['RUB']:.2f}</i>
<b>EUR</b>: <i>{currencies['EUR']:.2f}</i>
<b>USD</b>: <i>{currencies['USD']:.2f}</i>"""

    await message.reply(to_send, parse_mode='html')


@dp.message_handler(commands='income')
async def start_income(message: types.Message):
    await IncomeForm.currency.set()
    await message.reply("Input currency (available: CZK, RUB, EUR, USD)")


@dp.message_handler(lambda message: message.text in ['CZK', 'RUB', 'EUR', 'USD'], state=IncomeForm.currency)
async def process_currency(message: types.Message, state: FSMContext):
    await IncomeForm.next()
    await state.update_data(currency=message.text)
    await message.reply("Input amount of income")


@dp.message_handler(lambda message: message.text not in ['CZK', 'RUB', 'EUR', 'USD'], state=IncomeForm.currency)
async def process_invalid_currency(message: types.Message):
    await message.reply("Incorrect currency.\nInput currency (available: CZK, RUB, EUR, USD)")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
