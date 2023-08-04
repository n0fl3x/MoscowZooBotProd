# TODO: реализовать функционал, позволяющий проверить, проходил ли текущий пользователь опрос
# TODO: хотя бы один раз, и если да, то предлагать ему вывести результат прошлого опроса


import logging
import os
import sqlite3 as sql

from datetime import datetime
from aiogram.dispatcher.storage import FSMContext

from msk_zoo_tg_bot.settings import BASE_DIR

connect = sql.connect(os.path.join(BASE_DIR, 'zoo_bot_db.sqlite3'))
curs = connect.cursor()


async def db_start():
    """Функция, создающая таблицу в базе данных для учёта ответов пользователей.
    Если таблица уже существует, то просто подключается к ней."""

    if connect:
        logging.info(f' {datetime.now()} : Successfully connected to database.')
    else:
        logging.info(f' {datetime.now()} : NO CONNECTION TO DATABASE')

    curs.execute(
        """CREATE TABLE IF NOT EXISTS quiz_results (
        user_id TEXT PRIMARY KEY,
        answers TEXT)"""
    )
    connect.commit()


async def get_all_animals_stats():
    all_animals = curs.execute("""SELECT * FROM 'admin_and_models_animal'""")
    connect.commit()

    animals_with_stats = {}
    for animal in all_animals:
        key = animal[1]
        animal_stats = animal[5:]
        animals_with_stats.update([(key, animal_stats)])

    return animals_with_stats


async def db_insert_new_results(state: FSMContext):
    """Функция для вставки новой записи с результатами опроса,
    если пользователь впервые его проходит."""

    async with state.proxy() as data:
        user = str(data.get('user_id'))
        user_results = data.get('1st_question') + ", " \
            + data.get('2nd_question') + ", " \
            + data.get('3rd_question') + ", " \
            + data.get('4th_question') + ", " \
            + data.get('5th_question')

        to_insert = (user, user_results)
        curs.execute(
            """INSERT INTO quiz_results
            VALUES (?, ?)""",
            to_insert,
        )
        connect.commit()
        logging.info(f' {datetime.now()} : New record successfully added to database.')


async def db_delete_old_results(state: FSMContext):
    """Функция, удаляющая существующую запись с результатами опроса,
    если пользователь его уже проходил."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        curs.execute(f"""DELETE FROM quiz_results WHERE user_id = '{user_id}'""")
        connect.commit()
        logging.info(f' {datetime.now()} : Old record successfully deleted from database.')
        await db_insert_new_results(state=state)


async def check_user_db_record(state: FSMContext):
    """Функция для проверки проходил ли уже текущий пользователь опрос хотя бы один раз."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        find = curs.execute(f"""SELECT user_id FROM quiz_results WHERE user_id = '{user_id}'""")

        if not find:
            await db_insert_new_results(state=state)
        else:
            await db_delete_old_results(state=state)
