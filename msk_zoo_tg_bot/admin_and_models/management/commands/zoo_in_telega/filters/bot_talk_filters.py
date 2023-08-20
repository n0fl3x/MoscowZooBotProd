from aiogram import types


async def dont_want_quiz_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'dont_want_quiz':
        return True


async def check_user_result_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'check_result_before_quiz':
        return True


async def show_result_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'show_me_result' or \
            callback_query.data == 'see_previous_result':
        return True


async def after_result_menu_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'whats_next' or \
            callback_query.data == 'welp' or \
            callback_query.data == 'thank_you':
        return True


async def picture_to_save_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'save_picture':
        return True


async def care_program_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'care_program':
        return True


async def care_program_contacts_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'care_program_contacts':
        return True


async def thats_enough_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'thats_enough':
        return True


async def see_ya_filter(callback_query: types.CallbackQuery):
    if callback_query.data == 'likewise':
        return True
