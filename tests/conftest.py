import pytest
from src.logging_tools.log_manager import LoggingManager
from src.classes.validator import TaskSourceValidator
from src.classes.task import Task

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    LoggingManager.setup()

class ValidSource:
    def get_tasks(self):
        return [sample_task]

class InvalidSource:
    def some_other_method(self):
        pass

@pytest.fixture
def validator() -> TaskSourceValidator:
    return TaskSourceValidator()


@pytest.fixture
def sample_task() -> Task:
    return Task(id="test-123", payload={"info": "test data"})


@pytest.fixture
def mock_valid_source(sample_task):
    return ValidSource()


@pytest.fixture
def mock_invalid_source():
    return InvalidSource()