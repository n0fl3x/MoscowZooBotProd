from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text_data.quiz_q_and_a import answers


# QUESTION 1
inline_btn_1_1 = InlineKeyboardButton(
    text=f'{answers[0][0]}',
    callback_data=f'{answers[0][0]}',
)

inline_btn_1_2 = InlineKeyboardButton(
    text=f'{answers[0][1]}',
    callback_data=f'{answers[0][1]}',
)

inline_btn_1_3 = InlineKeyboardButton(
    text=f'{answers[0][2]}',
    callback_data=f'{answers[0][2]}',
)

inline_btn_1_4 = InlineKeyboardButton(
    text=f'{answers[0][3]}',
    callback_data=f'{answers[0][3]}',
)

inline_keyboard_1 = InlineKeyboardMarkup().\
    row(inline_btn_1_1).\
    row(inline_btn_1_2).\
    row(inline_btn_1_3).\
    row(inline_btn_1_4)


# QUESTION 2
inline_btn_2_1 = InlineKeyboardButton(
    text=f'{answers[1][0]}',
    callback_data=f'{answers[1][0]}',
)

inline_btn_2_2 = InlineKeyboardButton(
    text=f'{answers[1][1]}',
    callback_data=f'{answers[1][1]}',
)

inline_btn_2_3 = InlineKeyboardButton(
    text=f'{answers[1][2]}',
    callback_data=f'{answers[1][2]}',
)

inline_btn_2_4 = InlineKeyboardButton(
    text=f'{answers[1][3]}',
    callback_data=f'{answers[1][3]}',
)

inline_keyboard_2 = InlineKeyboardMarkup().\
    row(inline_btn_2_1).\
    row(inline_btn_2_2).\
    row(inline_btn_2_3).\
    row(inline_btn_2_4)


# QUESTION 3
inline_btn_3_1 = InlineKeyboardButton(
    text=f'{answers[2][0]}',
    callback_data=f'{answers[2][0]}',
)

inline_btn_3_2 = InlineKeyboardButton(
    text=f'{answers[2][1]}',
    callback_data=f'{answers[2][1]}',
)

inline_btn_3_3 = InlineKeyboardButton(
    text=f'{answers[2][2]}',
    callback_data=f'{answers[2][2]}',
)

inline_btn_3_4 = InlineKeyboardButton(
    text=f'{answers[2][3]}',
    callback_data=f'{answers[2][3]}',
)

inline_keyboard_3 = InlineKeyboardMarkup().\
    row(inline_btn_3_1).\
    row(inline_btn_3_2).\
    row(inline_btn_3_3).\
    row(inline_btn_3_4)


# QUESTION 4
inline_btn_4_1 = InlineKeyboardButton(
    text=f'{answers[3][0]}',
    callback_data=f'{answers[3][0]}',
)

inline_btn_4_2 = InlineKeyboardButton(
    text=f'{answers[3][1]}',
    callback_data=f'{answers[3][1]}',
)

inline_btn_4_3 = InlineKeyboardButton(
    text=f'{answers[3][2]}',
    callback_data=f'{answers[3][2]}',
)

inline_btn_4_4 = InlineKeyboardButton(
    text=f'{answers[3][3]}',
    callback_data=f'{answers[3][3]}',
)

inline_keyboard_4 = InlineKeyboardMarkup().\
    row(inline_btn_4_1).\
    row(inline_btn_4_2).\
    row(inline_btn_4_3).\
    row(inline_btn_4_4)


# QUESTION 5
inline_btn_5_1 = InlineKeyboardButton(
    text=f'{answers[4][0]}',
    callback_data=f'{answers[4][0]}',
)

inline_btn_5_2 = InlineKeyboardButton(
    text=f'{answers[4][1]}',
    callback_data=f'{answers[4][1]}',
)

inline_btn_5_3 = InlineKeyboardButton(
    text=f'{answers[4][2]}',
    callback_data=f'{answers[4][2]}',
)

inline_keyboard_5 = InlineKeyboardMarkup().\
    row(inline_btn_5_1).\
    row(inline_btn_5_2).\
    row(inline_btn_5_3)


# QUESTION 6
inline_btn_6_1 = InlineKeyboardButton(
    text=f'{answers[5][0]}',
    callback_data=f'{answers[5][0]}',
)

inline_btn_6_2 = InlineKeyboardButton(
    text=f'{answers[5][1]}',
    callback_data=f'{answers[5][1]}',
)

inline_btn_6_3 = InlineKeyboardButton(
    text=f'{answers[5][2]}',
    callback_data=f'{answers[5][2]}',
)

inline_keyboard_6 = InlineKeyboardMarkup().\
    row(inline_btn_6_1).\
    row(inline_btn_6_2).\
    row(inline_btn_6_3)


# QUESTION 7
inline_btn_7_1 = InlineKeyboardButton(
    text=f'{answers[6][0]}',
    callback_data=f'{answers[6][0]}',
)

inline_btn_7_2 = InlineKeyboardButton(
    text=f'{answers[6][1]}',
    callback_data=f'{answers[6][1]}',
)

inline_btn_7_3 = InlineKeyboardButton(
    text=f'{answers[6][2]}',
    callback_data=f'{answers[6][2]}',
)

inline_btn_7_4 = InlineKeyboardButton(
    text=f'{answers[6][3]}',
    callback_data=f'{answers[6][3]}',
)

inline_keyboard_7 = InlineKeyboardMarkup().\
    row(inline_btn_7_1).\
    row(inline_btn_7_2).\
    row(inline_btn_7_3).\
    row(inline_btn_7_4)


# QUESTION 8
inline_btn_8_1 = InlineKeyboardButton(
    text=f'{answers[7][0]}',
    callback_data=f'{answers[7][0]}',
)

inline_btn_8_2 = InlineKeyboardButton(
    text=f'{answers[7][1]}',
    callback_data=f'{answers[7][1]}',
)

inline_btn_8_3 = InlineKeyboardButton(
    text=f'{answers[7][2]}',
    callback_data=f'{answers[7][2]}',
)

inline_btn_8_4 = InlineKeyboardButton(
    text=f'{answers[7][3]}',
    callback_data=f'{answers[7][3]}',
)

inline_keyboard_8 = InlineKeyboardMarkup().\
    row(inline_btn_8_1).\
    row(inline_btn_8_2).\
    row(inline_btn_8_3).\
    row(inline_btn_8_4)


# QUESTION 9
inline_btn_9_1 = InlineKeyboardButton(
    text=f'{answers[8][0]}',
    callback_data=f'{answers[8][0]}',
)

inline_btn_9_2 = InlineKeyboardButton(
    text=f'{answers[8][1]}',
    callback_data=f'{answers[8][1]}',
)

inline_btn_9_3 = InlineKeyboardButton(
    text=f'{answers[8][2]}',
    callback_data=f'{answers[8][2]}',
)

inline_btn_9_4 = InlineKeyboardButton(
    text=f'{answers[8][3]}',
    callback_data=f'{answers[8][3]}',
)

inline_keyboard_9 = InlineKeyboardMarkup().\
    row(inline_btn_9_1).\
    row(inline_btn_9_2).\
    row(inline_btn_9_3).\
    row(inline_btn_9_4)
