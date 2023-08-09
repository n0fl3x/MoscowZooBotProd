from commands.static_commands import HELP_COMMAND
from commands.quiz_commands import (
    START_QUIZ_COMMAND,
    CANCEL_QUIZ_COMMAND,
)

from commands.feedback_commands import START_FEEDBACK_COMMAND


QUIZ_START_TEXT = f"""
Вы приступили к опросу на определение Вашего тотемного животного.

Если Вы хотите остановить опрос, введите или нажмите /{CANCEL_QUIZ_COMMAND} или просто воспользуйтесь кнопкой
"Остановить опрос" в конце любого из вопросов

Если Вы хотите перезапустить опрос, введите или нажмите /{START_QUIZ_COMMAND}
"""


QUIZ_COMPLETE_TEXT = f"""
Тест окончен.

Если Вы хотите повторить тест, введите команду или нажмите /{START_QUIZ_COMMAND}

Чтобы оставить отзыв о Вашем последнем результате опроса и о работе бота в целом,
введите команду или нажмите /{START_FEEDBACK_COMMAND}

Чтобы вывести список всех доступных команд, введите или нажмите /{HELP_COMMAND}
"""


QUIZ_STATE_CANCEL_COMMAND_TEXT = f"""
Вы остановили опрос.
Если вы захотите вновь пройти его, то придётся начать сначала.
Для этого введите команду или нажмите /{START_QUIZ_COMMAND}\n
Для вывода всех доступных команд - /{HELP_COMMAND}
"""


QUIZ_RESTART_TEXT = """
Вы начали опрос заново.
"""


QUIZ_CANCEL_NONE_STATE_TEXT = """
Вы ещё не приступили к новому опросу.
"""


QUIZ_ALREADY_ANSWERED_TEXT = """
Вы уже отвечали на этот вопрос.
"""


QUIZ_ALREADY_FINISHED_TEXT = """
Вы уже завершили этот опрос.
"""


QUIZ_CANCEL_FEEDBACK_STATE_TEXT = """
Вы сейчас оставляете отзыв, а не проходите опрос.
"""


FEEDBACK_CANCEL_FOR_NEW_QUIZ_TEXT = """
Вы передумали оставлять отзыв чтобы начать новый опрос.
"""
