import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from handlers.quiz_handlers import start_quiz_inline_button
from database.quiz_result_db import get_user_last_result
from commands.static_commands import START_COMMAND
from text_data.static_commands_text import START_COMMAND_TEXT

from filters.quiz_filters import (
    dont_want_quiz_filter,
    user_got_result_filter,
    see_previous_result,
)

from keyboards.start_kb import (
    inline_keyboard_start_msg,
    inline_keyboard_ok_lets_go_quiz,
    inline_keyboard_see_quiz_result_or_try_again,
)


# ---------------
# Just phrases
async def start_handler(message: types.Message, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if not cur_state:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo='AgACAgIAAxkBAAIHK2TXc2_ihStPGkGR8gt5zQ9yC6C6AAJ4zDEb0bm4Skjj5YsTOmyPAQADAgADcwADMAQ',
            caption=START_COMMAND_TEXT,
            reply_markup=inline_keyboard_start_msg,
        )
        logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{START_COMMAND} command.')

    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text='Сейчас не нулевой стейт (стартовый хэндлер)',
        )


async def dont_want_quiz_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    cur_state = await state.get_state()

    if not cur_state:
        await bot.answer_callback_query(callback_query_id=callback.id)
        await bot.send_photo(
            chat_id=callback.from_user.id,
            photo='AgACAgIAAxkBAAIHK2TXc2_ihStPGkGR8gt5zQ9yC6C6AAJ4zDEb0bm4Skjj5YsTOmyPAQADAgADcwADMAQ',
            caption='Не зли. Проходи.',
            reply_markup=inline_keyboard_ok_lets_go_quiz,
        )
        logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} refused to '
                     f'start new quiz by inline button.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Сейчас не нулевой стейт (не хочу опрос хэндлер)',
        )


async def user_got_result_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text='Эта штука проверяет БД на результат.',
    )
    user_id = callback.from_user.id
    got_result = await get_user_last_result(user_id=user_id)

    if got_result:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Ты уже проходил тест.\n'
                 'Хочешь снова увидеть прошлый результат?',
            reply_markup=inline_keyboard_see_quiz_result_or_try_again,
        )
    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Ты ещё не проходил тест.',
        )
        await start_quiz_inline_button(
            callback_query=callback,
            state=state,
        )


async def see_my_previous_result_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    user_id = callback.from_user.id
    animal = (await get_user_last_result(user_id))[4]
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f'Твой предыдущий результат опроса - {animal}.',
    )


# ---------------------
# Handlers registration
def register_static_command_handlers(disp: Dispatcher):
    disp.register_message_handler(
        start_handler,
        commands=[f'{START_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        dont_want_quiz_handler,
        dont_want_quiz_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        user_got_result_handler,
        user_got_result_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        see_my_previous_result_handler,
        see_previous_result,
        state='*',
    )
