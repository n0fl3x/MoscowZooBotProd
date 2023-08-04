from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from admin_and_models.management.commands.zoo_in_telega.texts.static_commands_buttons_text import CONTACTS_BUTTON_TEXT
from admin_and_models.management.commands.zoo_in_telega.urls.static_commands_urls import ZOO_CONTACTS_URL


zoo_contacts_btn = InlineKeyboardButton(
    text=CONTACTS_BUTTON_TEXT,
    url=ZOO_CONTACTS_URL,
)

zoo_contacts_inline_keyboard = InlineKeyboardMarkup().add(zoo_contacts_btn)
