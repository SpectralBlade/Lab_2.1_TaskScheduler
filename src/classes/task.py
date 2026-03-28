import time
from typing import Any
from src.classes.descriptors import PriorityDescriptor, StatusDescriptor, TaskSummary

class Task:
    """
    Класс, представляющий модель отдельной задачи в системе.
    Использует __slots__ для оптимизации памяти.
    """
    priority: int = PriorityDescriptor()
    status: str = StatusDescriptor()
    summary: str = TaskSummary()

    __slots__ = ('_id', '_description', '_priority', '_status', '_created_at', 'payload')

    def __init__(self, id: int | str, description: str, priority: int = 1, status: str = "NEW", payload: Any = None):
        self._id = id
        self._description = description
        self.priority = priority
        self.status = status
        self._created_at = time.time()
        self.payload = payload

    @property
    def is_ready(self) -> bool:
        """
        Вычисляемое свойство: проверяет, готова ли задача к выполнению.
        Как пример: пусть задача готова, если у нее статус новой и приоритет больше 50.
        """
        return self._status == "NEW" and self.priority > 50

    @property
    def id(self) -> int | str:
        """Свойство для ID."""
        return self._id

    def __str__(self) -> str:
        return f'Task(id={self._id}, status={self._status}, priority={self.priority})'