import json, time, random
from typing import Iterator
from src.classes.task import Task
from src.logging_tools.log_manager import LoggingManager


class GeneratorSource:
    def __init__(self, count: int):
        self.count = count

    @LoggingManager.log_task_sources
    def get_tasks(self) -> Iterator[Task]:
        for _ in range(self.count):
            task_id = f'Task_{_}'
            task_payload = {
                'time': time.time(),
                'priority': random.randint(1, 100),
                'msg': f'Custom random data for task #{_}'
            }

            yield Task(id=task_id, payload=task_payload)


class FileSource:
    def __init__(self, path: str):
        self.path = path

    @LoggingManager.log_task_sources
    def get_tasks(self) -> list[Task]:
        tasks = []
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
                for task in data:
                    tasks.append(Task(id=task["id"], payload=task["payload"]))
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            LoggingManager.logger.error(f'An error occured while parsing tasks from {self.path}: {e}')
        return tasks


class ApiSource:
    def __init__(self, endpoint: str, retries: int):
        self.endpoint = endpoint
        self.retries = retries
        self.server_data = [
            {"id": "API_1", "payload": {"type": "Critical", "msg": "System Reboot"}},
            {"id": "API_2", "payload": {"type": "Info", "msg": "Update Available"}},
            {"id": "API_3", "payload": {"type": "Warning", "msg": "Low Disk Space"}},
        ]

    def simulate_server_delay(self):
        time.sleep(random.uniform(0.2, 1.5))

    @LoggingManager.log_task_sources
    def get_tasks(self) -> list[Task]:
        LoggingManager.logger.info(f'Sending API request to {self.endpoint}...')
        self.simulate_server_delay()

        tasks = []
        for task in self.server_data:
            task = Task(id=task["id"], payload=task["payload"])
            tasks.append(task)

        return tasks