import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from filters.admin_panel_filters import admin_delete_spam_filter, admin_help_filter
from text_data.admin_panel_text import *
from states.admin_panel_states import AdminAuthorization
from database.admin_db import tg_admin_auth

from keyboards.admin_kb import (
    admin_keyboard,
    stop_keyboard,
    remove_kb,
)

from commands.admin_commands import (
    START_ADMIN_COMMAND,
    STOP_ADMIN_COMMAND,
)


# -----------------------
# Administration handlers
async def admin_panel_start_handler(message: types.Message, state: FSMContext) -> None:
    """Активация режима администратора."""

    username = message.from_user.username
    user_id = message.from_user.id

    is_admin = await tg_admin_auth(
        tg_username=username,
        user_id=user_id,
    )

    if is_admin:
        cur_state = await state.get_state()

        if not cur_state:
            await AdminAuthorization.TRUE.set()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"<b>Привет, {username if username else 'Admin'}!</b>\n" + HELLO_ADMIN,
                parse_mode="HTML",
                reply_markup=admin_keyboard,
            )
            logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                         f'{username} successfully activated admin panel '
                         f'from {cur_state} state.')

        elif cur_state == 'AdminAuthorization:TRUE':
            await bot.send_message(
                chat_id=message.from_user.id,
                text=ADMIN_STATE_ALREADY_TEXT,
            )
            logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                         f'{username} tried to activate admin panel '
                         f'while already in {cur_state} state.')

        elif cur_state == 'Feedback:feedback':
            await state.reset_state()
            await AdminAuthorization.TRUE.set()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=CANCELLED_FEEDBACK_ACTIVATED_ADMIN_STATE_TEXT,
            )
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"<b>Привет, {username if username else 'Admin'}!</b>\n" + HELLO_ADMIN,
                parse_mode="HTML",
                reply_markup=admin_keyboard,
            )
            logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                         f'{username} activated admin panel '
                         f'and cancelled {cur_state} state.')

        else:
            await state.reset_state()
            await AdminAuthorization.TRUE.set()
            await bot.send_message(
                chat_id=message.from_user.id,
                text=CANCELLED_QUIZ_ACTIVATED_ADMIN_STATE_TEXT,
            )
            await bot.send_message(
                chat_id=message.from_user.id,
                text=f"<b>Привет, {username if username else 'Admin'}!</b>\n" + HELLO_ADMIN,
                parse_mode="HTML",
                reply_markup=admin_keyboard,
            )
            logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                         f'{username} activated admin panel '
                         f'and cancelled {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=NOT_ADMIN,
        )
        logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                     f'{username} unsuccessfully tried to activate admin panel.')


async def admin_help_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    """Вызов помощи для панели администратора."""

    await bot.answer_callback_query(callback_query_id=callback.id)
    cur_state = await state.get_state()

    if cur_state == 'AdminAuthorization:TRUE':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=HELP_ADMIN,
            parse_mode="HTML",
            reply_markup=stop_keyboard,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} used help button of admin panel in {cur_state} state.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=NOT_IN_ADMIN_STATE,
        )
        logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to use help button of admin panel '
                     f'while in {cur_state} state.')


async def admin_scan_photo_handler(message: types.Message) -> None:
    """Вывод ID изображений."""

    document_id = message.photo[0].file_id
    file_info = await bot.get_file(document_id)

    await bot.send_message(
        chat_id=message.chat.id,
        text='<b>ID этой картинки:</b>',
        parse_mode="HTML",
        reply_markup=stop_keyboard,
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=document_id,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{file_info.file_id}",
    )
    await message.delete()
    logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} scanned photo for ID.')


async def admin_scan_document_handler(message: types.Message) -> None:
    """Вывод ID документа."""

    file_info = await bot.get_file(file_id=message.document.file_id)

    await bot.send_message(
        chat_id=message.chat.id,
        text='<b>ID этого файла:</b>',
        parse_mode="HTML",
        reply_markup=stop_keyboard,
    )
    await bot.send_document(
        chat_id=message.chat.id,
        document=message.document.file_id,
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"{file_info.file_id}",
    )
    await message.delete()
    logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} scanned document for ID.')


async def admin_panel_stop_handler(message: types.Message, state: FSMContext) -> None:
    """Выход из режима администратора."""

    await state.finish()
    await bot.send_message(
        chat_id=message.from_user.id,
        text=QUIT_ADMIN_PANEL_TEXT,
        reply_markup=remove_kb,
    )
    logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} quit admin panel.')


async def admin_delete_spam_handler(message: types.Message) -> None:
    """Анти-спам в режиме администратора."""

    await message.delete()
    logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} send useless message with {message.content_type} type '
                 f'in admin panel.')


# ---------------------
# Handlers registration
def register_admin_panel_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(
        admin_panel_start_handler,
        commands=[f'{START_ADMIN_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        admin_help_handler,
        admin_help_filter,
        state='*',
    )
    disp.register_message_handler(
        admin_scan_photo_handler,
        content_types=['photo'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        admin_scan_document_handler,
        content_types=['document'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        admin_panel_stop_handler,
        commands=[f'{STOP_ADMIN_COMMAND}'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        admin_delete_spam_handler,
        admin_delete_spam_filter,
        state=AdminAuthorization.TRUE,
    )
