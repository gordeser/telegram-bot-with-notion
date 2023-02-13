from config import API_TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['balance'])
async def show_balance(message: types.Message):
    CZK = 120.004343
    RUB = 456.0054354
    EUR = 789.32654654
    USD = 532.55654654

    # balances = {
    #     'CZK': CZK,
    #     'RUB': RUB,
    #     'EUR': EUR,
    #     'USD': USD
    # }

    to_send = f"""
Your balances
<b>CZK</b>: <i>{CZK:.2f}</i>
<b>RUB</b>: <i>{RUB:.2f}</i>
<b>EUR</b>: <i>{EUR:.2f}</i>
<b>USD</b>: <i>{USD:.2f}</i>"""

    await message.reply(to_send, parse_mode='html')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
