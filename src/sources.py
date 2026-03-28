import json, time, random
from typing import Iterator
from src.classes.task import Task
from src.logging_tools.log_manager import LoggingManager


class GeneratorSource:
    """
    Источник задач, генерирующий данные случайным образом в заданном количестве.
    """
    def __init__(self, count: int):
        """
        Инициализирует генератор задач.
        :param count: Количество задач, которые необходимо создать.
        """
        self.count = count

    @LoggingManager.log_task_sources
    def get_tasks(self) -> Iterator[Task]:
        """
        Генерирует итератор объектов Task со случайными данными.
        :return: Итератор, возвращающий объекты Task.
        """
        statuses = ["NEW", "IN_PROGRESS", "COMPLETED"]
        for _ in range(self.count):
            task_id = f'Task_{_}'
            task_description = f'Auto-generated task №{_}'
            task_priority = random.randint(1, 100)
            task_status = random.choice(statuses)
            task_payload = {
                'time': time.time(),
                'msg': f'Custom random data for task #{_}'
            }

            yield Task(
                id=task_id,
                description=task_description,
                priority=task_priority,
                status=task_status,
                payload=task_payload
            )


class FileSource:
    """
    Источник задач, считывающий данные из JSON-файла.
    """
    def __init__(self, path: str):
        """
        Инициализирует файловый источник.
        :param path: Путь к JSON-файлу с данными задач.
        """
        self.path = path

    @LoggingManager.log_task_sources
    def get_tasks(self) -> list[Task]:
        """
        Считывает список задач из файла и преобразует их в объекты Task.
        :return: Список объектов Task (пустой список в случае ошибки чтения).
        """
        tasks = []
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for task in data:
                    tasks.append(Task(
                        id=task["id"],
                        description=task.get("description", "Standard task description here."),
                        priority=task.get("priority", 1),
                        status=task.get("status", "NEW"),
                        payload=task.get("payload")
                    ))
        except (json.JSONDecodeError, FileNotFoundError, PermissionError) as e:
            LoggingManager.logger.error(f'An error occured while parsing tasks from {self.path}: {e}')
        return tasks


class ApiSource:
    """
    Источник задач, имитирующий получение данных через внешний API.
    """
    def __init__(self, endpoint: str, retries: int):
        """
        Инициализирует бутафорный API-источник.
        :param endpoint: URL-адрес конечной точки API.
        :param retries: Количество попыток повторного подключения.
        """
        self.endpoint = endpoint
        self.retries = retries
        self.server_data = [
            {"id": "API_1", "description": "Reloading a server", "priority": 100, "status": "NEW",
             "payload": {"type": "Critical"}},
            {"id": "API_2", "description": "Update packets", "priority": 50, "status": "NEW",
             "payload": {"type": "Info"}},
            {"id": "API_3", "description": "Clearing cache", "priority": 10, "status": "NEW",
             "payload": {"type": "Warning"}},
        ]

    def simulate_server_delay(self):
        """
        Имитирует сетевую задержку при обращении к серверу.
        :return: Данная функция ничего не возвращает.
        """
        time.sleep(random.uniform(0.2, 1.5))

    @LoggingManager.log_task_sources
    def get_tasks(self) -> list[Task]:
        """
        Запрашивает данные из имитированного API и преобразует их в список задач.
        :return: Список полученных объектов Task.
        """
        LoggingManager.logger.info(f'Sending API request to {self.endpoint}...')
        self.simulate_server_delay()

        tasks = []
        for task_data in self.server_data:
            tasks.append(Task(
                id=task_data["id"],
                description=task_data["description"],
                priority=task_data.get("priority", 1),
                status=task_data.get("status", "NEW"),
                payload=task_data.get("payload")
            ))

        return tasks