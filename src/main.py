from src.logging_tools.log_manager import LoggingManager
from src.classes.validator import TaskSourceValidator
from examples.examples import EXAMPLE_SOURCES

def main() -> None:
    LoggingManager.setup()

    LoggingManager.logger.info("Application started. Preparing to validate sources...")

    validator = TaskSourceValidator()

    LoggingManager.logger.info(f"Found {len(EXAMPLE_SOURCES)} sources in configuration. Starting validation...")

    for source in EXAMPLE_SOURCES:
        validator.verify(source)

    if not validator.validated_sources:
        LoggingManager.logger.warning("No valid task sources found. Exiting.")
        return

    LoggingManager.logger.info(f"Validation complete. {len(validator.validated_sources)} sources are ready for work.")

    for source in validator.validated_sources:
        try:
            validator.fetch_and_display(source)
        except Exception as e:
            LoggingManager.logger.error(f"Critical error while fetching tasks from {source.__class__.__name__}: {e}")

    LoggingManager.logger.info("Application finished its work successfully.")


if __name__ == '__main__':
    main()