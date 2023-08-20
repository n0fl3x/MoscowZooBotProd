from aiogram.dispatcher.filters.state import StatesGroup, State


class Feedback(StatesGroup):
    """Класс для фиксации состояния ожидания отзыва от пользователя."""

    feedback = State()
