import importlib.util
import os
from typing import Any
from src.logging_tools.log_manager import LoggingManager
from src.classes.validator import TaskSourceValidator
from src.classes.queue import TaskQueue

class ConsoleInterface:
    """
    Класс для взаимодействия с пользователем через консоль.
    Реализует логику интерактивного меню, загрузку источников из файла,
    а также мгновенный парсинг и кэширование задач для просмотра.
    """
    def __init__(self):
        """
        Инициализирует консольный интерфейс.
        Создает экземпляр валидатора и словарь для хранения очередей задач.
        """
        self.validator = TaskSourceValidator()
        self.queues: dict[Any, TaskQueue] = {}

    def _handle_error(self, message: str) -> None:
        """
        Обрабатывает некоторые ошибки: записывает сообщение в лог и выводит его в консоль.
        :param message: Текст сообщения об ошибке.
        """
        LoggingManager.logger.error(message)
        print(message)

    def load_sources_from_file(self) -> bool:
        """
        Запрашивает у пользователя имя файла, загружает из него источники задач,
        валидирует их и производит сбор задач в логи и кэш.
        :return: True, если хотя бы один источник успешно загружен и валидирован, иначе False.
        """
        prompt = ("\nEnter filename (MUST contain list with sources named 'SOURCES' "
                  "\nand MUST be located at src/examples!!!) (for example, examples.py) or 'exit': ")

        while (filename := input(prompt).strip().lower()) != 'exit':
            module_name = filename[:-3] if filename.endswith('.py') else filename
            file_path = os.path.join("examples", f"{module_name}.py")

            if not os.path.exists(file_path):
                msg = f"File {file_path} not found."
                print(msg)
                LoggingManager.logger.error(msg)
                continue

            try:
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                sources_list = getattr(module, 'SOURCES', getattr(module, 'SOURCES', None))

                if sources_list is None:
                    self._handle_error("SOURCES list not found in the specified file.")

                for s in sources_list:
                    if self.validator.verify(s):
                        self.queues[s] = TaskQueue(s)

                if self.validator.validated_sources:
                    return True

                self._handle_error("No valid sources found in the specified file.")
            except Exception as e:
                self._handle_error(f"Error trying to parse {filename}: {e}")

        return False

    def _process_queue_interactive(self):
        """
        Интерактивное меню для работы с конкретной ленивой очередью.
        """
        sources = self.validator.validated_sources
        if not sources:
            print("No valid sources loaded.")
            return

        print("\n--- Select Source ---")
        for i, src in enumerate(sources, 1):
            print(f"{i} - {src.__class__.__name__}")

        if (idx_in := input("Enter number: ").strip()).isdigit():
            idx = int(idx_in) - 1
            if 0 <= idx < len(sources):
                src = sources[idx]
                queue = self.queues[src]

                print(f"\n--- Processing TaskQueue for {src.__class__.__name__} ---")
                print("1 - Iterate all tasks")
                print("2 - Filter by status (e.g., NEW, IN_PROGRESS)")
                print("3 - Filter by priority (>= value)")
                print("4 - Get 'ready' tasks")

                op = input("Choose operation: ").strip()

                gen = None
                if op == "1":
                    gen = iter(queue)
                elif op == "2":
                    st = input("Enter status: ").strip()
                    gen = queue.filter_by_status(st)
                elif op == "3":
                    try:
                        p = int(input("Enter min priority: ").strip())
                        gen = queue.filter_by_priority(p)
                    except ValueError:
                        print("Invalid priority.")
                        return
                elif op == "4":
                    gen = queue.get_ready_tasks()
                else:
                    print("Invalid operation.")
                    return

                print("\nResults:")
                for t in gen:
                    print(f"  {t.summary} | Payload: {t.payload}")
                return
        print("Input error.")

    def run_menu(self):
        """
        Запускает главный цикл интерактивного меню для работы с загруженными данными.
        Позволяет просматривать список источников и работать с их очередями.
        """
        menu_text = (
            "\n--- MENU ---"
            "\n1 - List of valid sources"
            "\n2 - Display tasks from all sources"
            "\n3 - Process specific source (filters & iteration)"
            "\n0 - Exit\n"
        )

        while (choice := input(f"{menu_text}Enter your choice: ").strip()) != "0":
            if choice == "1":
                for i, src in enumerate(self.validator.validated_sources, 1):
                    print(f"{i}. {src.__class__.__name__}")

            elif choice == "2":
                for src, queue in self.queues.items():
                    print(f"\nSource: {src.__class__.__name__}")
                    for t in queue:
                        print(f"  {t.summary}")

            elif choice == "3":
                self._process_queue_interactive()

            else:
                self._handle_error(f"Incorrect input: {choice}")