import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_settings import bot
from filters.result_filters import get_totem_animal
from text_data.quiz_q_and_a import questions

from database.quiz_result_db import (
    check_user_result_after_quiz,
    delete_old_result,
    insert_new_result,
)

from commands.quiz_commands import (
    START_QUIZ_COMMAND,
    CANCEL_QUIZ_COMMAND,
)

from text_data.quiz_messages_text import (
    QUIZ_START_TEXT,
    QUIZ_COMPLETE_TEXT,
    QUIZ_STATE_CANCEL_COMMAND_TEXT,
    QUIZ_CANCEL_NONE_STATE_TEXT,
    QUIZ_ALREADY_ANSWERED_TEXT,
    QUIZ_ALREADY_FINISHED_TEXT,
    QUIZ_CANCEL_FEEDBACK_STATE_TEXT,
    QUIZ_RESTART_TEXT,
    FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT,
)

from filters.quiz_filters import (
    cancel_quiz_inline_btn_filter,
    question_filter_1,
    question_filter_2,
    question_filter_3,
    question_filter_4,
    question_filter_5,
    question_filter_6,
    question_filter_7,
    question_filter_8,
    question_filter_9,
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


# --------------
# States classes
class CurrentQuestion(StatesGroup):
    """Класс для фиксации состояний ожидания ответа на определённый по счёту вопрос."""

    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()


# -------------
# Quiz handlers
async def cancel_quiz_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды, введённой вручную.
    Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        await message.answer(text=QUIZ_CANCEL_NONE_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to cancel quiz '
                     f'at empty state by command.')

    elif current_state == 'Feedback:feedback':
        await message.answer(text=QUIZ_CANCEL_FEEDBACK_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to cancel '
                     f'quiz at {current_state} state by command.')

    else:
        await message.answer(text=QUIZ_STATE_CANCEL_COMMAND_TEXT)
        await state.reset_state()
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} cancelled '
                     f'quiz at {current_state} state by command.')


async def cancel_quiz_inline_button(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция-обработчик команды, вызванная через инлайн-кнопку.
    Останавливает текущий опрос."""

    current_state = await state.get_state()
    await callback.answer()

    if current_state is None:
        await callback.message.answer(text=QUIZ_CANCEL_NONE_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} tried to cancel quiz '
                     f'at empty state by inline button.')

    elif current_state == 'Feedback:feedback':
        await callback.message.answer(text=QUIZ_CANCEL_FEEDBACK_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} tried to cancel '
                     f'quiz at {current_state} state by inline button.')

    else:
        await callback.message.answer(text=QUIZ_STATE_CANCEL_COMMAND_TEXT)
        await state.reset_state()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} cancelled '
                     f'quiz at {current_state} state by inline button command.')


async def start_quiz_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды запуска опроса."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} started new quiz.')
    elif current_state == 'Feedback:feedback':
        await message.answer(text=FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT)
        await state.reset_state()
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} cancelled feedback stare '
                     f'and started new quiz.')
    else:
        await message.answer(text=QUIZ_RESTART_TEXT)
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} restarted quiz.')

    await message.answer(text=QUIZ_START_TEXT)
    await message.answer(
        text=questions[0],
        reply_markup=inline_keyboard_1
    )
    await CurrentQuestion.question_1.set()


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
        text=QUIZ_START_TEXT,
    )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
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
        async with state.proxy() as data:
            data['9th_question'] = callback_query.data
            proxy_dict = data.as_dict()
            result = await get_totem_animal(proxy_dict=proxy_dict)
        got_db_result = await check_user_result_after_quiz(state=state)

        if got_db_result:
            await delete_old_result(state=state)

        await insert_new_result(
            state=state,
            animal=result.get('animal'),
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 9th question.')
        await bot.send_message(
            chat_id=result.get('chat_id'),
            text='Вау! Да ты ' + result.get('animal') + '!',
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=QUIZ_COMPLETE_TEXT,
        )
        await state.finish()

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
    disp.register_message_handler(
        start_quiz_command,
        commands=[f'{START_QUIZ_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        start_quiz_inline_button,
        lambda callback: callback.data == 'go_quiz_again',
        state='*',
    )
    disp.register_message_handler(
        cancel_quiz_command,
        commands=[f'{CANCEL_QUIZ_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        cancel_quiz_inline_button,
        cancel_quiz_inline_btn_filter,
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
