from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from text_data.admin_panel_text import *


class AdminAuthorization(StatesGroup):
    TRUE = State()


ADMINS = [
    'equestrriann',
    'Nevzorov_R_O',
]


async def admin_panel(message: types.Message):
    if message.from_user.username in ADMINS:
        await AdminAuthorization.TRUE.set()
        await message.answer(
            text=f"<b>Привет, {message.from_user.username}!</b>\n" + HELLO_ADMIN,
            parse_mode="HTML",
            reply_markup=admin_keyboard),
    else:
        await message.answer(text=NOT_ADMIN)


async def admin_help(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await callback.message.answer(
        text=HELP,
        parse_mode="HTML",
        reply_markup=stop_keyboard
    )


async def scan_photo(msg: types.Message):
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


async def scan_document(msg: types.Message):
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


async def stop_handler(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        text='Вы вышли из панели администратора!',
        reply_markup=remove_kb,
    )


async def delete_spam(message: types.Message):
    await message.delete()


# ---------------------
# Handlers registration
def register_admin_panel_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(
        admin_panel,
        commands=['admin'],
        state='*',
    )
    disp.register_callback_query_handler(
        admin_help,
        lambda callback: callback.data == "help",
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        scan_photo,
        content_types=['photo'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        scan_document,
        content_types=['document'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        stop_handler,
        commands=['stop'],
        state=AdminAuthorization.TRUE,
    )
    disp.register_message_handler(
        delete_spam,
        content_types=['text', 'photo', 'video', 'sticker', 'document'],
    )
