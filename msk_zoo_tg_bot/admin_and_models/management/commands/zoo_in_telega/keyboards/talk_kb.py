from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text_data.bot_urls import VK_SHARE
from keyboards.feedback_kb import inline_btn_leave_feedback

from text_data.timosha_messages import (
    HELLO_QUIZ_BTN,
    I_DONT_WANT_BTN,
    OKAY_BTN,
    SHOW_RESULT_BTN,
    ONCE_AGAIN_BTN,
    YEP,
    WHATS_NEXT,
    SAVE_RESULT_BTN,
    SHARE_BOT_BTN,
    WHATS_HERE_BTN,
    NO_ENOUGH_BTN,
    CONTACTS_BTN,
    THANK_YOU_BTN,
    THANKS4SAVE_BTN,
    NO_BTN,
    CONTACTS_THANKS_BTN,
    VERY_BEGINING,
    FROM_QUIZ,
)


# ---
inline_btn_start_bot = InlineKeyboardButton(
    text=VERY_BEGINING,
    callback_data='stopped_at_start_bot',
)

inline_btn_run_quiz = InlineKeyboardButton(
    text=FROM_QUIZ,
    callback_data='stopped_at_quiz',
)

inline_keyboard_help_msg = InlineKeyboardMarkup().\
    row(inline_btn_start_bot).\
    row(inline_btn_run_quiz)


# ---
inline_btn_start_quiz = InlineKeyboardButton(
    text=HELLO_QUIZ_BTN,
    callback_data='check_result_before_quiz',
)

inline_btn_dont_want_to_start_quiz = InlineKeyboardButton(
    text=I_DONT_WANT_BTN,
    callback_data='dont_want_quiz',
)

inline_keyboard_start_msg = InlineKeyboardMarkup().\
    row(inline_btn_start_quiz).\
    row(inline_btn_dont_want_to_start_quiz)


# ---
inline_btn_ok_lets_go_quiz = InlineKeyboardButton(
    text=OKAY_BTN,
    callback_data='check_result_before_quiz',
)

inline_keyboard_ok_lets_go_quiz = InlineKeyboardMarkup().\
    row(inline_btn_ok_lets_go_quiz)


# ---
inline_btn_see_previous_result = InlineKeyboardButton(
    text=SHOW_RESULT_BTN,
    callback_data='see_previous_result',
)

inline_btn_try_quiz_again = InlineKeyboardButton(
    text=ONCE_AGAIN_BTN,
    callback_data='go_quiz',
)

inline_keyboard_see_quiz_result_or_try_again = InlineKeyboardMarkup().\
    row(inline_btn_see_previous_result).\
    row(inline_btn_try_quiz_again)


# ---
inline_btn_show_my_result = InlineKeyboardButton(
    text=YEP,
    callback_data='show_me_result',
)

inline_keyboard_show_me_result = InlineKeyboardMarkup().\
    row(inline_btn_show_my_result)


# ---
inline_btn_whats_next = InlineKeyboardButton(
    text=WHATS_NEXT,
    callback_data='whats_next',
)

inline_keyboard_whats_next = InlineKeyboardMarkup().\
    row(inline_btn_whats_next)


# ---
inline_btn_save_picture = InlineKeyboardButton(
    text=SAVE_RESULT_BTN,
    callback_data='save_picture',
)

inline_btn_share_bot = InlineKeyboardButton(
    text=SHARE_BOT_BTN,
    url=VK_SHARE,
)

inline_btn_care_program = InlineKeyboardButton(
    text=WHATS_HERE_BTN,
    callback_data='care_program',
)

inline_btn_thats_enough = InlineKeyboardButton(
    text=NO_ENOUGH_BTN,
    callback_data='thats_enough',
)

inline_keyboard_after_result = InlineKeyboardMarkup().\
    row(inline_btn_try_quiz_again).\
    row(inline_btn_save_picture).\
    row(inline_btn_share_bot).\
    row(inline_btn_leave_feedback).\
    row(inline_btn_care_program).\
    row(inline_btn_thats_enough)


# ---
inline_btn_thank_you_for_feedback = InlineKeyboardButton(
    text=CONTACTS_THANKS_BTN,
    callback_data='thank_you',
)

inline_keyboard_thank_you = InlineKeyboardMarkup().\
    row(inline_btn_thank_you_for_feedback)


# ---
inline_btn_thank_you_pic_save = InlineKeyboardButton(
    text=THANKS4SAVE_BTN,
    callback_data='thank_you',
)

inline_keyboard_thank_you_pic_save = InlineKeyboardMarkup().\
    row(inline_btn_thank_you_pic_save)


# ---
inline_btn_welp = InlineKeyboardButton(
    text='Штош',
    callback_data='welp',
)

inline_keyboard_welp = InlineKeyboardMarkup().\
    row(inline_btn_welp)


# ---
inline_btn_care_program_contacts = InlineKeyboardButton(
    text=CONTACTS_BTN,
    callback_data='care_program_contacts',
)

inline_btn_no_thanks = InlineKeyboardButton(
    text=NO_BTN,
    callback_data='thank_you',
)

inline_keyboard_care_program = InlineKeyboardMarkup().\
    row(inline_btn_care_program_contacts).\
    row(inline_btn_no_thanks)


# ---
inline_btn_likewise = InlineKeyboardButton(
    text=THANK_YOU_BTN,
    callback_data='likewise',
)

inline_keyboard_likewise = InlineKeyboardMarkup().\
    row(inline_btn_likewise)
