import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from database.quiz_result_db import check_user_result, get_db_animal
from commands.static_commands import START_COMMAND
from handlers.quiz_handlers import start_quiz_inline_button

from filters.bot_talk_filters import (
    dont_want_quiz_filter,
    check_user_result_filter,
    show_result_filter,
    after_result_menu_filter,
    picture_to_save_filter,
    care_program_filter,
    care_program_contacts_filter,
    thats_enough_filter,
    see_ya_filter,
)

from keyboards.talk_kb import (
    inline_keyboard_start_msg,
    inline_keyboard_ok_lets_go_quiz,
    inline_keyboard_see_quiz_result_or_try_again,
    inline_keyboard_whats_next,
    inline_keyboard_after_result,
    inline_keyboard_thank_you,
    inline_keyboard_welp,
    inline_keyboard_care_program,
    inline_keyboard_likewise,
    inline_keyboard_thank_you_pic_save,
)

from text_data.timosha_messages import (
    HELLO_MSG,
    DO_NOT_UPSET,
    U_HAVE_RESULT,
    WHAT_DO_U_WANT,
    CLUB_FRIENDS_INFO,
    THANKS_FOR_TALK,
    SEE_YOU,
    SAVE_RESULT_TEXT,
    CONTACTS,
)


# -----------------
# Bot talk handlers
async def start_handler(message: types.Message) -> None:
    await bot.send_photo(
        chat_id=message.chat.id,
        photo='AgACAgIAAxkBAAIKx2TfpTBifqDEusvXAAHkWGScwn-rOAAC0tIxGzd1AAFLG7N9QTErez8BAAMCAANzAAMwBA',
        caption=HELLO_MSG,
        parse_mode='HTML',
        reply_markup=inline_keyboard_start_msg,
    )
    logging.info(f' {datetime.now()} : User with ID {message.from_user.id} used /{START_COMMAND} command.')


async def dont_want_quiz_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo='AgACAgIAAxkBAAIKymTfpXzUAWq2DwiUcRBpKSdPHmVhAALfyzEb6Cn4Sv4XUhOfzfCsAQADAgADcwADMAQ',
        caption=DO_NOT_UPSET,
        reply_markup=inline_keyboard_ok_lets_go_quiz,
    )
    logging.info(f' {datetime.now()} : User with ID {callback.from_user.id} refused to '
                 f'start new quiz by inline button.')


async def check_user_result_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    user_id = callback.from_user.id
    got_result = await check_user_result(user_id=user_id)

    if got_result:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=U_HAVE_RESULT,
            reply_markup=inline_keyboard_see_quiz_result_or_try_again,
        )
    else:
        await start_quiz_inline_button(
            callback_query=callback,
            state=state,
        )


async def show_result_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)

    result = await check_user_result(user_id=callback.from_user.id)
    animal_name = result[4]
    db_animal = await get_db_animal(animal=animal_name)

    picture_id = db_animal[4]
    result_text = db_animal[6]
    nickname = db_animal[2]
    animal_url = db_animal[7]
    gender = db_animal[3]

    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo=picture_id,
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        parse_mode='HTML',
        text=result_text,
    )
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=f"""В Московском зоопарке представителем этого вида является {nickname}. """
             f"""О {'ней' if gender else 'нём'} и {'её' if gender else 'его'} сородичах можно почитать """
             f"""<b><a href='{animal_url}'>тут</a></b>.""",
        parse_mode='HTML',
        reply_markup=inline_keyboard_whats_next,
    )


async def after_result_menu_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=WHAT_DO_U_WANT,
        reply_markup=inline_keyboard_after_result,
    )


async def picture_to_save_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    totem = await check_user_result(user_id=callback.from_user.id)

    if totem:
        animal_name = totem[4]
        db_animal = await get_db_animal(animal=animal_name)
        if db_animal:
            picture = db_animal[5]
            await bot.send_document(
                chat_id=callback.from_user.id,
                document=picture,
                caption=SAVE_RESULT_TEXT,
                reply_markup=inline_keyboard_thank_you_pic_save,
            )
        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text='Видимо такого животного уже/ещё нету в БД',
                reply_markup=inline_keyboard_welp,
            )
    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text='Похоже ты всё-таки ещё ни разу не проходил опрос',
            reply_markup=inline_keyboard_welp,
        )


async def care_program_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo='AgACAgIAAxkBAAIKzWTfpaGdaY8MlzBsdHk9Re-OWpU4AALgyzEb6Cn4StQIfF0AARrflwEAAwIAA3MAAzAE',
        caption=CLUB_FRIENDS_INFO,
        reply_markup=inline_keyboard_care_program,
    )


async def care_program_contacts_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=CONTACTS,
        parse_mode='HTML',
        reply_markup=inline_keyboard_thank_you,
    )


async def thats_enough_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=THANKS_FOR_TALK,
        reply_markup=inline_keyboard_likewise,
    )


async def see_ya_handler(callback: types.CallbackQuery):
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=SEE_YOU,
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
        check_user_result_handler,
        check_user_result_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        show_result_handler,
        show_result_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        after_result_menu_handler,
        after_result_menu_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        picture_to_save_handler,
        picture_to_save_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        care_program_handler,
        care_program_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        care_program_contacts_handler,
        care_program_contacts_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        thats_enough_handler,
        thats_enough_filter,
        state='*',
    )
    disp.register_callback_query_handler(
        see_ya_handler,
        see_ya_filter,
        state='*',
    )
