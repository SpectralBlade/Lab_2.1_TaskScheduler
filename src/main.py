from src.logging_tools.log_manager import LoggingManager
from src.cli import ConsoleInterface


def main() -> None:
    """
    Основная функция запуска приложения.
    Инициализирует логи и запускает консольный интерфейс.
    """
    LoggingManager.setup()
    ui = ConsoleInterface()

    if ui.load_sources_from_file():
        ui.run_menu()

    LoggingManager.logger.info("Application closed.")

if __name__ == '__main__':
    main()