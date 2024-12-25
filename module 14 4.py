import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
from apikeyBot import api
from keyboards import *
from crud_functions import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.',
                         reply_markup=start_kb)





@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    # Получаем свежие данные из базы
    products = get_all_products()

    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')

        try:
            with open(f'{product[0]}.jpg', 'rb') as file:
                await message.answer_photo(file)
        except FileNotFoundError:
            await message.answer('Изображение для этого продукта не найдено.')

    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выбери опцию:', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()
    await call.answer


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    f = 'Формула Миффлина-Сан Жеора:\n' \
        'для мужчин: 10 х вес + 6.25 x рост – 5 х возраст + 5\n' \
        'для женщин: 10 x вес + 6.25 x рост – 5 x возраст – 161'
    await call.message.answer(f)
    await call.answer

@dp.message_handler(text='Информация')
async def info(message):
    await message.answer('Я бот, рассчитывающий норму калорий')


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост, пожалуйста')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес, пожалуйста')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = state.get_data
    try:
        calories_man = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        calories_wom = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161
        await message.answer(f'Норма (муж.): {calories_man} ккал')
        await message.answer(f'Норма (жен.): {calories_wom} ккал')
    except:
        await message.answer("Не могу конвертировать ваши значения в числа")
        return
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start , чтобы начать общение.')
    print(f'Получено: {message.text}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
