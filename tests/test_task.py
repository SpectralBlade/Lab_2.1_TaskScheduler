import pytest
from src.classes.task import Task
from src.classes.exceptions import InvalidPriorityError, InvalidStatusError


def test_task_creation_success():
    """Проверка успешного создания задачи с валидными данными."""
    task = Task(id="1", description="Test", priority=50, status="IN_PROGRESS", payload="Data")

    assert task.id == "1"
    assert task.priority == 50
    assert task.status == "IN_PROGRESS"


def test_task_is_ready_property():
    """Проверка логики вычисляемого свойства @property is_ready."""
    task_ready = Task(id="1", description="Ready", priority=60, status="NEW")
    assert task_ready.is_ready is True

    task_low_prio = Task(id="2", description="Not ready", priority=40, status="NEW")
    assert task_low_prio.is_ready is False

    task_wrong_status = Task(id="3", description="Not ready 2", priority=90, status="IN_PROGRESS")
    assert task_wrong_status.is_ready is False


def test_priority_descriptor_validation():
    """Проверка выброса исключения при невалидном приоритете (Data Descriptor)."""
    with pytest.raises(InvalidPriorityError):
        Task(id="1", description="Test", priority=150)

    with pytest.raises(InvalidPriorityError):
        Task(id="2", description="Test", priority=0)

    with pytest.raises(InvalidPriorityError):
        Task(id="3", description="Test", priority="High")


def test_status_descriptor_validation():
    """Проверка выброса исключения при невалидном статусе (data дескриптор)."""
    with pytest.raises(InvalidStatusError):
        Task(id="1", description="Test", status="UNKNOWN_STATUS")

    with pytest.raises(InvalidStatusError):
        Task(id="2", description="Test", status=123)


def test_summary_non_data_descriptor():
    """Проверка генерации строки сводки через non-data дескриптор."""
    task = Task(id="1", description="Test", priority=1, status="NEW")
    expected = "[NEW] ID: 1 | Test (Priority: 1)"

    assert task.summary == expected


def test_summary_is_read_only():
    """Проверка защиты от записи из-за комбинации __slots__ и non-data дескриптора."""
    task = Task(id="1", description="Test", priority=1, status="NEW")

    with pytest.raises(AttributeError):
        task.summary = "Trying to override summary"