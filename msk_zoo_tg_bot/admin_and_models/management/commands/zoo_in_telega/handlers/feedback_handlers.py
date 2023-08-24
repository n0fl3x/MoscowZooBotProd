import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from handlers.talk_handlers import after_result_menu_handler
from keyboards.feedback_kb import inline_keyboard_cancel_feedback
from database.quiz_result_db import check_user_result
from keyboards.talk_kb import inline_keyboard_thank_you
from text_data.timosha_messages import TYPE_YOUR_FEEDBACK, THANKS_FOR_FEEDBACK
from states.feedback_states import Feedback

from filters.feedback_filters import (
    cancel_feedback_inline_btn_filter,
    start_feedback_inline_btn_filter,
    process_feedback_filter,
)

from database.feedback_db import (
    check_user_feedback,
    delete_old_feedback,
    insert_new_feedback,
)

from text_data.feedback_messages_text import (
    FEEDBACK_STATE_ALREADY,
    FEEDBACK_CANCEL_NONE_STATE_TEXT,
    FEEDBACK_STATE_CANCEL_COMMAND_TEXT,
    FEEDBACK_CANCEL_QUIZ_STATE_TEXT,
    DONT_UNDERSTAND_FEEDBACK,
    CANT_FEEDBACK_WITHOUT_QUIZ,
    QUIT_ADMIN_TO_LEAVE_FEEDBACK_TEXT,
    ADMIN_STATE_NOT_FEEDBACK,
)


# -----------------
# Feedback handlers
async def start_feedback_inline_btn_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция активации состояния ожидания отзыва."""

    await bot.answer_callback_query(callback_query_id=callback.id)
    cur_state = await state.get_state()
    got_result = await check_user_result(user_id=callback.from_user.id)

    if got_result:

        if not cur_state:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=TYPE_YOUR_FEEDBACK,
                reply_markup=inline_keyboard_cancel_feedback,
            )
            await Feedback.feedback.set()
            logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} trying to crete a new feedback at {cur_state} state.')

        elif cur_state == 'Feedback:feedback':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=FEEDBACK_STATE_ALREADY,
                reply_markup=inline_keyboard_cancel_feedback,
            )
            logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} trying to crete a new feedback '
                         f'while in {cur_state} state.')

        elif cur_state == 'AdminAuthorization:TRUE':
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=QUIT_ADMIN_TO_LEAVE_FEEDBACK_TEXT,
            )
            logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} trying to crete a new feedback '
                         f'while in {cur_state} state. '
                         f'Need to deactivate admin panel.')

        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=CANT_FEEDBACK_WITHOUT_QUIZ,
            )
            logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} trying to crete a new feedback '
                         f'without finishing/cancelling current quiz.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=CANT_FEEDBACK_WITHOUT_QUIZ,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} trying to crete a new feedback at {cur_state} state '
                     f'without at least once completed quiz.')


async def cancel_feedback_inline_button_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Функция-обработчик отмены состояния отзыва, вызванная через инлайн-кнопку."""

    cur_state = await state.get_state()
    await bot.answer_callback_query(callback_query_id=callback.id)

    if not cur_state:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=FEEDBACK_CANCEL_NONE_STATE_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to cancel '
                     f'feedback at {cur_state} state by inline button.')

    elif cur_state == 'Feedback:feedback':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=FEEDBACK_STATE_CANCEL_COMMAND_TEXT,
        )
        await state.reset_state()
        await after_result_menu_handler(callback=callback)
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} canceled '
                     f'{cur_state} state by inline button.')

    elif cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=ADMIN_STATE_NOT_FEEDBACK,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to cancel feedback '
                     f'while in {cur_state} state. '
                     f'Need to deactivate admin panel.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=FEEDBACK_CANCEL_QUIZ_STATE_TEXT,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to cancel '
                     f'feedback at {cur_state} state by inline button.')


async def process_feedback_handler(message: types.Message, state: FSMContext) -> None:
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
            text=THANKS_FOR_FEEDBACK,
            reply_markup=inline_keyboard_thank_you,
        )
        logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                     f'{message.from_user.username} added new feedback:\n'
                     f'{message.text}')

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=DONT_UNDERSTAND_FEEDBACK,
            # reply_markup=inline_keyboard_cancel_feedback,
        )
        logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                     f'{message.from_user.username} trying to crete invalid feedback '
                     f'with {message.content_type} type.')


# ---------------------
# Handlers registration
def register_feedback_handlers(disp: Dispatcher) -> None:
    disp.register_callback_query_handler(
        start_feedback_inline_btn_handler,
        start_feedback_inline_btn_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        cancel_feedback_inline_button_handler,
        cancel_feedback_inline_btn_filter,
        state='*',
    )
    disp.register_message_handler(
        process_feedback_handler,
        process_feedback_filter,
        content_types=types.ContentTypes.ANY,
        state=Feedback.feedback,
    )
