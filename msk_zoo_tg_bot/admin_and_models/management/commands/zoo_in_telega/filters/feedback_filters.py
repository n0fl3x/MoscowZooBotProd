from aiogram import types

from commands.admin_commands import START_ADMIN_COMMAND
from commands.feedback_commands import CANCEL_FEEDBACK_COMMAND, START_FEEDBACK_COMMAND

from commands.static_commands import (
    START_COMMAND,
    HELP_COMMAND,
    CONTACTS_COMMAND,
)


async def start_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == START_FEEDBACK_COMMAND:
        return True


async def cancel_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == CANCEL_FEEDBACK_COMMAND:
        return True
