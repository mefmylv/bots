from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig, INFO
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
import random

from anon_token import token
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)


db = sqlite3.connect('anon_db')
cursor = db.cursor()

cursor.execute('''

CREATE TABLE IF NOT EXISTS ChatUSERS
(
ID INTEGER PRIMARY KEY,
TELEGRAM_ID INTEGER,
USERNAME TEXT,
FIRST_NAME TEXT,
SEX TEXT,
CONNECT_WITH INTEGER,
Rate INTEGER
);
       
''')


start_buttons = [
    types.KeyboardButton('Регистрация')
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)
search_buttons = [
    types.KeyboardButton('/finish'),
    types.KeyboardButton('/next')
]
search_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*search_buttons)
rate_buttons = [
    types.KeyboardButton('/Rate'),
    types.KeyboardButton('Назад')
]
rate_keyaboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*rate_buttons)

base_buttons = [
    types.KeyboardButton('Поиск'),
    types.KeyboardButton('О себе'),
    types.KeyboardButton('Рейтинг'),
]
base_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*base_buttons)

sex_buttons = [
    types.KeyboardButton('Мужской'),
    types.KeyboardButton('Женский')
]
sex_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*sex_buttons)
identify_buttons = [
    types.KeyboardButton('Я человек'),
    types.KeyboardButton('Я не человек')
]
identify_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*identify_buttons)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    message.answer('Добро пожаловать в Анонимный чат. Пожалуйста, зарегистрируйтесь', reply_markup=start_keyboard)
    user_id = message.from_user.id

    user_data = cursor.execute("SELECT * FROM ChatUSERS WHERE TELEGRAM_ID = ?", (user_id,)).fetchone()

    if user_data:
        await message.answer('Для того чтобы войти, подтвердите, что вы человек?', reply_markup=identify_keyboard)
    else:
        await message.answer('Зарегистрируйтесь', reply_markup=start_keyboard)


class RegState(StatesGroup):
    name = State()
    sex = State()


@dp.message_handler(text="Регистрация")
async def reg(message: types.Message):
    await message.answer("Введите имя")
    await RegState.name.set()


@dp.message_handler(state=RegState.name)
async def set_sex(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Какой у вас пол?', reply_markup=sex_keyboard)
    await RegState.sex.set()


@dp.message_handler(state=RegState.sex)
async def input_in_db(message: types.Message, state: FSMContext):
    await state.update_data(sex=message.text)
    result = await state.get_data()
    cursor.execute('INSERT INTO ChatUSERS (TELEGRAM_ID, USERNAME, FIRST_NAME, SEX) VALUES (?,?,?,?);',
                   (message.from_user.id, message.from_user.username, result['name'], result['sex']))

    cursor.connection.commit()
    await state.finish()
    await message.answer('Вы успешно зарегистрировались', reply_markup=base_keyboard)


@dp.message_handler(lambda message: message.text in ["Я человек", "Я не человек"], state="*")
async def handle_identify_choice(message: types.Message, state: FSMContext):
    if message.text == "Я человек":
        await message.answer('Отлично! Теперь давайте пройдем регистрацию.')
        await reg(message)
    else:
        await message.answer('Извините, но этот бот предназначен только для общения между людьми.')

chat_pairs = {}

@dp.message_handler(state='*', commands=['next'])
@dp.message_handler(state='*', text='Поиск')
async def cmd_next(message: types.Message):
    await message.answer('Ищем для вас человечка..', reply_markup=search_keyboard)

    all_user_ids = cursor.execute("SELECT TELEGRAM_ID FROM ChatUSERS").fetchall()
    current_user_id = message.from_user.id
    all_user_ids = [user_id for user_id in all_user_ids if user_id != current_user_id]

    def update_connect_with(user_id, connect_with):
        cursor.execute('UPDATE ChatUSERS SET CONNECT_WITH = ? WHERE TELEGRAM_ID = ?', (int(connect_with), int(user_id)))
        cursor.connection.commit()

    try:
        existing_pair = chat_pairs.get(current_user_id)
        if existing_pair:
            await message.answer('Вы уже связаны с кем-то. Завершите текущий диалог, чтобы начать новый.')
            return

        user_id_1 = random.choice(all_user_ids)[0]
        user_id_2 = random.choice([uid for uid in all_user_ids if uid != user_id_1])[0]

        while chat_pairs.get(user_id_1) == user_id_2 or chat_pairs.get(user_id_2) == user_id_1:
            user_id_1 = random.choice(all_user_ids)[0]
            user_id_2 = random.choice([uid for uid in all_user_ids if uid != user_id_1])[0]

        update_connect_with(user_id_1, current_user_id)
        update_connect_with(user_id_2, current_user_id)

        update_connect_with(current_user_id, user_id_1)
        update_connect_with(current_user_id, user_id_2)

        chat_pairs[user_id_1] = user_id_2
        chat_pairs[user_id_2] = user_id_1

        await message.answer('Диалог начался!')
        await message.bot.send_message(user_id_2, 'Диалог начался!')
        print(f"Успешно создан диалог между {current_user_id} и {user_id_1}")


    except IndexError:
        await message.answer('Недостаточно пользователей для общения.')
        print("Ошибка: Недостаточно пользователей для общения.")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text(message: types.Message):
    user_id = message.from_user.id
    if message.text == '/finish':
        await finish(message)
    elif message.text == '/Rate':
        await rate(message)
    else:
        if user_id in chat_pairs and chat_pairs[user_id] is not None:
            partner_id = chat_pairs[user_id]
            await bot.send_message(partner_id, f"Аноним: {message.text}")
            print(f"Отправлено сообщение пользователю {partner_id}: {message.text}")
        elif message.text == '/finish':
            await finish(message)
        else:
            await message.answer('Вам нужно начать диалог с помощью команды /next')
            print("Ошибка: Пользователь не связан с кем-то для общения.")
@dp.message_handler(commands=['finish'])
async def cmd_finish(message: types.Message):
    await finish(message)

async def finish(message: types.Message):
    user_id = message.from_user.id

    if user_id in chat_pairs and chat_pairs[user_id] is not None:
        partner_id = chat_pairs[user_id]

        chat_pairs.pop(user_id)
        chat_pairs.pop(partner_id)

        await bot.send_message(user_id, 'Диалог завершен. Чтобы начать новый, используйте команду /next,И оцените своего собеседника',
                               reply_markup=rate_keyaboard)
        await bot.send_message(partner_id, 'Диалог завершен. Чтобы начать новый, используйте команду /next,И оцените своего собеседника',
                               reply_markup=rate_keyaboard)
        print(f"Диалог между {user_id} и {partner_id} завершен.")
    else:
        await bot.send_message(user_id, 'Вы не связаны с кем-то, чтобы завершить диалог.', reply_markup=base_keyboard)


class RateState(StatesGroup):
    rate = State()


@dp.message_handler(commands='Rate')
async def rate(message: types.Message):
    await message.answer('На сколько вы хотите оценить собеседника, от 1 до 10')
    await RateState.rate.set()

@dp.message_handler(state=RateState.rate)
async def rate_people(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        if user_id in chat_pairs:
            partner_id = chat_pairs[user_id]
            rating = int(message.text)

            if 1 <= rating <= 10:
                await state.update_data(rate=rating)
                cursor.execute('UPDATE ChatUSERS SET Rate = ? WHERE TELEGRAM_ID = ?', (rating, partner_id))
                cursor.connection.commit()

                await message.answer('Оценка сохранена. Диалог завершен.', reply_markup=base_keyboard)
            else:
                await message.answer('Пожалуйста, введите число от 1 до 10.')

            await state.finish()  
        else:
            await message.answer('Что-то пошло не так. Ваш партнер не найден.', reply_markup=base_keyboard)
    except ValueError:
        await message

@dp.message_handler(text='Назад')
async def back(message:types.Message):
    await message.answer('Меню',reply_markup=base_keyboard)

@dp.message_handler(text='Рейтинг')
async def reiting(message: types.Message):
    rating = cursor.execute('SELECT Rate FROM ChatUSERS WHERE TELEGRAM_ID=?;', (message.from_user.id,)).fetchone()
    await message.reply(f"Ваш рейтинг: {rating[0] if rating else 'не оценен'}")

executor.start_polling(dp, skip_updates=True)
