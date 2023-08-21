import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from text_data.admin_panel_text import *
from states.admin_panel_states import AdminAuthorization

from keyboards.admin_kb import (
    admin_keyboard,
    stop_keyboard,
    remove_kb,
)


ADMINS = [
    'equestrriann',
    'Nevzorov_R_O',
    'camomail0_0',
    'Kotia_Ro',
    'AYSharapova',
    'Swaggareus',
]


# -----------------------
# Administration handlers
async def admin_panel_start_handler(message: types.Message):
    if message.from_user.username in ADMINS:
        await AdminAuthorization.TRUE.set()
        await message.answer(
            text=f"<b>Привет, {message.from_user.username}!</b>\n" + HELLO_ADMIN,
            parse_mode="HTML",
            reply_markup=admin_keyboard,
        )
        logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                     f'{message.from_user.username} successfully activated admin panel.')
    else:
        await message.answer(text=NOT_ADMIN)
        logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                     f'{message.from_user.username} unsuccessfully tried to activate admin panel.')


async def admin_help_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await callback.message.answer(
        text=HELP,
        parse_mode="HTML",
        reply_markup=stop_keyboard,
    )
    logging.info(f' {datetime.now()} : User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} used help button of admin panel.')


async def admin_scan_photo_handler(msg: types.Message):
    document_id = msg.photo[0].file_id
    file_info = await bot.get_file(document_id)

    await bot.send_message(
        chat_id=msg.chat.id,
        text='<b>ID этой картинки:</b>',
        parse_mode="HTML",
        reply_markup=stop_keyboard,
    )
    await bot.send_photo(
        chat_id=msg.chat.id,
        photo=document_id,
    )
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"{file_info.file_id}",
    )
    await msg.delete()
    logging.info(f' {datetime.now()} : User with ID = {msg.from_user.id} and username = '
                 f'{msg.from_user.username} scanned photo for ID.')


async def admin_scan_document_handler(msg: types.Message):
    file_info = await bot.get_file(file_id=msg.document.file_id)

    await bot.send_message(
        chat_id=msg.chat.id,
        text='<b>ID этого файла:</b>',
        parse_mode="HTML",
        reply_markup=stop_keyboard,
    )
    await bot.send_document(
        chat_id=msg.chat.id,
        document=msg.document.file_id,
    )
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"{file_info.file_id}",
    )
    await msg.delete()
    logging.info(f' {datetime.now()} : User with ID = {msg.from_user.id} and username = '
                 f'{msg.from_user.username} scanned document for ID.')


async def admin_panel_stop_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text='Вы вышли из панели администратора!',
        reply_markup=remove_kb,
    )
    logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} quit admin panel.')


async def admin_delete_spam_handler(message: types.Message):
    await message.delete()
    logging.info(f' {datetime.now()} : User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} send useless message with {message.content_type} type '
                 f'in admin panel.')


# ---------------------
# Handlers registration
def register_admin_panel_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(
        admin_panel_start_handler,
        commands=['admin'],
        state='*',
    )
    disp.register_callback_query_handler(
        admin_help_handler,
        lambda callback: callback.data == "help",
        state=AdminAuthorization.TRUE,
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
        commands=['stop'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        admin_delete_spam_handler,
        content_types=[
            'text',
            'photo',
            'video',
            'sticker',
            'document',
        ],
        state=AdminAuthorization.TRUE,
    )
