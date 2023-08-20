from aiogram import types


async def start_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'go_feedback':
        return True


async def cancel_feedback_inline_btn_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'cancel_feedback':
        return True
