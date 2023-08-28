import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from filters.random_messages_filter import random_message_filter
from handlers.admin_panel_handlers import admin_delete_spam_handler


# ------------------------
# Anti users' spam handler
async def random_message_handler(message: types.Message, state: FSMContext) -> None:
    """Функция для удаления рандомных сообщений от пользователя."""

    cur_state = await state.get_state()

    if cur_state == 'Feedback:feedback':
        return

    elif cur_state == 'AdminAuthorization:TRUE':
        await admin_delete_spam_handler(message=message)

    else:
        await message.delete()
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {message.from_user.id} and username = '
                     f'{message.from_user.username} tried to send random message '
                     f'with {message.content_type} type while in {cur_state} state.')


# ---------------------
# Handlers registration
def register_rand_msg_handler(disp: Dispatcher) -> None:
    disp.register_message_handler(
        random_message_handler,
        random_message_filter,
        content_types=types.ContentTypes.ANY,
        state='*',
    )
