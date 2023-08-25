import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from logic.quiz_result_logic import get_totem_animal
from keyboards.talk_kb import inline_keyboard_show_me_result
from text_data.quiz_q_and_a import questions
from states.quiz_states import CurrentQuestion
from text_data.timosha_messages import I_KNOW_WHO_YOU_ARE

from database.quiz_result_db import (
    check_user_result,
    delete_old_result,
    insert_new_result,
)

from text_data.quiz_messages_text import (
    QUIZ_ALREADY_ANSWERED_TEXT,
    QUIZ_RESTART_TEXT,
    FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT,
    QUIT_ADMIN_TO_START_QUIZ_TEXT,
    QUIZ_CANCEL_FEEDBACK_STATE_TEXT,
    DIDNT_QUIZ, ADMIN_MODE_NOT_QUIZ,
    FEEDBACK_STATE_NOT_QUIZ,
    GO_ON_QUIZ,
)

from filters.quiz_filters import (
    question_filter_1,
    question_filter_2,
    question_filter_3,
    question_filter_4,
    question_filter_5,
    question_filter_6,
    question_filter_7,
    question_filter_8,
    question_filter_9,
    start_quiz_inline_btn_filter, continue_quiz_filter,
)

from keyboards.quiz_kb import (
    inline_keyboard_1,
    inline_keyboard_2,
    inline_keyboard_3,
    inline_keyboard_4,
    inline_keyboard_5,
    inline_keyboard_6,
    inline_keyboard_7,
    inline_keyboard_8,
    inline_keyboard_9,
)


# -------------
# Quiz handlers
async def start_quiz_inline_button(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to start new quiz while in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    else:
        if not cur_state:
            logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                         f'{callback.from_user.username} started new quiz from {cur_state} state.')

        elif cur_state == 'Feedback:feedback':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT,
            )
            await state.reset_state()
            logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                         f'{callback.from_user.username} cancelled {cur_state} state and started new quiz.')

        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=QUIZ_RESTART_TEXT,
            )
            await state.reset_state()
            logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                         f'{callback.from_user.username} cancelled {cur_state} state and restarted quiz.')

        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[0],
            reply_markup=inline_keyboard_1,
        )
        await CurrentQuestion.question_1.set()


async def process_question_1(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 1st quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_1':
        async with state.proxy() as data:
            data['user_id'] = callback.from_user.id
            data['username'] = callback.from_user.username
            data['1st_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[1],
            reply_markup=inline_keyboard_2,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 1st question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 1st quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 1st quiz question in {cur_state} state.')


async def process_question_2(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 2nd quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_2':
        async with state.proxy() as data:
            data['2nd_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[2],
            reply_markup=inline_keyboard_3,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 2nd question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 2nd quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 2nd quiz question in {cur_state} state.')


async def process_question_3(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 3rd quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_3':
        async with state.proxy() as data:
            data['3rd_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[3],
            reply_markup=inline_keyboard_4,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 3rd question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 3rd quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 3rd quiz question in {cur_state} state.')


async def process_question_4(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 4th quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_4':
        async with state.proxy() as data:
            data['4th_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[4],
            reply_markup=inline_keyboard_5,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 4th question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 4th quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 4th quiz question in {cur_state} state.')


async def process_question_5(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 5th quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_5':
        async with state.proxy() as data:
            data['5th_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[5],
            reply_markup=inline_keyboard_6,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 5th question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 5th quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 5th quiz question in {cur_state} state.')


async def process_question_6(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 6th quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_6':
        async with state.proxy() as data:
            data['6th_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[6],
            reply_markup=inline_keyboard_7,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 6th question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 6th quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 6th quiz question in {cur_state} state.')


async def process_question_7(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 7th quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_7':
        async with state.proxy() as data:
            data['7th_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[7],
            reply_markup=inline_keyboard_8,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 7th question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 7th quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 7th quiz question in {cur_state} state.')


async def process_question_8(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 8th quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_8':
        async with state.proxy() as data:
            data['8th_question'] = callback.data
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=questions[8],
            reply_markup=inline_keyboard_9,
        )
        await CurrentQuestion.next()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 8th question.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 8th quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 8th quiz question in {cur_state} state.')


async def process_question_9(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция обработки последнего вопроса викторины + обработка результата."""

    await bot.answer_callback_query(callback_query_id=callback.id)
    logging.info(f' {datetime.now()}: callback_query = {callback}')
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=QUIT_ADMIN_TO_START_QUIZ_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 9th quiz question in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'CurrentQuestion:question_9':
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} answered ({callback.data}) the 9th question.')
        async with state.proxy() as data:
            data['9th_question'] = callback.data
            proxy_dict = data.as_dict()
            totem_animal = await get_totem_animal(proxy_dict=proxy_dict)
        got_db_result = await check_user_result(user_id=data.get('user_id'))

        if got_db_result:
            await delete_old_result(state=state)

        await insert_new_result(
            state=state,
            animal=totem_animal,
        )

        await state.finish()
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=I_KNOW_WHO_YOU_ARE,
            reply_markup=inline_keyboard_show_me_result,
        )

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_CANCEL_FEEDBACK_STATE_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 9th quiz question in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to answer 9th quiz question in {cur_state} state.')


async def continue_quiz_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    cur_state = await state.get_state()

    if not cur_state:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=DIDNT_QUIZ,
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to continue quiz in {cur_state} state.')

    elif cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=ADMIN_MODE_NOT_QUIZ,
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to continue quiz in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=FEEDBACK_STATE_NOT_QUIZ,
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to continue quiz in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=GO_ON_QUIZ,
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} and username = '
                     f'{callback.from_user.username} continued quiz in {cur_state} state.')

        if cur_state == 'CurrentQuestion:question_1':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[0],
                reply_markup=inline_keyboard_1,
            )

        if cur_state == 'CurrentQuestion:question_2':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[1],
                reply_markup=inline_keyboard_2,
            )

        if cur_state == 'CurrentQuestion:question_3':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[2],
                reply_markup=inline_keyboard_3,
            )

        if cur_state == 'CurrentQuestion:question_4':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[3],
                reply_markup=inline_keyboard_4,
            )

        if cur_state == 'CurrentQuestion:question_5':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[4],
                reply_markup=inline_keyboard_5,
            )

        if cur_state == 'CurrentQuestion:question_6':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[5],
                reply_markup=inline_keyboard_6,
            )

        if cur_state == 'CurrentQuestion:question_7':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[6],
                reply_markup=inline_keyboard_7,
            )

        if cur_state == 'CurrentQuestion:question_8':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[7],
                reply_markup=inline_keyboard_8,
            )

        if cur_state == 'CurrentQuestion:question_9':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=questions[8],
                reply_markup=inline_keyboard_9,
            )


# ---------------------
# Handlers registration
def register_quiz_handlers(disp: Dispatcher) -> None:
    disp.register_callback_query_handler(
        start_quiz_inline_button,
        start_quiz_inline_btn_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_1,
        question_filter_1,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_2,
        question_filter_2,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_3,
        question_filter_3,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_4,
        question_filter_4,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_5,
        question_filter_5,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_6,
        question_filter_6,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_7,
        question_filter_7,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_8,
        question_filter_8,
        state='*',
    )
    disp.register_callback_query_handler(
        process_question_9,
        question_filter_9,
        state='*',
    )
    disp.register_callback_query_handler(
        continue_quiz_handler,
        continue_quiz_filter,
        state='*',
    )
