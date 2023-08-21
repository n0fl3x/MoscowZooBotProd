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
    QUIZ_ALREADY_FINISHED_TEXT,
    QUIZ_RESTART_TEXT,
    FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT,
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
    start_quiz_inline_btn_filter,
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
async def start_quiz_inline_button(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    cur_state = await state.get_state()

    if cur_state is None:
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} started new quiz.')
    elif cur_state == 'Feedback:feedback':
        await callback_query.answer(text=FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT)
        await state.reset_state()
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} cancelled feedback state '
                     f'and started new quiz.')
    else:
        await callback_query.answer(text=QUIZ_RESTART_TEXT)
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} restarted quiz.')

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=questions[0],
        reply_markup=inline_keyboard_1
    )
    await CurrentQuestion.question_1.set()


async def process_question_1(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_1':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['user_id'] = callback_query.from_user.id
            data['username'] = callback_query.from_user.username
            data['1st_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 1st question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[1],
            reply_markup=inline_keyboard_2,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_1' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 1st question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 1st question again in already finished quiz.')


async def process_question_2(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_2':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['2nd_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 2nd question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[2],
            reply_markup=inline_keyboard_3,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_2' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 2nd question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 2nd question again in already finished quiz.')


async def process_question_3(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_3':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['3rd_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 3rd question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[3],
            reply_markup=inline_keyboard_4,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_3' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 3rd question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 3rd question again in already finished quiz.')


async def process_question_4(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_4':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['4th_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 4th question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[4],
            reply_markup=inline_keyboard_5,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_4' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 4th question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 4th question again in already finished quiz.')


async def process_question_5(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_5':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['5th_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 5th question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[5],
            reply_markup=inline_keyboard_6,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_5' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 5th question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 5th question again in already finished quiz.')


async def process_question_6(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_6':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['6th_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 6th question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[6],
            reply_markup=inline_keyboard_7,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_6' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 6th question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 6th question again in already finished quiz.')


async def process_question_7(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_7':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['7th_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 7th question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[7],
            reply_markup=inline_keyboard_8,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_7' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 7th question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 7th question again in already finished quiz.')


async def process_question_8(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_8':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        async with state.proxy() as data:
            data['8th_question'] = callback_query.data

        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 8th question.')
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=questions[8],
            reply_markup=inline_keyboard_9,
        )
        await CurrentQuestion.next()
    elif cur_state != 'CurrentQuestion:question_8' and cur_state is not None:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_ANSWERED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 8th question again in current quiz.')
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 8th question again in already finished quiz.')


async def process_question_9(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """Функция обработки последнего вопроса викторины + обработка результата."""

    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if cur_state == 'CurrentQuestion:question_9':
        await bot.answer_callback_query(callback_query_id=callback_query.id)
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 9th question.')
        async with state.proxy() as data:
            data['9th_question'] = callback_query.data
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
            chat_id=callback_query.from_user.id,
            text=I_KNOW_WHO_YOU_ARE,
            reply_markup=inline_keyboard_show_me_result,
        )
    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{QUIZ_ALREADY_FINISHED_TEXT}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 9th question again in already finished quiz.')


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
