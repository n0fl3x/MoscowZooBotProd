from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_start_quiz = InlineKeyboardButton(
    text='Начать викторину',
    callback_data='start_quiz',
)

inline_btn_dont_want_to_start_quiz = InlineKeyboardButton(
    text='А я не хочу',
    callback_data='dont_want_quiz',
)

inline_keyboard_start_msg = InlineKeyboardMarkup().\
    row(inline_btn_start_quiz).\
    row(inline_btn_dont_want_to_start_quiz)


# ---
inline_btn_ok_lets_go_quiz = InlineKeyboardButton(
    text="Ладно погнали",
    callback_data='ok_start_quiz',
)

inline_keyboard_ok_lets_go_quiz = InlineKeyboardMarkup().\
    row(inline_btn_ok_lets_go_quiz)


# ---
inline_btn_see_previous_result = InlineKeyboardButton(
    text='Хочу увидеть предыдущий результат',
    callback_data='see_previous_result',
)

inline_btn_try_quiz_again = InlineKeyboardButton(
    text='Хочу заново пройти опрос',
    callback_data='go_quiz_again',
)

inline_keyboard_see_quiz_result_or_try_again = InlineKeyboardMarkup().\
    row(inline_btn_see_previous_result).\
    row(inline_btn_try_quiz_again)
