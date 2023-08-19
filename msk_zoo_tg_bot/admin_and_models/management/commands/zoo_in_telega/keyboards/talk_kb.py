from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_start_quiz = InlineKeyboardButton(
    text='Начать викторину',
    callback_data='check_result_before_quiz',
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
    callback_data='check_result_before_quiz',
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
    callback_data='go_quiz',
)

inline_keyboard_see_quiz_result_or_try_again = InlineKeyboardMarkup().\
    row(inline_btn_see_previous_result).\
    row(inline_btn_try_quiz_again)


# ---
inline_btn_show_my_result = InlineKeyboardButton(
    text='Конечно!',
    callback_data='show_me_result',
)

inline_keyboard_show_me_result = InlineKeyboardMarkup().\
    row(inline_btn_show_my_result)


# ---
inline_btn_whats_next = InlineKeyboardButton(
    text='Ок, что дальше?',
    callback_data='whats_next',
)

inline_keyboard_whats_next = InlineKeyboardMarkup().\
    row(inline_btn_whats_next)


# ---
inline_btn_save_picture = InlineKeyboardButton(
    text='Сохранить результат в виде картинки',
    callback_data='save_picture',
)

inline_btn_share_bot = InlineKeyboardButton(
    text='Рассказать о Тимофее',
    url='https://vk.com/share.php?url=https://t.me/Moscow_Zoo_bot',
)

inline_btn_leave_feedback = InlineKeyboardButton(
    text='Оставить отзыв',
    callback_data='leave_feedback',
)

inline_btn_care_program = InlineKeyboardButton(
    text='А тут что?',
    callback_data='care_program',
)

inline_keyboard_after_result = InlineKeyboardMarkup().\
    row(inline_btn_try_quiz_again).\
    row(inline_btn_save_picture).\
    row(inline_btn_share_bot).\
    row(inline_btn_leave_feedback).\
    row(inline_btn_care_program)


# ---
inline_btn_thank_you = InlineKeyboardButton(
    text='Спасибо',
    callback_data='thank_you',
)

inline_keyboard_thank_you = InlineKeyboardMarkup().\
    row(inline_btn_thank_you)


# ---
inline_btn_welp = InlineKeyboardButton(
    text='Штош',
    callback_data='welp',
)

inline_keyboard_welp = InlineKeyboardMarkup().\
    row(inline_btn_welp)


# ---
inline_btn_care_program_contacts = InlineKeyboardButton(
    text='Контакты',
    callback_data='care_program_contacts',
)

inline_btn_care_program_website = InlineKeyboardButton(
    text='Сайт',
    url='https://moscowzoo.ru/',
)

inline_keyboard_care_program = InlineKeyboardMarkup().\
    row(inline_btn_care_program_contacts).\
    row(inline_btn_care_program_website).\
    row(inline_btn_thank_you)
