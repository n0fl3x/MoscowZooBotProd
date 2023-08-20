from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text_data.timosha_messages import LEAVE_FEEDBACK_BTN, NO_BTN


# Feedback button
inline_btn_leave_feedback = InlineKeyboardButton(
    text=LEAVE_FEEDBACK_BTN,
    callback_data='go_feedback',
)


# Cancel feedback
inline_btn_cancel_feedback = InlineKeyboardButton(
    text=NO_BTN,
    callback_data='cancel_feedback'
)

inline_keyboard_cancel_feedback = InlineKeyboardMarkup().row(inline_btn_cancel_feedback)
