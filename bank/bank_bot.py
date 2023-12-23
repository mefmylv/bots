import random
from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig , INFO
from bank_token import token
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


import sqlite3

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

data_base = sqlite3.connect('bank.db')
cursor = data_base.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users
(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER ,
USERNAME TEXT ,
FIRST_NAME TEXT NOT NULL,
LAST_NAME TEXT NOT NULL,
Card_Number INTEGER,
Password TEXT,
BALANCE INTEGER DEFAULT 0,
Phone_Number Integer

);
''')

start_buttons = [
    types.KeyboardButton('/Регистрация'),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)
indentify_button = [
    types.KeyboardButton('Ввести пароль')
]

indentify_keyboard = types.ReplyKeyboardMarkup().add(*indentify_button)

after_password_button = [
    types.KeyboardButton('Баланс'),
    types.KeyboardButton('Перевод'),
    types.KeyboardButton('Пополнить'),
]
after_password_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*after_password_button)

@dp.message_handler(commands='start')
async def start(message:types.Message):
    await message.answer('Это банк')
    user_id = message.from_user.id

    user_data = cursor.execute("SELECT * FROM users WHERE TELEGRAM_ID = ?", (user_id,)).fetchone()

    if user_data:
        await message.answer('Введите Пароль',reply_markup=indentify_keyboard)
    else:
        await message.answer('Зарегистрируйтесть',reply_markup=start_keyboard)


class PasswordState(StatesGroup):
    password = State()

@dp.message_handler(text='Ввести пароль')
async def input_password(message: types.Message, state: FSMContext):
    await message.reply('Введите Пароль')
    await PasswordState.password.set()

@dp.message_handler(state=PasswordState.password)
async def input_password(message:types.Message,state:FSMContext):
    await state.update_data(password=message.text)
    data = await storage.get_data(user=message.from_user.id)
    print(data)
    if data['password'] == message.text:
        await message.reply('Вы успешно Вошли', reply_markup=after_password_keyboard)
        await state.finish()
    else:
        await message.answer('Неправильный Пароль')



class RegState(StatesGroup):
    name = State()
    last_name = State()
    password = State()
    phone_number = State()

@dp.message_handler(commands='Регистрация')
async def reg(message:types.Message):
    user_id = message.from_user.id
    user_data = cursor.execute("SELECT * FROM users WHERE TELEGRAM_ID = ?", (user_id,)).fetchone()

    if user_data:
        await message.answer('Вы уже Зарегестрировались ,Введите Пароль', reply_markup=indentify_keyboard)
    else:
        await message.answer('Вы еще не зарегистрировались ,Зарегистрируйтесть')
        await message.answer('Заполните Анкету для регистрации')
        await message.answer('Введите Свое Имя')
        await RegState.name.set()

@dp.message_handler(state=RegState.name)
async def get_lastname(message:types.Message, state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Теперь введите фамилию')
    await RegState.last_name.set()

@dp.message_handler(state=RegState.last_name)
async def get_passwoord(message:types.Message, state:FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer('А теперь придумайте пароль')
    await RegState.password.set()

@dp.message_handler(state=RegState.password)
async def get_phone_number(message:types.Message, state:FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Отлично а теперь отправьте свой номер телефона')
    await RegState.phone_number.set()

@dp.message_handler(state=RegState.phone_number)
async def get_(message:types.Message, state:FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer('Вы успешно прошли регистрацию')
    result = await storage.get_data(user=message.from_user.id)
    card_number = random.randint(1000000000000000,9999999999999999)
    print(result)
    cursor.execute('INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?);',
                   (None, message.from_user.id, message.from_user.username, result['name'], result['last_name'],
                    card_number, result['password'], 0.0, result['phone_number']))

    cursor.connection.commit()
    await RegState.phone_number.set()

@dp.message_handler(text='Баланс')
async def balance(message: types.Message):
    cursor.execute('SELECT BALANCE FROM users WHERE TELEGRAM_ID = ?;', (message.from_user.id,))
    result = cursor.fetchone()

    if result:
        balance = result[0]
        await message.answer(f'Ваш баланс: {balance}')
    else:
        await message.answer('У вас нет баланса или произошла ошибка.')


class TransferState(StatesGroup):
    card_number = State()
    amount = State()



@dp.message_handler(text='Перевод')
async def get_card_num(message: types.Message, state:FSMContext):
    await message.answer('Введите номер карты пользователя, которому вы хотите перевести')
    await TransferState.card_number.set()
@dp.message_handler(state=TransferState.card_number)
async def transfer_amount(message: types.Message, state: FSMContext):
    await message.answer('Введите сумму которую перевести')
    await state.update_data(card_number=message.text)
    await TransferState.amount.set()




@dp.message_handler(state=TransferState.amount)
async def transfer(message:types.Message, state:FSMContext):
    await state.update_data(amount=message.text)
    try:
        amount = int(message.text)
        card_number_to = await state.get_data()
        card_number_to = card_number_to['card_number']
        cursor.execute('UPDATE users SET BALANCE = BALANCE - ? WHERE TELEGRAM_ID = ?;', (amount, message.from_user.id))
        cursor.execute('UPDATE users SET BALANCE = BALANCE + ? WHERE Card_Number = ?;', (amount, card_number_to))

        await message.reply(f'Вы успешно перевели {amount} пользователю с номером карты {card_number_to}')
        await state.finish()
    except ValueError:
        await message.reply('Пожалуйста, введите числовое значение для перевода.')
    except sqlite3.Error as e:
        await message.reply(f'Произошла ошибка при выполнении перевода: {e}')




class BalanceState(StatesGroup):
    text = State()
    amount = State()

@dp.message_handler(text='Пополнить')
async def input_amount(message:types.Message):
    await message.reply('На сколько вы хотите пополнить баланс')
    await BalanceState.text.set()

@dp.message_handler(state=BalanceState.text)
async def popolnenie(message: types.Message, state: FSMContext):
    try:
        amount = int(message.text)
        cursor.execute('UPDATE users SET BALANCE = BALANCE + ? WHERE TELEGRAM_ID = ?;', (amount, message.from_user.id))
        await message.reply(f'Вы успешно пополнили баланс на {amount}')
        await state.finish()
    except ValueError:
        await message.reply('Пожалуйста, введите числовое значение для пополнения баланса.')



executor.start_polling(dp, skip_updates=True)




