from config import TG_API_TOKEN
from notion import getAmountOfCurrencies, addNewPage, deletePage

from states.IncomeForm import IncomeForm
from states.ExpenseForm import ExpenseForm
from filters.IsCorrectNumber import IsCorrectNumber
from keyboards.currency import currency_keyboard

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TG_API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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
    await message.reply("Choose currency", reply_markup=currency_keyboard)


@dp.message_handler(lambda message: message.text in ['CZK', 'RUB', 'EUR', 'USD'], state=IncomeForm.currency)
async def process_income_currency(message: types.Message, state: FSMContext):
    await IncomeForm.next()
    await state.update_data(currency=message.text)
    await message.reply("Input amount of income", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text not in ['CZK', 'RUB', 'EUR', 'USD'], state=IncomeForm.currency)
async def process_income_currency_incorrect(message: types.Message):
    await message.reply("Incorrect currency.\nChoose currency")


@dp.message_handler(IsCorrectNumber(), state=IncomeForm.amount)
async def process_income_amount(message: types.Message, state: FSMContext):
    await IncomeForm.next()
    await state.update_data(amount=float(message.text))
    await message.reply("Input any comment (optional)")


@dp.message_handler(state=IncomeForm.amount)
async def process_income_amount_incorrect(message: types.Message):
    await message.reply("Incorrect number.\nInput amount of income")


@dp.message_handler(state=IncomeForm.comment)
async def process_income_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    async with state.proxy() as data:
        with open("last_added.txt", "w") as f:
            f.write(addNewPage('income', '-', data['currency'], data['amount'], data['comment']))
    await state.finish()


@dp.message_handler(commands='expense')
async def start_expense(message: types.Message):
    await ExpenseForm.name.set()
    await message.reply("Input name of item")


@dp.message_handler(state=ExpenseForm.name)
async def process_expense_name(message: types.Message, state: FSMContext):
    await ExpenseForm.next()
    await state.update_data(name=message.text)
    await message.reply("Choose currency", reply_markup=currency_keyboard)


@dp.message_handler(lambda message: message.text in ['CZK', 'RUB', 'EUR', 'USD'], state=ExpenseForm.currency)
async def process_expense_currency(message: types.Message, state: FSMContext):
    await ExpenseForm.next()
    await state.update_data(currency=message.text)
    await message.reply("Input amount of expense", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda message: message.text not in ['CZK', 'RUB', 'EUR', 'USD'], state=ExpenseForm.currency)
async def process_expense_currency_incorrect(message: types.Message):
    await message.reply("Incorrect currency.")


@dp.message_handler(IsCorrectNumber(), state=ExpenseForm.amount)
async def process_expense_amount(message: types.Message, state: FSMContext):
    await ExpenseForm.next()
    await state.update_data(amount=float(message.text))
    await message.reply("Input any comment (optional)")


@dp.message_handler(state=ExpenseForm.amount)
async def process_expense_amount_incorrect(message: types.Message):
    await message.reply("Incorrect number.\nInput amount of expense")


@dp.message_handler(state=ExpenseForm.comment)
async def process_expense_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    async with state.proxy() as data:
        with open("last_added.txt", "w") as f:
            f.write(addNewPage('expense', data['name'], data['currency'], data['amount'], data['comment']))
    await state.finish()


@dp.message_handler(commands='del')
async def delete_last_record(message: types.Message):
    try:
        with open("last_added.txt", "r") as f:
            to_delete = f.readline()
            if len(to_delete) == 0:
                raise ValueError
            await message.reply("Last page has been deleted")
            deletePage(to_delete)

        with open("last_added.txt", "w") as _:
            pass
    except:
        await message.reply("There is no page to delete")

    # await message.reply("This function is in reconstruction")


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
