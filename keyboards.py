from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup




start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Рассчитать"),
            KeyboardButton(text="Информация"),
            KeyboardButton(text="Купить")
        ]
    ], resize_keyboard=True
)
kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')],
        [InlineKeyboardButton('Формулы расчёта', callback_data='formulas')],
    ]
)
catalog_kb =  InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Product1', callback_data="product_buying")],
        [InlineKeyboardButton('Product2', callback_data="product_buying")],
        [InlineKeyboardButton('Product3', callback_data="product_buying")],
        [InlineKeyboardButton('Product4', callback_data="product_buying")]
    ]
)