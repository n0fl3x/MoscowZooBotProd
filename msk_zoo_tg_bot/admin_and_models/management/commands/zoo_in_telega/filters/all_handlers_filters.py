from aiogram import types

from commands.feedback_commands import CANCEL_FEEDBACK_COMMAND
from commands.quiz_commands import CANCEL_QUIZ_COMMAND
from text_data.quiz_q_and_a import answers


async def random_message_filter(message: types.Message):
    if message.text != '/admin' and \
            message.text != '/help' and \
            message.text != '/stop' and \
            message.text != '/start':
        return True


async def user_got_result_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'check_result_before_quiz':
        return True


async def dont_want_quiz_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'dont_want_quiz':
        return True


async def after_result_menu_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'whats_next' or \
            callback_query.data == 'welp' or \
            callback_query.data == 'thank_you':
        return True


async def picture_to_save_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'save_picture':
        return True


async def show_result_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'show_me_result' or callback_query.data == 'see_previous_result':
        return True


async def care_program_contacts_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'care_program_contacts':
        return True


async def care_program_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'care_program':
        return True


# QUIZ FILTERS
async def start_quiz_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'go_quiz':
        return True


async def cancel_quiz_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_QUIZ_COMMAND}':
        return True


# FEEDBACK FILTERS
async def start_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'leave_feedback':
        return True


async def cancel_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == f'/{CANCEL_FEEDBACK_COMMAND}':
        return True


# -----------------
# Questions filters
async def question_filter_1(callback_query: types.CallbackQuery):
    if callback_query.data == answers[0][0] \
            or callback_query.data == answers[0][1] \
            or callback_query.data == answers[0][2] \
            or callback_query.data == answers[0][3]:
        return True


async def question_filter_2(callback_query: types.CallbackQuery):
    if callback_query.data == answers[1][0] \
            or callback_query.data == answers[1][1] \
            or callback_query.data == answers[1][2] \
            or callback_query.data == answers[1][3]:
        return True


async def question_filter_3(callback_query: types.CallbackQuery):
    if callback_query.data == answers[2][0] \
            or callback_query.data == answers[2][1] \
            or callback_query.data == answers[2][2] \
            or callback_query.data == answers[2][3]:
        return True


async def question_filter_4(callback_query: types.CallbackQuery):
    if callback_query.data == answers[3][0] \
            or callback_query.data == answers[3][1] \
            or callback_query.data == answers[3][2] \
            or callback_query.data == answers[3][3]:
        return True


async def question_filter_5(callback_query: types.CallbackQuery):
    if callback_query.data == answers[4][0] \
            or callback_query.data == answers[4][1] \
            or callback_query.data == answers[4][2]:
        return True


async def question_filter_6(callback_query: types.CallbackQuery):
    if callback_query.data == answers[5][0] \
            or callback_query.data == answers[5][1] \
            or callback_query.data == answers[5][2]:
        return True


async def question_filter_7(callback_query: types.CallbackQuery):
    if callback_query.data == answers[6][0] \
            or callback_query.data == answers[6][1] \
            or callback_query.data == answers[6][2] \
            or callback_query.data == answers[6][3]:
        return True


async def question_filter_8(callback_query: types.CallbackQuery):
    if callback_query.data == answers[7][0] \
            or callback_query.data == answers[7][1] \
            or callback_query.data == answers[7][2] \
            or callback_query.data == answers[7][3]:
        return True


async def question_filter_9(callback_query: types.CallbackQuery):
    if callback_query.data == answers[8][0] \
            or callback_query.data == answers[8][1] \
            or callback_query.data == answers[8][2] \
            or callback_query.data == answers[8][3]:
        return True
