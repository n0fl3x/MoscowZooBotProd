from aiogram import types

from commands.static_commands import (
    START_COMMAND,
    HELP_COMMAND,
    CONTACTS_COMMAND,
)


async def random_message_filter(message: types.Message):
    if message.text != '/admin' and \
            message.text != '/stop' and \
            message.text != f'/{START_COMMAND}' and \
            message.text != f'/{HELP_COMMAND}' and \
            message.text != f'/{CONTACTS_COMMAND}':
        return True
