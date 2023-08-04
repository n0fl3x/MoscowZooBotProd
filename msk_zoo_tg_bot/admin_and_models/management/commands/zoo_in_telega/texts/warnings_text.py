from admin_and_models.management.commands.zoo_in_telega.commands.quiz_commands import START_QUIZ_COMMAND
from admin_and_models.management.commands.zoo_in_telega.commands.static_commands import HELP_COMMAND


NOT_NONE_STATE_CANCEL_COMMAND_TEXT = f"""
Вы остановили опрос.
Если вы захотите вновь пройти его, то придётся начать сначала.
Для этого введите команду или нажмите /{START_QUIZ_COMMAND}\n
Для вывода всех доступных команд - /{HELP_COMMAND}
"""


NONE_STATE_CANCEL_COMMAND_TEXT = """
Вы ещё не приступили к новому опросу
"""


ALREADY_ANSWERED = f"""
Вы уже отвечали на этот вопрос
"""


ALREADY_FINISHED = f"""
Вы уже завершили этот опрос
"""
