import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


logging.basicConfig(level=logging.INFO)
api = '????????'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Расчитать'),
            KeyboardButton(text='Информация')
        ]
    ], resize_keyboard=True
)
kb1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ]
)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
@dp.message_handler(text='Привет')
async def all_massages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Расчитать')
async def main_menu(message):
    await message.answer('Выбери опцию:', reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=float(message.text))
    await message.answer('Введите рост в см.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(first1=float(message.text))
    await message.answer('Введите вес в кг.')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(first2=float(message.text))
    data = await state. get_data()
    bmi = (10 * data['first2']) + (6.25 * data['first1']) - (5 * data['first']) + 5
    await message.answer(f'Ваша норма калорий равена: {bmi} .')
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)