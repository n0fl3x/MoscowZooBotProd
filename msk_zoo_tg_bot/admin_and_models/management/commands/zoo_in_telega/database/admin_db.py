import logging
import os
import sqlite3 as sql

from datetime import datetime

from msk_zoo_tg_bot.settings import BASE_DIR


connect = sql.connect(os.path.join(BASE_DIR, 'zoo_bot_db.sqlite3'))
curs = connect.cursor()


async def tg_admin_auth(tg_username: str, user_id: int) -> bool:
    """Функция проверки доступа текущего пользователя в админ-панель Telegram."""

    db_admin = curs.execute(
        f"""SELECT *
        FROM 'auth_user'
        WHERE username = '{tg_username}'"""
    ).fetchone()

    if db_admin:
        logging.info(f' {datetime.now()} :\n'
                     f'User with ID = {user_id} and username = {tg_username} '
                     f'successfully founded as admin in database.')
        return True

    logging.info(f' {datetime.now()} :\n'
                 f'User with ID = {user_id} and username = {tg_username} '
                 f'did not found as admin in database.')
    return False
