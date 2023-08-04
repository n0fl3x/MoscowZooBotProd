import logging
import os

from dotenv import load_dotenv, find_dotenv

from aiogram import Bot
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv(find_dotenv())


# ------------
# Bot settings
storage = MemoryStorage()

bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))

dp = Dispatcher(
    bot=bot,
    storage=storage
)


# -------
# Logging
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
