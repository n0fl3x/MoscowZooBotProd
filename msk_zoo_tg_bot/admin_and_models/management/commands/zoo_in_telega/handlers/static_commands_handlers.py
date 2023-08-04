# TODO: добавить хендлеры, которые будут обрабатывать нестандартные для бота сообщения (видео, картинки и т.д.)


import logging

from datetime import datetime
from aiogram import types, Dispatcher

from admin_and_models.management.commands.zoo_in_telega.keyboards.about_kb import about_inline_keyboard
from admin_and_models.management.commands.zoo_in_telega.keyboards.contacts_kb import zoo_contacts_inline_keyboard

from admin_and_models.management.commands.zoo_in_telega.commands.static_commands import (
    START_COMMAND,
    HELP_COMMAND,
    ABOUT_COMMAND,
    CONTACTS_COMMAND,
    CREATORS_COMMAND,
)

from admin_and_models.management.commands.zoo_in_telega.texts.static_commands_text import (
    START_COMMAND_TEXT,
    HELP_COMMAND_TEXT,
    CONTACTS_COMMAND_TEXT,
    CREATORS_COMMAND_TEXT,
)


# ---------------
# Static commands
async def start_command(message: types.Message) -> None:
    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{START_COMMAND} command.')
    await message.answer_photo(
        photo=open('images/start-logo.jpg', 'br'),
        caption=START_COMMAND_TEXT,
    )


async def help_command(message: types.Message) -> None:
    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{HELP_COMMAND} command.')
    await message.answer(text=HELP_COMMAND_TEXT)


async def about_command(message: types.Message) -> None:
    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{ABOUT_COMMAND} command.')
    await message.answer_photo(
        photo=open('images/about-logo.jpg', 'br'),
        reply_markup=about_inline_keyboard,
    )


async def contacts_command(message: types.Message) -> None:
    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{CONTACTS_COMMAND} command.')
    await message.answer(
        text=CONTACTS_COMMAND_TEXT,
        reply_markup=zoo_contacts_inline_keyboard,
    )


async def creators_command(message: types.Message) -> None:
    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{CREATORS_COMMAND} command.')
    await message.answer_photo(
        photo=open('images/creators-logo.png', 'br'),
        caption=CREATORS_COMMAND_TEXT,
    )


# ---------------------
# Handlers registration
def register_static_command_handlers(disp: Dispatcher):
    disp.register_message_handler(
        start_command,
        commands=[f'{START_COMMAND}'],
        state='*',
    )
    disp.register_message_handler(
        help_command,
        commands=[f'{HELP_COMMAND}'],
        state='*',
    )
    disp.register_message_handler(
        about_command,
        commands=[f'{ABOUT_COMMAND}'],
        state='*',
    )
    disp.register_message_handler(
        contacts_command,
        commands=[f'{CONTACTS_COMMAND}'],
        state='*',
    )
    disp.register_message_handler(
        creators_command,
        commands=[f'{CREATORS_COMMAND}'],
        state='*',
    )
