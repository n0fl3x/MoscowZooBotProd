from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Feedback button
inline_btn_leave_feedback = InlineKeyboardButton(
    text='Оставить отзыв',
    callback_data='go_feedback',
)


# Cancel feedback
inline_btn_cancel_feedback = InlineKeyboardButton(
    text='Не хочу оставлять отзыв',
    callback_data='cancel_feedback'
)

inline_keyboard_cancel_feedback = InlineKeyboardMarkup().row(inline_btn_cancel_feedback)
