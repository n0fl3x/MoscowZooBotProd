from aiogram import types

from commands.feedback_commands import CANCEL_FEEDBACK_COMMAND
from commands.quiz_commands import CANCEL_QUIZ_COMMAND
from text_data.quiz_q_and_a import answers


async def user_got_result_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'start_quiz' or \
            callback_query.data == 'ok_start_quiz':
        return callback_query


async def dont_want_quiz_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'dont_want_quiz':
        return callback_query


async def see_previous_result(callback_query: types.CallbackQuery):
    if callback_query.data == 'see_previous_result':
        return callback_query


async def cancel_quiz_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_QUIZ_COMMAND}':
        return callback_query


async def cancel_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_FEEDBACK_COMMAND}':
        return callback_query


# -----------------
# Questions filters
async def question_filter_1(callback_query: types.CallbackQuery):
    if callback_query.data == answers[0][0] \
            or callback_query.data == answers[0][1] \
            or callback_query.data == answers[0][2] \
            or callback_query.data == answers[0][3]:
        return callback_query


async def question_filter_2(callback_query: types.CallbackQuery):
    if callback_query.data == answers[1][0] \
            or callback_query.data == answers[1][1] \
            or callback_query.data == answers[1][2] \
            or callback_query.data == answers[1][3]:
        return callback_query


async def question_filter_3(callback_query: types.CallbackQuery):
    if callback_query.data == answers[2][0] \
            or callback_query.data == answers[2][1] \
            or callback_query.data == answers[2][2] \
            or callback_query.data == answers[2][3]:
        return callback_query


async def question_filter_4(callback_query: types.CallbackQuery):
    if callback_query.data == answers[3][0] \
            or callback_query.data == answers[3][1] \
            or callback_query.data == answers[3][2] \
            or callback_query.data == answers[3][3]:
        return callback_query


async def question_filter_5(callback_query: types.CallbackQuery):
    if callback_query.data == answers[4][0] \
            or callback_query.data == answers[4][1] \
            or callback_query.data == answers[4][2]:
        return callback_query


async def question_filter_6(callback_query: types.CallbackQuery):
    if callback_query.data == answers[5][0] \
            or callback_query.data == answers[5][1] \
            or callback_query.data == answers[5][2]:
        return callback_query


async def question_filter_7(callback_query: types.CallbackQuery):
    if callback_query.data == answers[6][0] \
            or callback_query.data == answers[6][1] \
            or callback_query.data == answers[6][2] \
            or callback_query.data == answers[6][3]:
        return callback_query


async def question_filter_8(callback_query: types.CallbackQuery):
    if callback_query.data == answers[7][0] \
            or callback_query.data == answers[7][1] \
            or callback_query.data == answers[7][2] \
            or callback_query.data == answers[7][3]:
        return callback_query


async def question_filter_9(callback_query: types.CallbackQuery):
    if callback_query.data == answers[8][0] \
            or callback_query.data == answers[8][1] \
            or callback_query.data == answers[8][2] \
            or callback_query.data == answers[8][3]:
        return callback_query
