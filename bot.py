from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.utils import executor
from config import bot, dp
from media.images import *
from media.texts import *

async def on_startup(_):
    print('Бот успешно запущен')

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    # клавиатура
    btn = KeyboardButton('Манул... звучит знакомо...')
    start_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn)

    # сообщения Тимофея
    await bot.send_photo(message.chat.id, text=hello_text)
    await message.answer(hello_text, parse_mode="HTML", reply_markup=start_menu)
    await message.delete()

@dp.message_handler()
async def reply_handler(message: types.Message):
    try:
        match message.text:
            case 'Манул... звучит знакомо...':
                # клавиатура
                btn1 = KeyboardButton('ДА 🦥')
                btn2 = KeyboardButton('А я не хочу ☹️')
                START_QUIZ = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btn1).add(btn2)

                # сообщения от Тимофея
                await bot.send_video(message.chat.id, video=manul_paws)
                await message.answer(manul_text)
                await message.answer(quiz_text, reply_markup=START_QUIZ)

            case 'ДА 🦥':
                await message.answer('Я еще не сделал викторину, потому что у меня лапки😢')

            case 'А я не хочу ☹️':
                # клавиатура
                btn3 = KeyboardButton('Ладно, давай викторину😊')
                OKAY_START = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(btn3)

                # сообщения от Тимофея
                await bot.send_photo(message.chat.id, angry_timosha)
                await message.answer(angry_text, reply_markup=OKAY_START)

            case 'Ладно, давай викторину😊':
                await message.answer('Я еще не сделал викторину, потому что у меня лапки😢')
    except Exception as e:
        await message.reply('Не удалось отправить видео в кружочке')
        print(f'[INFO] {e}')

# Получить id картинки
@dp.message_handler(content_types=['photo'])
async def scan_message(msg: types.Message):
    document_id = msg.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')
    await bot.send_message(msg.chat.id, text=f"file_id: {file_info.file_id}\n"
                                             f"file_path: {file_info.file_path}\n"
                                             f"file_size: {file_info.file_size}\n"
                                             f"file_unique_id: {file_info.file_unique_id}\n")

# Получить id видео
@dp.message_handler(content_types=['video'])
async def get_video_id(message: types.Message):
    video_id = message.video.file_id
    file_info = await bot.get_file(video_id)
    print(f'file_id: {file_info.file_id}')
    await bot.send_message(message.chat.id, text=f"file_id: {file_info.file_id}")

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
