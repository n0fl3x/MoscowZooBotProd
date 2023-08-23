from aiogram import types

from commands.admin_commands import START_ADMIN_COMMAND, STOP_ADMIN_COMMAND

from commands.static_commands import (
    START_COMMAND,
    HELP_COMMAND,
    CONTACTS_COMMAND,
)


async def random_message_filter(message: types.Message):
    if message.text != f'/{START_ADMIN_COMMAND}' and \
            message.text != f'/{STOP_ADMIN_COMMAND}' and \
            message.text != f'/{START_COMMAND}' and \
            message.text != f'/{HELP_COMMAND}' and \
            message.text != f'/{CONTACTS_COMMAND}':
        return True
