from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from admin_and_models.management.commands.zoo_in_telega.urls.static_commands_urls import (
    ZOO_HISTORY_URL,
    YOUTUBE_CHANNEL_URL,
)

from admin_and_models.management.commands.zoo_in_telega.texts.static_commands_buttons_text import (
    HISTORY_BUTTON_TEXT,
    YOUTUBE_BUTTON_TEXT,
)


about_website_btn = InlineKeyboardButton(
    text=HISTORY_BUTTON_TEXT,
    url=ZOO_HISTORY_URL,
)

about_youtube_btn = InlineKeyboardButton(
    text=YOUTUBE_BUTTON_TEXT,
    url=YOUTUBE_CHANNEL_URL,
)

about_inline_keyboard = InlineKeyboardMarkup().add(about_website_btn).add(about_youtube_btn)
