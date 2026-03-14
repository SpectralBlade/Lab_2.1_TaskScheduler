from typing import Protocol, Iterable, runtime_checkable
from src.classes.task import Task

@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол (интерфейс) для источников задач.
    Определяет контракт, которому должны соответствовать все классы-источники
    для успешной валидации и работы в системе.
    """
    def get_tasks(self) -> Iterable[Task]:
        """
        Абстрактный метод для получения итератора или списка объектов Task.
        :return: Итерируемый объект, содержащий экземпляры Task.
        """
        ...