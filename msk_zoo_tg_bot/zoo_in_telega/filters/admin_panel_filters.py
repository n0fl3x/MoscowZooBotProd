from aiogram import types

from commands.admin_commands import HELP_ADMIN_COMMAND


async def admin_help_filter(callback: types.CallbackQuery):
    if callback.data == HELP_ADMIN_COMMAND:
        return True


async def admin_delete_spam_filter(message: types.Message):
    if message.content_type != 'photo' and \
            message.content_type != 'document':
        return True
