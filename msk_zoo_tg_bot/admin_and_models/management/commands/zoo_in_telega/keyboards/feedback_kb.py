from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from commands.feedback_commands import START_FEEDBACK_COMMAND, CANCEL_FEEDBACK_COMMAND
from text_data.timosha_messages import LEAVE_FEEDBACK_BTN, CHANGED_MY_MIND


# Feedback button
inline_btn_leave_feedback = InlineKeyboardButton(
    text=LEAVE_FEEDBACK_BTN,
    callback_data=START_FEEDBACK_COMMAND,
)


# Cancel feedback
inline_btn_cancel_feedback = InlineKeyboardButton(
    text=CHANGED_MY_MIND,
    callback_data=CANCEL_FEEDBACK_COMMAND,
)

inline_keyboard_cancel_feedback = InlineKeyboardMarkup().row(inline_btn_cancel_feedback)
