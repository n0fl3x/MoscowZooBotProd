from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from commands.quiz_commands import CONTINUE_QUIZ_COMMAND
from text_data.quiz_messages_text import WANT_TO_CONTINUE_QUIZ_BTN
from text_data.timosha_messages import LEAVE_FEEDBACK_BTN, CHANGED_MY_MIND_BTN

from commands.feedback_commands import (
    START_FEEDBACK_COMMAND,
    CANCEL_FEEDBACK_COMMAND,
    CANCEL_QUIZ_TO_GO_FEEDBACK_COMMAND,
)


# ---
inline_btn_leave_feedback = InlineKeyboardButton(
    text=LEAVE_FEEDBACK_BTN,
    callback_data=START_FEEDBACK_COMMAND,
)

inline_btn_cancel_feedback = InlineKeyboardButton(
    text=CHANGED_MY_MIND_BTN,
    callback_data=CANCEL_FEEDBACK_COMMAND,
)

inline_keyboard_cancel_feedback = InlineKeyboardMarkup().row(inline_btn_cancel_feedback)


# ---
inline_btn_cancel_quiz_to_start_fb = InlineKeyboardButton(
    text=LEAVE_FEEDBACK_BTN,
    callback_data=CANCEL_QUIZ_TO_GO_FEEDBACK_COMMAND,
)

inline_btn_continue_quiz = InlineKeyboardButton(
    text=WANT_TO_CONTINUE_QUIZ_BTN,
    callback_data=CONTINUE_QUIZ_COMMAND,
)

inline_keyboard_cancel_quiz_to_start_fb = InlineKeyboardMarkup().\
    row(inline_btn_cancel_quiz_to_start_fb).\
    row(inline_btn_continue_quiz)
