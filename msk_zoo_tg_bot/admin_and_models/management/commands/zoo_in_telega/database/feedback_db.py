import logging
import os
import sqlite3 as sql

from datetime import datetime

from msk_zoo_tg_bot.settings import BASE_DIR


connect = sql.connect(os.path.join(BASE_DIR, 'zoo_bot_db.sqlite3'))
curs = connect.cursor()


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
    logging.info(f' {datetime.now()} : New feedback of user with ID {user_id} and username = {username} '
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
