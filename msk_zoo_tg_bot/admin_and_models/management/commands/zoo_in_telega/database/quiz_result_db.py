import logging
import os
import sqlite3 as sql

from datetime import datetime
from aiogram.dispatcher.storage import FSMContext

from msk_zoo_tg_bot.settings import BASE_DIR


connect = sql.connect(os.path.join(BASE_DIR, 'zoo_bot_db.sqlite3'))
curs = connect.cursor()


async def insert_new_result(state: FSMContext, animal: str) -> None:
    """Функция для вставки новой записи с результатами опроса,
    если пользователь впервые его проходит."""

    async with state.proxy() as data:
        record_id = curs.execute(
            """SELECT max(id) 
            FROM 'admin_and_models_result'"""
        ).fetchone()[0]
        connect.commit()

        if record_id:
            record_id += 1
        else:
            record_id = 1

        username = data.get('username')
        created_at = datetime.now()
        user_id = str(data.get('user_id'))
        user_results = data.get('1st_question') + ", " \
            + data.get('2nd_question') + ", " \
            + data.get('3rd_question') + ", " \
            + data.get('4th_question') + ", " \
            + data.get('5th_question') + ", " \
            + data.get('6th_question') + ", " \
            + data.get('7th_question') + ", " \
            + data.get('8th_question') + ", " \
            + data.get('9th_question')

        to_insert = (record_id, created_at, user_id, username, animal, user_results)

        curs.execute(
            """INSERT INTO 'admin_and_models_result'
            VALUES (?, ?, ?, ?, ?, ?)""",
            to_insert,
        )
        connect.commit()
        logging.info(f' {datetime.now()} :\n'
                     f'New result = {animal} of user with ID = {user_id} and '
                     f'username = {username} successfully added to database.')


async def delete_old_result(state: FSMContext) -> None:
    """Функция, удаляющая существующую запись с результатами опроса,
    если пользователь его уже проходил."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        curs.execute(
            f"""DELETE FROM 'admin_and_models_result' 
            WHERE res_user_id = '{user_id}'"""
        )
        connect.commit()
        logging.info(f' {datetime.now()} :\n'
                     f'Old result of user with ID = {user_id} successfully '
                     f'deleted from database.')


async def check_user_result(user_id: int) -> list:
    """Функция для проверки результата пользователя, если он/она уже проходил(-а) опрос хотя бы один раз."""

    result = curs.execute(
        f"""SELECT * 
        FROM 'admin_and_models_result' 
        WHERE res_user_id = '{user_id}'"""
    ).fetchone()
    connect.commit()

    return result


async def get_db_animal(animal: str) -> list:
    """Функция для поиска нужного животного из БД."""

    db_animal_record = curs.execute(
        f"""SELECT * 
        FROM 'admin_and_models_animal' 
        WHERE anim_animal = '{animal}'"""
    ).fetchone()
    connect.commit()

    return db_animal_record
