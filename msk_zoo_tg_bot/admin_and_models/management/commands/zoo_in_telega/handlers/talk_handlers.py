import logging

from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_settings import bot
from database.quiz_result_db import check_user_result, get_db_animal
from handlers.quiz_handlers import start_quiz_inline_button
from text_data.quiz_messages_text import NEVER_QUIZ

from commands.static_commands import (
    START_COMMAND,
    HELP_COMMAND,
    CONTACTS_COMMAND,
)

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
    inline_keyboard_care_program,
    inline_keyboard_likewise,
    inline_keyboard_thank_you_pic_save,
    inline_keyboard_help_msg,
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
    USER_HELP,
    CONTACTS,
    SOMETHING_ELSE,
)

from text_data.bot_urls import MOSCOW_ZOO_ANIMALS


# -----------------
# Bot talk handlers
async def help_handler(message: types.Message) -> None:
    await bot.send_message(
        chat_id=message.chat.id,
        text=USER_HELP,
        reply_markup=inline_keyboard_help_msg,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} used bot help menu button.')


async def help_to_restart_bot_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await start_handler(message=callback.message)
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} restarted bot by help menu button.')


async def help_to_restart_quiz_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await start_quiz_inline_button(
        callback=callback,
        state=state,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} restarted quiz by help menu button.')


async def contacts_handler(message: types.Message) -> None:
    await bot.send_message(
        chat_id=message.chat.id,
        text=CONTACTS,
        reply_markup=inline_keyboard_thank_you,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {message.from_user.id} and username = '
                 f'{message.from_user.username} want to see contacts by help menu button.')


async def start_handler(message: types.Message) -> None:
    await bot.send_photo(
        chat_id=message.chat.id,
        photo='AgACAgIAAxkBAAIKx2TfpTBifqDEusvXAAHkWGScwn-rOAAC0tIxGzd1AAFLG7N9QTErez8BAAMCAANzAAMwBA',
        caption=HELLO_MSG,
        reply_markup=inline_keyboard_start_msg,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {message.chat.id} and username = '
                 f'{message.chat.username} started/restarted bot.')


async def dont_want_quiz_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo='AgACAgIAAxkBAAIKymTfpXzUAWq2DwiUcRBpKSdPHmVhAALfyzEb6Cn4Sv4XUhOfzfCsAQADAgADcwADMAQ',
        caption=DO_NOT_UPSET,
        reply_markup=inline_keyboard_ok_lets_go_quiz,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} refused to start new quiz by inline button.')


async def check_user_result_handler(callback: types.CallbackQuery, state: FSMContext) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    user_id = callback.from_user.id
    got_result = await check_user_result(user_id=user_id)

    if got_result:
        animal_name = got_result[4]
        db_animal = await get_db_animal(animal=animal_name)

        if db_animal:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=U_HAVE_RESULT,
                reply_markup=inline_keyboard_see_quiz_result_or_try_again,
            )
            logging.info(f' {datetime.now()} :\n'
                         f'User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} can get previous result or start quiz again.')

        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f'Ты <b>{animal_name}</b>❤\n\n'
                     f'К сожалению, сейчас я не смогу рассказать о твоем тотемном животном больше, но ты всегда '
                     f'можешь найти его на <a href="{MOSCOW_ZOO_ANIMALS}">на сайте Московского зоопарка</a>📌\n\n'
                     f'Хочешь сделать что-нибудь еще?',
                reply_markup=inline_keyboard_after_result,
            )
            logging.info(f' {datetime.now()} :\n'
                         f'User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} want to see previous result = {animal_name} '
                         f'but this animal was deleted from database.')

    else:
        await start_quiz_inline_button(
            callback=callback,
            state=state,
        )
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} do not have previous result and started new quiz.')


async def show_result_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    result = await check_user_result(user_id=callback.from_user.id)

    if result:
        animal_name = result[4]
        db_animal = await get_db_animal(animal=animal_name)

        if db_animal:
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
                text=result_text,
            )
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f"В Московском зоопарке представителем этого вида является {nickname}🐥\n"
                     f"О {'ней' if gender else 'нём'} и {'её' if gender else 'его'} сородичах можно почитать "
                     f"<b><a href='{animal_url}'>тут</a></b>👀",
                reply_markup=inline_keyboard_whats_next,
            )

            if callback.data == 'see_previous_result':
                logging.info(f' {datetime.now()} :\n'
                             f'User with ID = {callback.from_user.id} and username = '
                             f'{callback.from_user.username} want to see previous result = {animal_name}.')
            else:
                logging.info(f' {datetime.now()} :\n'
                             f'User with ID = {callback.from_user.id} and username = '
                             f'{callback.from_user.username} got new quiz result = {animal_name}.')

        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f'Ты <b>{animal_name}</b>❤\n\n'
                     f'К сожалению, сейчас я не смогу рассказать о твоем тотемном животном больше, но ты всегда '
                     f'можешь найти его на <a href="{MOSCOW_ZOO_ANIMALS}">на сайте Московского зоопарка</a>📌\n\n'
                     f'Хочешь сделать что-нибудь еще?',
                reply_markup=inline_keyboard_after_result,
            )
            logging.info(f' {datetime.now()} :\n'
                         f'User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} want to see previous result = {animal_name} '
                         f'but this animal was deleted from database.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=NEVER_QUIZ + SOMETHING_ELSE,
            reply_markup=inline_keyboard_after_result,
        )
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} want to see previous result '
                     f'without completing quiz at least once.')


async def after_result_menu_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)

    if callback.data == 'whats_next':
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=WHAT_DO_U_WANT,
            reply_markup=inline_keyboard_after_result,
        )
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} finished quiz and activated after quiz menu.')
    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=SOMETHING_ELSE,
            reply_markup=inline_keyboard_after_result,
        )
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} activated after quiz menu.')


async def picture_to_save_handler(callback: types.CallbackQuery) -> None:
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
            logging.info(f' {datetime.now()} :\n'
                         f'User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} get a result = {animal_name} HD picture to save.')

        else:
            await bot.send_message(
                chat_id=callback.from_user.id,
                text=f'Ты <b>{animal_name}</b> ❤\n'
                     f'Но я тебе не расскажу о нём 🥺' + SOMETHING_ELSE,
                reply_markup=inline_keyboard_after_result,
            )
            logging.info(f' {datetime.now()} :\n'
                         f'User with ID = {callback.from_user.id} and username = '
                         f'{callback.from_user.username} want to get previous HD picture of result = {animal_name} '
                         f'but it was deleted from database.')

    else:
        await bot.send_message(
            chat_id=callback.from_user.id,
            text=NEVER_QUIZ + SOMETHING_ELSE,
            reply_markup=inline_keyboard_after_result,
        )
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {callback.from_user.id} and username = '
                     f'{callback.from_user.username} tried to get HD picture of result to save '
                     f'without completing quiz at least once.')


async def care_program_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo='AgACAgIAAxkBAAIKzWTfpaGdaY8MlzBsdHk9Re-OWpU4AALgyzEb6Cn4StQIfF0AARrflwEAAwIAA3MAAzAE',
        caption=CLUB_FRIENDS_INFO,
        reply_markup=inline_keyboard_care_program,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} watching care program info.')


async def care_program_contacts_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=CONTACTS,
        reply_markup=inline_keyboard_thank_you,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} watching care program contacts.')


async def thats_enough_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_message(
        chat_id=callback.from_user.id,
        text=THANKS_FOR_TALK,
        reply_markup=inline_keyboard_likewise,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} ending chat with bot.')


async def see_ya_handler(callback: types.CallbackQuery) -> None:
    await bot.answer_callback_query(callback_query_id=callback.id)
    await bot.send_photo(
        chat_id=callback.from_user.id,
        photo='AgACAgIAAxkBAAIK0GTfpcm3p5ZJa6oj6eqZX7MoBmGiAALhyzEb6Cn4SjgIaWUVgvJEAQADAgADcwADMAQ',
        caption=SEE_YOU,
    )
    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {callback.from_user.id} and username = '
                 f'{callback.from_user.username} finished the bot.')


# ---------------------
# Handlers registration
def register_static_command_handlers(disp: Dispatcher) -> None:
    disp.register_message_handler(
        help_handler,
        commands=[f'{HELP_COMMAND}'],
        state='*',
    )
    disp.register_callback_query_handler(
        help_to_restart_bot_handler,
        lambda callback: callback.data == 'stopped_at_start_bot',
        state='*',
    )
    disp.register_callback_query_handler(
        help_to_restart_quiz_handler,
        lambda callback: callback.data == 'stopped_at_quiz',
        state='*',
    )
    disp.register_message_handler(
        contacts_handler,
        commands=[f'{CONTACTS_COMMAND}'],
        state='*',
    )
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
