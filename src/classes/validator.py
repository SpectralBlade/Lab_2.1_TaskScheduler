from typing import Any, List
from src.classes.contract import TaskSource
from src.classes.task import Task
from src.logging_tools.log_manager import LoggingManager

class TaskSourceValidator:
    """
    Класс для проверки и управления источниками задач.
    Отвечает за проверку объектов на соответствие протоколу TaskSource.
    """
    def __init__(self):
        """
        Инициализирует валидатор с пустым списком проверенных источников.
        """
        self.validated_sources: list[TaskSource] = []

    def verify(self, source: Any) -> bool:
        """
        Проверяет, соответствует ли переданный объект интерфейсу TaskSource.
        :param source: Объект, который необходимо проверить.
        :return: True, если объект валиден, иначе False.
        """
        source_name = source.__class__.__name__

        if isinstance(source, TaskSource):
            LoggingManager.logger.info(f"Source '{source_name}' successfully validated against TaskSource protocol.")
            self.validated_sources.append(source)
            return True

        LoggingManager.logger.error(f"Source '{source_name}' failed validation.")
        return False

    def fetch_and_display(self, source: TaskSource) -> List[Task]:
        """
        Получает задачи из источника и выводит информацию о них в лог.
        :param source: Валидный источник задач, поддерживающий метод get_tasks.
        :return: Список полученных объектов Task.
        """
        tasks = list(source.get_tasks())
        LoggingManager.logger.info(f"Source returned {len(tasks)} tasks:")

        for task in tasks:
            LoggingManager.logger.info(f"  -> {task.summary} | Payload: {task.payload}")

        return tasks