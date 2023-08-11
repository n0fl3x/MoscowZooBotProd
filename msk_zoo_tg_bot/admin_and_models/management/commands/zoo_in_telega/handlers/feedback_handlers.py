import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from bot_settings import bot
from keyboards.feedback_kb import inline_keyboard_cancel_feedback
from database.quiz_result_db import check_user_result

from database.feedback_db import (
    check_user_feedback,
    delete_old_feedback,
    insert_new_feedback,
)

from commands.feedback_commands import (
    START_FEEDBACK_COMMAND,
    CANCEL_FEEDBACK_COMMAND,
)

from text_data.feedback_messages_text import (
    START_FEEDBACK_STATE,
    BUSY_FOR_FEEDBACK,
    FEEDBACK_STATE_ALREADY,
    FEEDBACK_CANCEL_NONE_STATE_TEXT,
    FEEDBACK_STATE_CANCEL_COMMAND_TEXT,
    FEEDBACK_CANCEL_QUIZ_STATE_TEXT,
    DONT_UNDERSTAND_FEEDBACK,
    THANK_YOU_FOR_FEEDBACK,
    CANT_FEEDBACK_WITHOUT_QUIZ,
)

from filters.handlers_filters import cancel_feedback_inline_btn_filter


# --------------
# States classes
class Feedback(StatesGroup):
    """Класс для фиксации состояния ожидания отзыва от пользователя."""

    feedback = State()


# -----------------
# Feedback handlers
async def feedback_command(message: types.Message, state: FSMContext) -> None:
    """Функция активации состояния ожидания отзыва."""

    async with state.proxy() as data:
        data['user_id'] = message.from_user.id

    got_result = await check_user_result(state=state)

    if got_result:
        cur_state = await state.get_state()

        if cur_state is None:
            await message.answer(
                text=START_FEEDBACK_STATE,
                reply_markup=inline_keyboard_cancel_feedback,
            )
            await Feedback.feedback.set()
            logging.info(f' {datetime.now()} : User with ID {message.from_user.id} trying to crete a new feedback.')

        elif cur_state == 'Feedback:feedback':
            await message.answer(
                text=FEEDBACK_STATE_ALREADY,
                reply_markup=inline_keyboard_cancel_feedback,
            )
            logging.info(f' {datetime.now()} : User with ID {message.from_user.id} trying to crete a new feedback '
                         f'while already in a feedback state.')

        else:
            await message.answer(text=BUSY_FOR_FEEDBACK)
            logging.info(f' {datetime.now()} : User with ID {message.from_user.id} trying to crete a new feedback '
                         f'without finishing/cancelling current quiz.')

    else:
        await message.answer(text=CANT_FEEDBACK_WITHOUT_QUIZ)
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} trying to crete a new feedback '
                     f'without at least once completed quiz.')


async def cancel_feedback_command(message: types.Message, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel_feedback, введённой вручную.
    Отменяет состояние ожидания отзыва."""

    current_state = await state.get_state()

    if current_state is None:
        await message.answer(text=FEEDBACK_CANCEL_NONE_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to cancel '
                     f'feedback at empty state by command.')

    elif current_state == 'Feedback:feedback':
        await message.answer(text=FEEDBACK_STATE_CANCEL_COMMAND_TEXT)
        await state.reset_state()
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} canceled '
                     f'feedback state by command.')

    else:
        await message.answer(text=FEEDBACK_CANCEL_QUIZ_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to cancel '
                     f'feedback at {current_state} state by command.')


async def cancel_feedback_inline_button(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция-обработчик команды /cancel_feedback, вызванная через инлайн-кнопку.
    Отменяет состояние ожидания отзыва."""

    current_state = await state.get_state()
    await callback.answer()

    if current_state is None:
        await callback.message.answer(text=FEEDBACK_CANCEL_NONE_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} tried to cancel '
                     f'feedback at empty state by inline button.')

    elif current_state == 'Feedback:feedback':
        await callback.message.answer(text=FEEDBACK_STATE_CANCEL_COMMAND_TEXT)
        await state.reset_state()
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} canceled '
                     f'feedback state by inline button.')

    else:
        await callback.message.answer(text=FEEDBACK_CANCEL_QUIZ_STATE_TEXT)
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} tried to cancel '
                     f'feedback at {current_state} state by inline button.')


async def process_feedback(message: types.Message, state: FSMContext) -> None:
    """Функция обработки отзыва."""

    if message.text:
        user_id = message.from_user.id
        username = message.from_user.username
        text = message.text
        fb = await check_user_feedback(user_id=user_id)

        if fb:
            await delete_old_feedback(user_id=user_id)

        await insert_new_feedback(
            user_id=user_id,
            username=username,
            text=text,
        )
        await state.finish()
        await bot.send_message(
            chat_id=message.chat.id,
            text=THANK_YOU_FOR_FEEDBACK,
        )
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} added new feedback:\n'
                     f'{message.text}')

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=DONT_UNDERSTAND_FEEDBACK,
        )
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} trying to crete invalid feedback '
                     f'with {message.content_type} type.')


# ---------------------
# Handlers registration
def register_feedback_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(
        feedback_command,
        commands=[f'{START_FEEDBACK_COMMAND}'],
        state='*',
    )
    disp.register_message_handler(
        process_feedback,
        lambda message: message.text != f'/{CANCEL_FEEDBACK_COMMAND}',
        content_types=types.ContentTypes.ANY,
        state=Feedback.feedback,
    )
    disp.register_message_handler(
        cancel_feedback_command,
        commands=[f'{CANCEL_FEEDBACK_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        cancel_feedback_inline_button,
        cancel_feedback_inline_btn_filter,
        state='*',
    )
