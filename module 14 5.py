import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from apikeyBot import api
from keyboards import *
import crud_functions
from crud_functions import *

logging.basicConfig(level=logging.INFO)
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Привет, {message.from_user.username}! Я бот помогающий твоему здоровью.',
                         reply_markup=start_kb)

'''
Создайте цепочку изменений состояний RegistrationState.
Функции цепочки состояний RegistrationState:

sing_up(message):
Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя (только латинский алфавит):".
После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
'''

@dp.message_handler(text=['Регистрация'])
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит):')
    await RegistrationState.username.set()

'''
set_username(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии username на message.text.
Далее выводится сообщение "Введите свой email:" и принимается новое состояние RegistrationState.email.
Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует, введите другое имя" и
запрашивать новое состояние для RegistrationState.username.
'''

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if not crud_functions.is_included(message.text):
        await state.update_data(username=message.text)
        await message.answer('Введите свой e-mail:')
        await RegistrationState.email.set()
    else:
        await message.answer('Пользователь с таким именем уже существует, пожалуйста, введите другое имя:')
        await RegistrationState.username.set()

'''
set_email(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
Далее выводить сообщение "Введите свой возраст:":
После ожидать ввода возраста в атрибут RegistrationState.age.
'''

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    if ('@' in message.text) and ('.' in message.text):
        await state.update_data(email=message.text)
        await message.answer('Введите свой возраст:')
        await RegistrationState.age.set()
    else:
        await message.answer('Неверный формат эл.почты, введите, пожалуйста, другой адрес:')
        await RegistrationState.email.set()

'''
set_age(message, state):
Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
Эта функция должна обновлять данные в состоянии RegistrationState.age на message.text.
Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users при помощи ранее написанной
crud-функции add_user.
'''


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    crud_functions.add_user(data['username'], data['email'], data['age'])
    await message.answer(f'Пользователь {data["username"]} зарегистрирован.')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message: types.Message):
    # Получаем свежие данные из базы
    products = get_all_products()

    for product in products:
        await message.answer(f'Название: {product[1]} | Описание: {product[2]} | Цена: {product[3]}')

        try:
            with open(f'{product[0]}.bmp', 'rb') as file:
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


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст (лет): ')
    await UserState.age.set()
    await call.answer  # для деактивации кнопки после нажатия




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

@dp.callback_query_handler(text="back_to_catalog")
async def back(call):
    await call.message.answer("Что вас интересует ?", reply_markup=start_kb)
    await call.answer()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
