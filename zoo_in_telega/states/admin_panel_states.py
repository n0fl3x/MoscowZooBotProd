from aiogram.dispatcher.filters.state import StatesGroup, State


class AdminAuthorization(StatesGroup):
    """Класс для фиксации состояния режима администратора."""

    TRUE = State()
