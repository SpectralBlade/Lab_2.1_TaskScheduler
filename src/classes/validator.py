from typing import Any, List
from src.classes.contract import TaskSource
from src.classes.task import Task
from src.logging_tools.log_manager import LoggingManager

class TaskSourceValidator:
    def __init__(self):
        self.validated_sources: list[TaskSource] = []

    def verify(self, source: Any) -> bool:
        source_name = source.__class__.__name__

        if isinstance(source, TaskSource):
            LoggingManager.logger.info(f"Source '{source_name}' successfully validated against TaskSource protocol.")
            self.validated_sources.append(source)
            return True

        LoggingManager.logger.error(f"Source '{source_name}' failed validation.")
        return False

    def fetch_and_display(self, source: TaskSource) -> List[Task]:
        tasks = list(source.get_tasks())
        LoggingManager.logger.info(f"Source returned {len(tasks)} tasks:")

        for task in tasks:
            LoggingManager.logger.info(f"  -> [Task ID: {task.id}] Payload: {task.payload}")

        return tasks