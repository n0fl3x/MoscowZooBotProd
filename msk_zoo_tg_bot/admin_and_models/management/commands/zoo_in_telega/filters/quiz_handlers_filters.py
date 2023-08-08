from aiogram import types

from commands.feedback_commands import CANCEL_FEEDBACK_COMMAND
from commands.quiz_commands import CANCEL_QUIZ_COMMAND


"""
Хоть эти фильтры в данный момент не несут никакой смысловой нагрузки,
они были вынесены в отдельный файл для их возможной будущей кастомизации.
"""


async def cancel_quiz_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_QUIZ_COMMAND}':
        return callback_query


async def cancel_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_FEEDBACK_COMMAND}':
        return callback_query


# -----------------
# Questions filters
async def question_filter_1(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_2(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_3(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_4(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_5(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_6(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_7(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_8(callback_query: types.CallbackQuery):
    return callback_query


async def question_filter_9(callback_query: types.CallbackQuery):
    return callback_query
