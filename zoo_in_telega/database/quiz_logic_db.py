import os
import sqlite3 as sql

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
