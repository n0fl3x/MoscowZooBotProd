from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from admin_and_models.management.commands.zoo_in_telega.urls.quiz_animals_urls import (
    ANIMAL_1_URL,
    ANIMAL_2_URL,
    ANIMAL_3_URL,
    ANIMAL_4_URL,
    ANIMAL_5_URL,
    ANIMAL_6_URL,
    ANIMAL_7_URL,
    ANIMAL_8_URL,
    ANIMAL_9_URL,
    ANIMAL_10_URL,
    ANIMAL_11_URL,
)


LETS_SEE = """Подробнее"""


# ---------
# Бинтуронг
inline_btn_result_1 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_1_URL,
)

inline_keyboard_result_1 = InlineKeyboardMarkup().add(inline_btn_result_1)


# --------
# Капибара
inline_btn_result_2 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_2_URL,
)

inline_keyboard_result_2 = InlineKeyboardMarkup().add(inline_btn_result_2)


# --------
# Большая панда
inline_btn_result_3 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_3_URL,
)

inline_keyboard_result_3 = InlineKeyboardMarkup().add(inline_btn_result_3)


# --------
# Никобарский голубь
inline_btn_result_4 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_4_URL,
)

inline_keyboard_result_4 = InlineKeyboardMarkup().add(inline_btn_result_4)


# --------
# Медоед
inline_btn_result_5 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_5_URL,
)

inline_keyboard_result_5 = InlineKeyboardMarkup().add(inline_btn_result_5)


# --------
# Японский макак
inline_btn_result_6 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_6_URL,
)

inline_keyboard_result_6 = InlineKeyboardMarkup().add(inline_btn_result_6)


# --------
# Ягуарунди
inline_btn_result_7 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_7_URL,
)

inline_keyboard_result_7 = InlineKeyboardMarkup().add(inline_btn_result_7)


# --------
# Ушастый ёж
inline_btn_result_8 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_8_URL,
)

inline_keyboard_result_8 = InlineKeyboardMarkup().add(inline_btn_result_8)


# --------
# Заяц-беляк
inline_btn_result_9 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_9_URL,
)

inline_keyboard_result_9 = InlineKeyboardMarkup().add(inline_btn_result_9)


# --------
# Китайский аллигатор
inline_btn_result_10 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_10_URL,
)

inline_keyboard_result_10 = InlineKeyboardMarkup().add(inline_btn_result_10)


# --------
# Львиный тамарин
inline_btn_result_11 = InlineKeyboardButton(
    text=LETS_SEE,
    url=ANIMAL_11_URL,
)

inline_keyboard_result_11 = InlineKeyboardMarkup().add(inline_btn_result_11)
