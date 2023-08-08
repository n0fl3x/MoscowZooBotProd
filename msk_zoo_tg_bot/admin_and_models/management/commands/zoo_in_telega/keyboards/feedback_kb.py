from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from commands.feedback_commands import CANCEL_FEEDBACK_COMMAND


# CANCEL FEEDBACK
inline_btn_cancel_feedback = InlineKeyboardButton(
    text='Не хочу оставлять отзыв',
    callback_data=f'/{CANCEL_FEEDBACK_COMMAND}'
)

inline_keyboard_cancel_feedback = InlineKeyboardMarkup().row(inline_btn_cancel_feedback)
