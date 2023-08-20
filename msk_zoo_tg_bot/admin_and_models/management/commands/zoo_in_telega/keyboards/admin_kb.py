import aiogram.types

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


help_btn = InlineKeyboardButton(
    text='help',
    callback_data='help',
)

admin_keyboard = InlineKeyboardMarkup(row_width=1).add(help_btn)

stop_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/stop'))

remove_kb = aiogram.types.ReplyKeyboardRemove()
