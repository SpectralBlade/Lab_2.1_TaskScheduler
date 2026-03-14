import importlib.util
import os
from src.logging_tools.log_manager import LoggingManager
from src.classes.validator import TaskSourceValidator

class ConsoleInterface:
    """
    Класс для взаимодействия с пользователем через консоль.
    Реализует логику интерактивного меню, загрузку источников из файла,
    а также мгновенный парсинг и кэширование задач для просмотра.
    """
    def __init__(self):
        """
        Инициализирует консольный интерфейс.
        Создает экземпляр валидатора и пустой словарик для хранения задач.
        """
        self.validator = TaskSourceValidator()
        self.tasks_cache = {}

    def _handle_error(self, message: str) -> None:
        """
        Обрабатывает некоторые ошибки: записывает сообщение в лог и выводит его в консоль.
        :param message: Текст сообщения об ошибке.
        :return: Данная функция ничего не возвращает.
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
                        tasks = self.validator.fetch_and_display(s)
                        self.tasks_cache[s] = tasks

                if self.validator.validated_sources:
                    return True

                self._handle_error("No valid sources found in the specified file.")
            except Exception as e:
                self._handle_error(f"Error trying to parse {filename}: {e}")

        return False

    def _display_cached_source(self):
        """
        Вспомогательный метод для выбора одного конкретного источника и вывода его задач.
        Использует данные из кэша, не инициируя новый процесс сбора задач.
        :return: Данная функция ничего не возвращает.
        """
        sources = self.validator.validated_sources
        for i, src in enumerate(sources, 1):
            print(f"{i} - {src.__class__.__name__}")

        if (idx_in := input("Enter number: ").strip()).isdigit():
            idx = int(idx_in) - 1
            if 0 <= idx < len(sources):
                src = sources[idx]
                tasks = self.tasks_cache.get(src, [])
                print(f"\nTasks {src.__class__.__name__}:")
                for t in tasks:
                    print(f"  {t}")
                return
        print("Input error.")

    def run_menu(self):
        """
        Запускает главный цикл интерактивного меню для работы с загруженными данными.
        Позволяет просматривать список источников и их задачи из кэша.
        :return: Данная функция ничего не возвращает.
        """
        menu_text = (
            "\n--- MENU ---"
            "\n1 - List of valid parsed sources"
            "\n2 - Tasks from all sources"
            "\n3 - Tasks from a specific source"
            "\n0 - Exit\n"
        )

        while (choice := input(f"{menu_text}Enter your choice: ").strip()) != "0":
            if choice == "1":
                for i, src in enumerate(self.validator.validated_sources, 1):
                    print(f"{i}. {src.__class__.__name__}")

            elif choice == "2":
                for src, tasks in self.tasks_cache.items():
                    print(f"\nSource: {src.__class__.__name__}")
                    for t in tasks:
                        print(f"  {t}")

            elif choice == "3":
                self._display_cached_source()

            else:
                self._handle_error(f"Incorrect input: {choice}")