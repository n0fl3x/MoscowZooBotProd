import logging

from datetime import datetime
from random import choice

from database.quiz_logic_db import get_all_animals_stats
from text_data.quiz_q_and_a import answers


async def get_totem_animal(proxy_dict: dict) -> str:
    user_id = proxy_dict.pop('user_id')
    username = proxy_dict.pop('username')

    params = {
        'суточная активность': 0,
        'тип питания': 0,
        'среда обитания': 0,
        'климат': 0,
        'годовая активность': 0,
        'социальность': 0,
        'внешний вид': 0,
        'мечты': 0,
        'просто вопрос': 0,
    }

    # ------------
    # 1st question
    if proxy_dict['1st_question'] == answers[0][0]:
        params['суточная активность'] += 3
    if proxy_dict['1st_question'] == answers[0][1]:
        params['суточная активность'] += 1
    if proxy_dict['1st_question'] == answers[0][2]:
        params['суточная активность'] -= 1
    if proxy_dict['1st_question'] == answers[0][3]:
        params['суточная активность'] -= 3

    # ------------
    # 2nd question
    if proxy_dict['2nd_question'] == answers[1][0]:
        params['тип питания'] += 3
    if proxy_dict['2nd_question'] == answers[1][1]:
        params['тип питания'] += 1
    if proxy_dict['2nd_question'] == answers[1][2]:
        params['тип питания'] -= 1
    if proxy_dict['2nd_question'] == answers[1][3]:
        params['тип питания'] -= 3

    # ------------
    # 3rd question
    if proxy_dict['3rd_question'] == answers[2][0]:
        params['среда обитания'] += 3
    if proxy_dict['3rd_question'] == answers[2][1]:
        params['среда обитания'] += 1
    if proxy_dict['3rd_question'] == answers[2][2]:
        params['среда обитания'] -= 1
    if proxy_dict['3rd_question'] == answers[2][3]:
        params['среда обитания'] -= 3

    # ------------
    # 4th question
    if proxy_dict['4th_question'] == answers[3][0]:
        params['климат'] += 3
    if proxy_dict['4th_question'] == answers[3][1]:
        params['климат'] += 1
    if proxy_dict['4th_question'] == answers[3][2]:
        params['климат'] -= 1
    if proxy_dict['4th_question'] == answers[3][3]:
        params['климат'] -= 3

    # ------------
    # 5th question
    if proxy_dict['5th_question'] == answers[4][0]:
        params['годовая активность'] -= 3
    if proxy_dict['5th_question'] == answers[4][1]:
        params['годовая активность'] += 0
    if proxy_dict['5th_question'] == answers[4][2]:
        params['годовая активность'] += 3

    # ------------
    # 6th question
    if proxy_dict['6th_question'] == answers[5][0]:
        params['социальность'] += 3
    if proxy_dict['6th_question'] == answers[5][1]:
        params['социальность'] += 0
    if proxy_dict['6th_question'] == answers[5][2]:
        params['социальность'] -= 3

    # ------------
    # 7th question
    if proxy_dict['7th_question'] == answers[6][0]:
        params['внешний вид'] += 3
    if proxy_dict['7th_question'] == answers[6][1]:
        params['внешний вид'] += 1
    if proxy_dict['7th_question'] == answers[6][2]:
        params['внешний вид'] -= 1
    if proxy_dict['7th_question'] == answers[6][3]:
        params['внешний вид'] -= 3

    # ------------
    # 8th question
    if proxy_dict['8th_question'] == answers[7][0]:
        params['мечты'] += 3
    if proxy_dict['8th_question'] == answers[7][1]:
        params['мечты'] += 1
    if proxy_dict['8th_question'] == answers[7][2]:
        params['мечты'] -= 1
    if proxy_dict['8th_question'] == answers[7][3]:
        params['мечты'] -= 3

    # ------------
    # 9th question
    if proxy_dict['9th_question'] == answers[8][0]:
        params['просто вопрос'] += 3
    if proxy_dict['9th_question'] == answers[8][1]:
        params['просто вопрос'] -= 3
    if proxy_dict['9th_question'] == answers[8][2]:
        params['просто вопрос'] -= 1
    if proxy_dict['9th_question'] == answers[8][3]:
        params['просто вопрос'] += 1

    animals_with_stats = await get_all_animals_stats()

    glob_diff = {animal: 0 for animal in animals_with_stats.keys()}

    glob_diff_cnt = 0
    for tupl in animals_with_stats.values():
        diff = []
        tupl_cnt = 0

        for stat in params.values():
            cur_diff = stat - int(tupl[tupl_cnt])
            diff.append(abs(cur_diff))

            if tupl_cnt < len(tupl):
                tupl_cnt += 1

        glob_diff[list(glob_diff.keys())[glob_diff_cnt]] = sum(diff)

        if glob_diff_cnt < len(glob_diff.keys()):
            glob_diff_cnt += 1

    min_diff = min(glob_diff.values())
    best_animals = {key: value for key, value in glob_diff.items() if value == min_diff}

    if len(best_animals) == 1:
        totem_animal = list(best_animals.keys())[0]
    else:
        totem_animal = choice(list(best_animals.keys()))

    logging.info(f' {datetime.now()} :\n'
                 f'User with ID {user_id} and username = {username} '
                 f'got new totem animal = {totem_animal}')

    return totem_animal
