import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from admin_and_models.management.commands.zoo_in_telega.logic.quiz_output import questions, answers

from admin_and_models.management.commands.zoo_in_telega.bot_settings import bot
from admin_and_models.management.commands.zoo_in_telega.commands.quiz_commands import START_QUIZ_COMMAND, CANCEL_COMMAND
from admin_and_models.management.commands.zoo_in_telega.filters.result_filters import get_totem_animal
from admin_and_models.management.commands.zoo_in_telega.database.zoo_bot_db_config import (
    check_user_db_record,
    db_start,
    get_all_animals_stats,
)

from admin_and_models.management.commands.zoo_in_telega.filters.quiz_handlers_filters import (
    cancel_inline_btn_filter,
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

from admin_and_models.management.commands.zoo_in_telega.texts.warnings_text import (
    NOT_NONE_STATE_CANCEL_COMMAND_TEXT,
    NONE_STATE_CANCEL_COMMAND_TEXT,
    ALREADY_ANSWERED,
    ALREADY_FINISHED,
)

from admin_and_models.management.commands.zoo_in_telega.texts.questions_text import (
    START_QUIZ_TEXT,
    END_MESSAGE,
)

from admin_and_models.management.commands.zoo_in_telega.keyboards.quiz_kb import (
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


async def cancel_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel, введённой вручную. Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to cancel empty state.')
        await message.answer(text=NONE_STATE_CANCEL_COMMAND_TEXT)
        return

    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} cancelled '
                 f'quiz at {current_state} state by /cancel command.')
    await state.reset_state()
    await message.answer(text=NOT_NONE_STATE_CANCEL_COMMAND_TEXT)


async def cancel_inline_button(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel, вызванная через инлайн-кнопку. Останавливает текущий опрос."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} tried to cancel empty state.')
        await callback.answer()
        await callback.message.answer(text=NONE_STATE_CANCEL_COMMAND_TEXT)
        return

    logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} cancelled '
                 f'quiz at {current_state} state by cancel inline button.')
    await state.reset_state()
    await callback.answer()
    await callback.message.answer(text=NOT_NONE_STATE_CANCEL_COMMAND_TEXT)


async def animal_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды запуска опроса."""

    current_state = await state.get_state()

    if current_state is None:
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} started new quiz.')
    else:
        await message.answer(text='Вы начали опрос заново.')
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} restarted quiz.')

    await db_start()
    await message.answer(text=START_QUIZ_TEXT)
    await message.answer(
        text=questions[0],
        reply_markup=inline_keyboard_1
    )
    await get_all_animals_stats()
    await CurrentQuestion.question_1.set()


async def process_question_1(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    logging.info(f' {datetime.now()}: callback_query = {callback_query}')
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[0][0]}'
            or callback_query.data == f'{answers[0][1]}'
            or callback_query.data == f'{answers[0][2]}'
            or callback_query.data == f'{answers[0][3]}'):

        if cur_state == 'CurrentQuestion:question_1':
            await bot.answer_callback_query(callback_query.id)
            # await db_start()
            async with state.proxy() as data:
                data['user_id'] = callback_query.from_user.id
                data['1st_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 1st question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[1],
                reply_markup=inline_keyboard_2,
            )

        elif cur_state != 'CurrentQuestion:question_1' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 1st question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 1st question again in already finished quiz.')

    else:
        await process_question_2(callback_query=callback_query, state=state)


async def process_question_2(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[1][0]}'
            or callback_query.data == f'{answers[1][1]}'
            or callback_query.data == f'{answers[1][2]}'
            or callback_query.data == f'{answers[1][3]}'):

        if cur_state == 'CurrentQuestion:question_2':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['2nd_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 2nd question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[2],
                reply_markup=inline_keyboard_3,
            )

        elif cur_state != 'CurrentQuestion:question_2' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 2nd question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 2nd question again in already finished quiz.')

    else:
        await process_question_3(callback_query=callback_query, state=state)


async def process_question_3(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[2][0]}'
            or callback_query.data == f'{answers[2][1]}'
            or callback_query.data == f'{answers[2][2]}'
            or callback_query.data == f'{answers[2][3]}'):

        if cur_state == 'CurrentQuestion:question_3':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['3rd_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 3rd question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[3],
                reply_markup=inline_keyboard_4,
            )

        elif cur_state != 'CurrentQuestion:question_3' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 3rd question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 3rd question again in already finished quiz.')

    else:
        await process_question_4(callback_query=callback_query, state=state)


async def process_question_4(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[3][0]}'
            or callback_query.data == f'{answers[3][1]}'
            or callback_query.data == f'{answers[3][2]}'
            or callback_query.data == f'{answers[3][3]}'):

        if cur_state == 'CurrentQuestion:question_4':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['4th_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 4th question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[4],
                reply_markup=inline_keyboard_5,
            )

        elif cur_state != 'CurrentQuestion:question_4' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 4th question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 4th question again in already finished quiz.')

    else:
        await process_question_5(callback_query=callback_query, state=state)


async def process_question_5(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[4][0]}'
            or callback_query.data == f'{answers[4][1]}'
            or callback_query.data == f'{answers[4][2]}'):

        if cur_state == 'CurrentQuestion:question_5':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['5th_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 5th question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[5],
                reply_markup=inline_keyboard_6,
            )

        elif cur_state != 'CurrentQuestion:question_5' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 5th question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 5th question again in already finished quiz.')

    else:
        await process_question_6(callback_query=callback_query, state=state)


async def process_question_6(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[5][0]}'
            or callback_query.data == f'{answers[5][1]}'
            or callback_query.data == f'{answers[5][2]}'):

        if cur_state == 'CurrentQuestion:question_6':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['6th_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 6th question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[6],
                reply_markup=inline_keyboard_7,
            )

        elif cur_state != 'CurrentQuestion:question_6' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 6th question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 6th question again in already finished quiz.')

    else:
        await process_question_7(callback_query=callback_query, state=state)


async def process_question_7(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[6][0]}'
            or callback_query.data == f'{answers[6][1]}'
            or callback_query.data == f'{answers[6][2]}'
            or callback_query.data == f'{answers[6][3]}'):

        if cur_state == 'CurrentQuestion:question_7':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['7th_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 7th question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[7],
                reply_markup=inline_keyboard_8,
            )

        elif cur_state != 'CurrentQuestion:question_7' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 7th question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 7th question again in already finished quiz.')

    else:
        await process_question_8(callback_query=callback_query, state=state)


async def process_question_8(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[7][0]}'
            or callback_query.data == f'{answers[7][1]}'
            or callback_query.data == f'{answers[7][2]}'
            or callback_query.data == f'{answers[7][3]}'):

        if cur_state == 'CurrentQuestion:question_8':
            await bot.answer_callback_query(callback_query.id)
            async with state.proxy() as data:
                data['8th_question'] = callback_query.data
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=callback_query.data,
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                         f'({callback_query.data}) the 8th question.')
            await CurrentQuestion.next()
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=questions[8],
                reply_markup=inline_keyboard_9,
            )

        elif cur_state != 'CurrentQuestion:question_8' and cur_state is not None:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_ANSWERED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 8th question again in current quiz.')

        else:
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text=f'{ALREADY_FINISHED}',
            )
            logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                         f'answer ({callback_query.data}) the 8th question again in already finished quiz.')

    else:
        await process_question_9(callback_query=callback_query, state=state)


async def process_question_9(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if (callback_query.data == f'{answers[8][0]}'
        or callback_query.data == f'{answers[8][1]}'
        or callback_query.data == f'{answers[8][2]}'
        or callback_query.data == f'{answers[8][3]}')\
            and cur_state == 'CurrentQuestion:question_9':
        await bot.answer_callback_query(callback_query.id)
        async with state.proxy() as data:
            data['9th_question'] = callback_query.data
            proxy_dict = data.as_dict()
            result = await get_totem_animal(proxy_dict=proxy_dict)
        # TODO: разбить функцию записи на несколько для ускорения процесса
        await check_user_db_record(state=state)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=callback_query.data,
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} answered '
                     f'({callback_query.data}) the 9th question.')
        await state.finish()
        await bot.send_message(
            chat_id=result.get('chat_id'),
            text='Вау! Да ты ' + result.get('animal') + '!',
        )
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=END_MESSAGE,
        )

    else:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=f'{ALREADY_FINISHED}',
        )
        logging.info(f' {datetime.now()} : User with ID {callback_query.from_user.id} tried to '
                     f'answer ({callback_query.data}) the 9th question again in already finished quiz.')


# ---------------------
# Handlers registration
def register_quiz_handlers(disp: Dispatcher):
    disp.register_message_handler(
        cancel_command,
        commands=[f'{CANCEL_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        cancel_inline_button,
        cancel_inline_btn_filter,
        state='*',
    )
    disp.register_message_handler(
        animal_command,
        commands=[f'{START_QUIZ_COMMAND}'],
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
