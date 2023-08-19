import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from filters.all_handlers_filters import random_message_filter


# --------------
# For users spam
async def random_message_handler(message: types.Message, state: FSMContext):
    """Функция для удаления рандомных сообщений от пользователя."""

    cur_state = await state.get_state()

    if cur_state == 'Feedback.feedback':
        return
    else:
        await message.delete()
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} tried to send random message '
                     f'with {message.content_type} type.')


# ---------------------
# Handlers registration
def register_rand_msg_handler(disp: Dispatcher):
    disp.register_message_handler(
        random_message_handler,
        random_message_filter,
        content_types=types.ContentTypes.ANY,
        state='*',
    )
