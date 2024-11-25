from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *

initiate_db()
products = get_all_products()

api = '8047870216:AAFDztSsKbcXwXuAZwFq3wqgBjjchzLs6B8'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Регистрация'), KeyboardButton(text='Рассчитать')],
        [KeyboardButton(text='Информация'), KeyboardButton(text='Купить')]
    ],resize_keyboard=True)


start_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
start_kb.add(inline_button1, inline_button2)

products_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=f'{products[0][1]}', callback_data='product_buying'), InlineKeyboardButton(text=f'{products[1][1]}', callback_data='product_buying')],
        [InlineKeyboardButton(text=f'{products[2][1]}', callback_data='product_buying'), InlineKeyboardButton(text=f'{products[3][1]}', callback_data='product_buying')]
    ], resize_keyboard=True)

class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000


@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)

#
#   ------РЕГИСТРАЦИЯ--------
#
@dp.message_handler(text=['Регистрация'])
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

@dp.message_handler(state = RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer('Пользователь существует, введите другое имя:')
        await RegistrationState.username.set()
    else:
        await state.update_data(username = message.text)
        await message.answer('Введите свой email:')
        await RegistrationState.email.set()

@dp.message_handler(state = RegistrationState.email)
async def set_email(message, state):
    if if_email_exists(message.text):
        await message.answer('Пользователь с таким email существует, введите другой email:')
        await RegistrationState.email.set()
    else:
        await state.update_data(email = message.text)
        await message.answer('Введите свой возраст:')
        await RegistrationState.age.set()

@dp.message_handler(state = RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    users_data = await state.get_data()
    add_user(users_data["username"], users_data["email"], users_data["age"])
    await message.answer('Регистрация прошла успешно!', reply_markup=kb)
    await state.finish()

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=start_kb)
@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    #products = get_all_products()
    for product in products:
        try:
            with open(f'pics/pic{product[0]}.jpg', 'rb') as image:
                await message.answer_photo(image, f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')
        except FileNotFoundError:
                await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')

    await message.answer('Выберите продукт для покупки:', reply_markup=products_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()
@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('10 * вес(кг) + 6.25 * рост(см) - 5 * возраст + 5')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_height(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост в см:')
    await UserState.height.set()

@dp.message_handler(state = UserState.height)
async def set_weight(message, state):
    await state.update_data(height = message.text)
    await message.answer('Введите свой вес в кг:')
    await UserState.weight.set()


@dp.message_handler(state = UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight = message.text)
    users_data = await state.get_data()
    calories = 10 * float(users_data["weight"]) + 6.25 * float(users_data["height"]) - 5 * int(users_data["age"]) + 5
    await message.answer(f'Ваша норма калорий: {calories}')
    await state.finish()
@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)