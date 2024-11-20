from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = '8047870216:AAFDztSsKbcXwXuAZwFq3wqgBjjchzLs6B8'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button1, button2, button3)

start_kb = InlineKeyboardMarkup(resize_keyboard=True)
inline_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
inline_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
start_kb.add(inline_button1, inline_button2)

products_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data='product_buying'), InlineKeyboardButton(text='Product2', callback_data='product_buying')],
        [InlineKeyboardButton(text='Product3', callback_data='product_buying'), InlineKeyboardButton(text='Product4', callback_data='product_buying')]
    ], resize_keyboard=True)

class UserState(StatesGroup):
    age = State()
    height = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start_message(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text=['Рассчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=start_kb)

@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    for i in range(1,5):
        with open(f'pics/pic{i}.jpg', 'rb') as image:
            await message.answer_photo(image, f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
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