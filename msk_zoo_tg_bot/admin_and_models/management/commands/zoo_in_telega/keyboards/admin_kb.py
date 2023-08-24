import aiogram.types

from commands.admin_commands import HELP_ADMIN_COMMAND, STOP_ADMIN_COMMAND

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


help_btn = InlineKeyboardButton(
    text=HELP_ADMIN_COMMAND,
    callback_data=HELP_ADMIN_COMMAND,
)

admin_keyboard = InlineKeyboardMarkup().add(help_btn)

stop_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(f'/{STOP_ADMIN_COMMAND}'))

remove_kb = aiogram.types.ReplyKeyboardRemove()
