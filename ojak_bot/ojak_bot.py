from aiogram import Bot, Dispatcher, types, executor
from logging import basicConfig , INFO
from ojak_token import token
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
basicConfig(level=INFO)

database = sqlite3.connect('ojak.db')
cursor = database.cursor()




cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ojak_User(
    Id INTEGER PRIMARY KEY,
    Telegram_Id INTEGER,
    Username TEXT,
    Firstname TEXT,
    Contact TEXT,
    Location TEXT
    );
    ''')
cursor.connection.commit()





start_buttons = [
    types.KeyboardButton('О нас'),
    types.KeyboardButton('Меню'),
    types.KeyboardButton('Адрес'),
]
start_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*start_buttons)



@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer(f'Здравствуйте, {message.from_user.full_name}', reply_markup=start_keyboard)







@dp.message_handler(text='О нас')
async def about_us(message: types.Message):
    await message.reply('Ocak Kebap'
'Кафе Ожак Кебап на протяжении 18 лет радует своих гостей с изысканными турецкими блюдами в особенности своим кебабом.'
'Наше кафе отличается от многих кафе своими доступными ценами и быстрым сервисом.'
'В 2016 году по голосованию на сайте Horeca были удостоены "Лучшее кафе" на каждый день и мы стараемся оправдать доверие наших гостей.'
'Мы не добавляем консерванты, усилители вкуса, красители, ароматизаторы, растительные и животные жиры, вредные добавки с маркировкой «Е». У нас строгий контроль качества: наши филиалы придерживаются норм Кырпотребнадзор и санэпидемстанции. Мы используем только сертифицированную мясную и рыбную продукцию от крупных поставщиков.')

@dp.message_handler(text='Адрес')
async def adress(message: types.Message):
    await message.reply('Курманжан датка, 209 1-этаж')

shashlyki = [
    types.KeyboardButton('Вали кебаб'),
    types.KeyboardButton('Шефим кебаб'),
    types.KeyboardButton('Симит кебаб'),
    types.KeyboardButton('Форель на мангале целиком'),
    types.KeyboardButton('Адана с йогуртом'),
    types.KeyboardButton('3Киремите кофте'),
    types.KeyboardButton('Патлыжан кебаб'),
    types.KeyboardButton('Кашарлы кебаб'),
    types.KeyboardButton('Ассорти кебаб'),
    types.KeyboardButton('Крылышки на мангале'),
    types.KeyboardButton('Фыстыклы кебаб'),
    types.KeyboardButton('Чоп шиш баранина'),
    types.KeyboardButton('Пирзола'),
    types.KeyboardButton('Сач кавурма с мясом'),
    types.KeyboardButton('Сач кавурма с курицей'),
    types.KeyboardButton('Форель на мангале кусочками'),
    types.KeyboardButton('Семга с ризотто'),
    types.KeyboardButton('Донер кебаб'),
    types.KeyboardButton('Донер сарма'),
    types.KeyboardButton('Шашлык из баранины'),
    types.KeyboardButton('Кашарлы кофте'),
    types.KeyboardButton('Ызгара кофте'),
    types.KeyboardButton('Урфа'),
    types.KeyboardButton('Адана острый'),
    types.KeyboardButton('Адана кебаб'),
    types.KeyboardButton('Назад')
]
shashlyki_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*shashlyki)


order = [
    types.KeyboardButton('Заказать'),
    types.KeyboardButton('Назад в меню')
]
order_button = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*order)


@dp.message_handler(text='Меню')
async def menu(message: types.Message):
    await message.reply("Меню:",reply_markup=shashlyki_button)
@dp.message_handler(text='Шефим кебаб')
async def shefim_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163138.png','Шефим кебаб ,\n420с',reply_markup=order_button)

@dp.message_handler(text='Вали кебаб')
async def vali_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150910.png','Вали кебаб ,\n3200с',reply_markup=order_button)

@dp.message_handler(text='Симит кебаб')
async def simit_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163137.png','Cимит Кебаб,\n420 с',reply_markup=order_button)

@dp.message_handler(text='Форель на мангале целиком')
async def forel_on_mangal(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163137.png','Форель на мангале целиком,\n700 с',reply_markup=order_button)


@dp.message_handler(text='Адана с йогуртом')
async def adana_with_yougurt(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/48324.png','Адана с йогуртом,\n420 с',reply_markup=order_button)

@dp.message_handler(text='Киремите кофте')
async def kiremite_kofte(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163140.png','Киремите кофте,\n400 с',reply_markup=order_button)


@dp.message_handler(text='Патлыжан кебаб')
async def patyljan_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150928.png','Патлыжан кебаб,\n500 с',reply_markup=order_button)


@dp.message_handler(text='Кашарлы кебаб')
async def kasharly_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150929.png','Кашарлы кебаб,\n480 с',reply_markup=order_button)


@dp.message_handler(text='Ассорти кебаб')
async def assorti_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150931.png','Ассорти кебаб,\n700 с',reply_markup=order_button)


@dp.message_handler(text='Крылышки на мангале')
async def krylyshki_na_mangale(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150925.png','Крылышки на мангале,\n400c',reply_markup=order_button)


@dp.message_handler(text='Фыстыклы кебаб')
async def fystykly_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150932.png','Фыстыклы кебаб,\n460c',reply_markup=order_button)


@dp.message_handler(text='Чоп шиш баранина')
async def chop_shish_baranina(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150926.png','Чоп шиш баранина,\n400c',reply_markup=order_button)


@dp.message_handler(text='Пирзола')
async def pirzola(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150927.png','Пирзола,\n700c',reply_markup=order_button)


@dp.message_handler(text='Сач кавурма с мясом')
async def sach_kavurma_s_myasom(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163141.png','Сач кавурма с мясом,\n450c',reply_markup=order_button)


@dp.message_handler(text='Сач кавурма с курицей')
async def sach_kavurma_s_kuritsei(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163144.png','Сач кавурма с курицей,\n440c',reply_markup=order_button)


@dp.message_handler(text='Форель на мангале кусочками')
async def forel_on_mangal_with_pieces(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163145.png','Форель на мангале кусочками,\n1100c',reply_markup=order_button)


@dp.message_handler(text='Семга с ризотто')
async def semga_with_rissoto(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163146.png','Семга с ризотто,\n800c',reply_markup=order_button)


@dp.message_handler(text='Донер кебаб ')
async def doner_kebab_(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163147.png','Донер кебаб ,\n440c',reply_markup=order_button)


@dp.message_handler(text='Донер сарма')
async def doner_sarma(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/163148.png','Донер сарма,\n450c',reply_markup=order_button)


@dp.message_handler(text='Урфа')
async def urfa(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150936.png','Урфа,\n420c',reply_markup=order_button)


@dp.message_handler(text='Шашлык из баранины')
async def shashlyk_iz_govyadiny(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150933.png','Шашлык из баранины,\n450c',reply_markup=order_button)


@dp.message_handler(text='Кашарлы кофте')
async def kasharly_kofte(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150934.png','Кашарлы кофте,\n420c',reply_markup=order_button)


@dp.message_handler(text='Ызгара кофте')
async def yszgara_kofte(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150935.png','Ызгара кофте,\n400c',reply_markup=order_button)


@dp.message_handler(text='Адана острый')
async def adana_ostryi(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/150937.png','Адана острый,\n420c',reply_markup=order_button)

@dp.message_handler(text='Адана кебаб')
async def adana_kebab(message: types.Message):
    await message.answer_photo('https://nambafood.kg/dish_image/48323.png','Адана кебаб,\n420c',reply_markup=order_button)


@dp.message_handler(text='Назад')
async def nazad(message: types.Message):
    await start(message)

class OrderState(StatesGroup):
    name = State()
    contact = State()
    location = State()

@dp.message_handler(text='Заказать')
async def order(message: types.Message):
    await message.answer('Пожалуйста, введите ваше имя')
    await OrderState.name.set()

@dp.message_handler(state=OrderState.name)
async def get_contact(message:types.Message,state:FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Отлично теперь Введите Номер Телефона')
    await OrderState.contact.set()

@dp.message_handler(state=OrderState.contact)
async def get_location(message:types.Message, state:FSMContext):
    await state.update_data(contact=message.text)
    await message.answer('Прекрасно а теперь введите свой адрес')
    await OrderState.location.set()

@dp.message_handler(state=OrderState.location)
async def input_in_db(message:types.Message, state:FSMContext):
    await state.update_data(location=message.text)
    await message.answer('Вы успешно сделали заказ')
    result = await storage.get_data(user=message.from_user.id)
    print(result)
    cursor.execute('INSERT INTO Ojak_User VALUES (?,?,?,?,?,?);',
                   (None, message.from_user.id, message.from_user.username,
                    result['name'], result['contact'], result['location']))

    await state.finish()
    await message.answer('Пожалуйста Ожидайте,Мы Предлагаем Вам Изучить меню', reply_markup=start_keyboard)

@dp.message_handler(text='Назад в меню')
async def back_to_menu(message:types.Message):
    await menu(message)
executor.start_polling(dp, skip_updates=True)


