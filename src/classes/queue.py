from typing import Generator
from src.classes.task import Task
from src.classes.contract import TaskSource


class TaskQueueIterator:
    """
    Итератор для обхода TaskQueue.
    Реализует кэширование для поддержки повторных проходов.
    """
    def __init__(self, queue: 'TaskQueue'):
        self._queue = queue
        self._cursor = 0

    def __iter__(self):
        return self

    def __next__(self) -> Task:
        """
        Основная логика ленивого обхода и кэширования.
        """
        if self._cursor < len(self._queue._queue_cache):
            task = self._queue._queue_cache[self._cursor]
            self._cursor += 1
            return task

        if not self._queue._is_exhausted:
            try:
                task = next(self._queue._source_iterator)
                self._queue._queue_cache.append(task)
                self._cursor += 1
                return task
            except StopIteration:
                self._queue._is_exhausted = True
                raise StopIteration

        raise StopIteration


class TaskQueue:
    """
    Очередь задач, поддерживающая ленивую итерацию и фильтрацию.
    """
    def __init__(self, source: TaskSource):
        self._source = source
        self._source_iterator = iter(self._source.get_tasks())

        self._queue_cache: list[Task] = []
        self._is_exhausted: bool = False

    def __iter__(self) -> TaskQueueIterator:
        """
        Реализует протокол итерации.
        Возвращает пользовательский класс итератора.
        """
        return TaskQueueIterator(self)

    def filter_by_status(self, target_status: str) -> Generator[Task, None, None]:
        """
        Фильтрует задачи по заданному статусу.
        """
        target_status = target_status.upper()
        return (task for task in self if task.status == target_status)

    def filter_by_priority(self, min_priority: int) -> Generator[Task, None, None]:
        """
        Отбирает задачи, приоритет которых больше или равен заданному.
        """
        return (task for task in self if task.priority >= min_priority)

    def get_ready_tasks(self) -> Generator[Task, None, None]:
        """
        Отбирает задачи, готовые к выполнению (использует свойство is_ready).
        """
        return (task for task in self if task.is_ready)