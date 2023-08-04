from admin_and_models.management.commands.zoo_in_telega.commands.static_commands import HELP_COMMAND
from admin_and_models.management.commands.zoo_in_telega.commands.quiz_commands import START_QUIZ_COMMAND, CANCEL_COMMAND


START_QUIZ_TEXT = f"""
Вы приступили к опросу на определение Вашего тотемного животного.

Если Вы хотите остановить опрос, введите или нажмите /{CANCEL_COMMAND} или просто воспользуйтесь кнопкой
"Остановить опрос" в конце любого из вопросов

Если Вы хотите перезапустить опрос, введите или нажмите /{START_QUIZ_COMMAND}
"""


QUESTION_1 = """
Какой стихией Вы хотели бы управлять?
"""


QUESTION_2 = """
Чем бы Вы предпочли перекусить?
"""


QUESTION_3 = """
Какое Ваше любимое время дня?
"""


QUESTION_4 = """
Какой у Вас характер?
"""


QUESTION_5 = """
Какая погода Вам больше по-душе?
"""


END_MESSAGE = f"""
Тест окончен.

Если Вы хотите повторить тест, введите команду или нажмите /{START_QUIZ_COMMAND}

Чтобы вывести список всех доступных команд, введите или нажмите /{HELP_COMMAND}
"""
