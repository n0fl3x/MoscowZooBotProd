import logging
import os
import sqlite3 as sql

from datetime import datetime
from aiogram.dispatcher.storage import FSMContext

from msk_zoo_tg_bot.settings import BASE_DIR


connect = sql.connect(os.path.join(BASE_DIR, 'zoo_bot_db.sqlite3'))
curs = connect.cursor()


async def get_all_animals_stats() -> dict:
    """Функция для получения словаря с названиями всех животных из БД и только их коэффициентов
    для использования при определении результата опроса."""

    all_animals = curs.execute(
        """SELECT * 
        FROM 'admin_and_models_animal'"""
    )
    connect.commit()

    animals_with_stats = {}
    for row in all_animals:
        animal = row[1]
        animal_stats = row[8:]
        animals_with_stats.update([(animal, animal_stats)])

    return animals_with_stats


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
        logging.info(f' {datetime.now()} : New result of user with ID {user_id} and username = {username} '
                     f'successfully added to database.')


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
        logging.info(f' {datetime.now()} : Old result of user with ID {user_id} successfully deleted from database.')


async def check_user_result(state: FSMContext) -> bool:
    """Функция для проверки проходил ли уже текущий пользователь опрос хотя бы один раз."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        result = curs.execute(
            f"""SELECT * 
            FROM 'admin_and_models_result' 
            WHERE res_user_id = '{user_id}'"""
        ).fetchone()
        connect.commit()

        if result:
            return True
        return False


async def insert_new_feedback(user_id: int, username: str, text: str) -> None:
    """Функция для добавления нового отзыва в БД."""

    fb_id = curs.execute(
        """SELECT max(id) 
        FROM 'admin_and_models_feedback'"""
    ).fetchone()[0]
    connect.commit()

    if fb_id is not None:
        fb_id += 1
    else:
        fb_id = 1

    created_at = datetime.now()
    user_result = curs.execute(
        f"""SELECT res_totem_animal 
        FROM 'admin_and_models_result' 
        WHERE res_user_id = '{user_id}'"""
    ).fetchone()
    connect.commit()

    if not user_result:
        return
    else:
        animal = user_result[0]

    to_insert = (fb_id, created_at, animal, user_id, username, text)

    curs.execute(
        """INSERT INTO 'admin_and_models_feedback'
        VALUES (?, ?, ?, ?, ?, ?)""",
        to_insert,
    )
    connect.commit()
    logging.info(f' {datetime.now()} : New feedback of user with ID {user_id} and username = {username}'
                 f'successfully added to database.')


async def delete_old_feedback(user_id: int) -> None:
    """Функция для удаления уже существующего отзыва пользователя из БД."""

    curs.execute(
        f"""DELETE FROM 'admin_and_models_feedback' 
        WHERE fb_user_id = '{user_id}'"""
    )
    connect.commit()
    logging.info(f' {datetime.now()} : Old feedback successfully deleted from database.')


async def check_user_feedback(user_id: int):
    """Функция для проверки наличия отзыва от текущего пользователя."""

    fb = curs.execute(
        f"""SELECT * 
        FROM 'admin_and_models_feedback' 
        WHERE fb_user_id = '{user_id}'"""
    ).fetchone()
    connect.commit()

    if fb:
        return True
    return False
