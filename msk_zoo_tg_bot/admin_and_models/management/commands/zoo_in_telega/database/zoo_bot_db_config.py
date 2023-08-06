import logging
import os
import sqlite3 as sql
from datetime import datetime
from aiogram.dispatcher.storage import FSMContext

from msk_zoo_tg_bot.settings import BASE_DIR


connect = sql.connect(os.path.join(BASE_DIR, 'zoo_bot_db.sqlite3'))
curs = connect.cursor()


async def get_all_animals_stats() -> dict:
    """Функция для получения словаря с названиями всех животных из БД и только их коэффициентов."""

    all_animals = curs.execute(
        """SELECT * 
        FROM 'admin_and_models_animal'"""
    )
    connect.commit()

    animals_with_stats = {}
    for animal in all_animals:
        key = animal[1]
        animal_stats = animal[5:]
        animals_with_stats.update([(key, animal_stats)])

    return animals_with_stats


async def insert_new_results(state: FSMContext, animal: str):
    """Функция для вставки новой записи с результатами опроса,
    если пользователь впервые его проходит."""

    async with state.proxy() as data:
        record_id = curs.execute(
            """SELECT max(id) 
            FROM 'admin_and_models_result'"""
        ).fetchone()[0]

        if record_id is not None:
            record_id += 1
        else:
            record_id = 1

        created_at = datetime.now()
        user = str(data.get('user_id'))
        user_results = data.get('1st_question') + ", " \
            + data.get('2nd_question') + ", " \
            + data.get('3rd_question') + ", " \
            + data.get('4th_question') + ", " \
            + data.get('5th_question') + ", " \
            + data.get('6th_question') + ", " \
            + data.get('7th_question') + ", " \
            + data.get('8th_question') + ", " \
            + data.get('9th_question')

        to_insert = (record_id, created_at, user, animal, user_results)
        curs.execute(
            """INSERT INTO 'admin_and_models_result'
            VALUES (?, ?, ?, ?, ?)""",
            to_insert,
        )
        connect.commit()
        logging.info(f' {datetime.now()} : New result successfully added to database.')


async def delete_old_results(state: FSMContext, animal: str):
    """Функция, удаляющая существующую запись с результатами опроса,
    если пользователь его уже проходил."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        curs.execute(
            f"""DELETE FROM 'admin_and_models_result' 
            WHERE res_user_id = '{user_id}'"""
        )
        connect.commit()
        logging.info(f' {datetime.now()} : Old result successfully deleted from database.')
        await insert_new_results(
            state=state,
            animal=animal,
        )


async def check_user_result(state: FSMContext, animal: str):
    """Функция для проверки проходил ли уже текущий пользователь опрос хотя бы один раз."""

    async with state.proxy() as data:
        user_id = data.get('user_id')
        result = curs.execute(
            f"""SELECT * 
            FROM 'admin_and_models_result' 
            WHERE res_user_id = '{user_id}'"""
        )

        if not result:
            await insert_new_results(
                state=state,
                animal=animal,
            )
        else:
            await delete_old_results(
                state=state,
                animal=animal,
            )


async def insert_new_feedback(user_id: int, username: str, text: str):
    """Функция для добавления нового отзыва в БД."""

    fb_id = curs.execute(
        """SELECT max(id) 
        FROM 'admin_and_models_feedback'"""
    ).fetchone()[0]
    print(fb_id)

    if fb_id is not None:
        fb_id += 1
    else:
        fb_id = 1
    print(fb_id)

    created_at = datetime.now()
    user_result = curs.execute(
        f"""SELECT res_totem_animal 
        FROM 'admin_and_models_result' 
        WHERE res_user_id = '{user_id}'"""
    ).fetchone()
    print(user_result)

    if not user_result:
        return
    else:
        animal = user_result[0]
        print(animal)

    to_insert = (fb_id, created_at, animal, user_id, username, text)
    print(to_insert)

    curs.execute(
        """INSERT INTO 'admin_and_models_feedback'
        VALUES (?, ?, ?, ?, ?, ?)""",
        to_insert,
    )
    connect.commit()
    logging.info(f' {datetime.now()} : New feedback successfully added to database.')


async def delete_old_feedback(user_id: int, username: str, text: str):
    """Функция для удаления уже существующего отзыва пользователя из БД."""

    curs.execute(
        f"""DELETE FROM 'admin_and_models_feedback' 
                WHERE fb_user_id = '{user_id}'"""
    )
    connect.commit()
    logging.info(f' {datetime.now()} : Old feedback successfully deleted from database.')
    await insert_new_feedback(
        user_id=user_id,
        username=username,
        text=text,
    )


async def check_user_feedback(user_id: int, username: str, text: str):
    """Функция для проверки наличия отзыва от текущего пользователя."""

    fb = curs.execute(
        f"""SELECT * 
        FROM 'admin_and_models_feedback' 
        WHERE fb_user_id = '{user_id}'"""
    ).fetchone()

    if not fb:
        await insert_new_feedback(
            user_id=user_id,
            username=username,
            text=text,
        )
        return 'kek'
    else:
        await delete_old_feedback(
            user_id=user_id,
            username=username,
            text=text,
        )
