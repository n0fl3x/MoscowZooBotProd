from aiogram import types


async def random_message_filter(message: types.Message):
    if message.text != '/admin' and \
            message.text != '/help' and \
            message.text != '/stop' and \
            message.text != '/start':
        return True
