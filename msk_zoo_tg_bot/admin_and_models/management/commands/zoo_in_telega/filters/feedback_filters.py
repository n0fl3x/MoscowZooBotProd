from aiogram import types

from commands.feedback_commands import (
    CANCEL_FEEDBACK_COMMAND,
    START_FEEDBACK_COMMAND,
    CANCEL_QUIZ_TO_GO_FEEDBACK_COMMAND,
)


async def start_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == START_FEEDBACK_COMMAND or \
            callback_query.data == CANCEL_QUIZ_TO_GO_FEEDBACK_COMMAND:
        return True


async def cancel_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == CANCEL_FEEDBACK_COMMAND:
        return True
