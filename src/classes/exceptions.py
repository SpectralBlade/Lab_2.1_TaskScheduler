class TaskError(Exception):
    """Базовое исключение для всех ошибок, связанных с задачами."""
    pass

class InvalidPriorityError(TaskError):
    """Выбрасывается при попытке установить некорректный приоритет."""
    pass

class InvalidStatusError(TaskError):
    """Выбрасывается при попытке установить неизвестный статус задачи."""
    pass