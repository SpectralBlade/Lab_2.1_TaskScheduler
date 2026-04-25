import pytest
from typing import Iterator
from src.classes.task import Task
from src.classes.queue import TaskQueue

class DummySource:
    """Источник-заглушка."""
    def get_tasks(self) -> Iterator[Task]:
        yield Task(id="1", description="Коллоквиум", priority=10, status="NEW")
        yield Task(id="2", description="Ассессмент", priority=90, status="NEW")
        yield Task(id="3", description="Контест", priority=50, status="IN_PROGRESS")
        yield Task(id="4", description="Экзамен", priority=100, status="COMPLETED")


@pytest.fixture
def queue():
    """Фикстура для инициализации очереди перед каждым тестом."""
    source = DummySource()
    return TaskQueue(source)

def test_queue_iteration_and_repeatability(queue):
    """Проверка протокола итерации и возможности повторного обхода."""
    tasks_first_pass = list(queue)
    assert len(tasks_first_pass) == 4

    tasks_second_pass = list(queue)
    assert len(tasks_second_pass) == 4


def test_lazy_evaluation_returns_generators(queue):
    """Проверка того, что фильтры возвращают генераторы, а не списки (ленивость)."""
    gen_status = queue.filter_by_status("NEW")
    gen_priority = queue.filter_by_priority(50)

    assert type(gen_status).__name__ == "generator"
    assert type(gen_priority).__name__ == "generator"


def test_filter_by_status(queue):
    """Проверка корректности ленивой фильтрации по статусу."""
    gen = queue.filter_by_status("new")
    tasks = list(gen)

    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[1].id == "2"


def test_filter_by_priority(queue):
    """Проверка корректности ленивой фильтрации по приоритету."""
    gen = queue.filter_by_priority(90)
    tasks = list(gen)

    assert len(tasks) == 2
    assert tasks[0].id == "2"
    assert tasks[1].id == "4"


def test_get_ready_tasks(queue):
    """Проверка фильтрации готовых задач (is_ready: status == NEW и priority > 50)."""
    gen = queue.get_ready_tasks()
    tasks = list(gen)

    assert len(tasks) == 1
    assert tasks[0].id == "2"


def test_builtins_compatibility(queue):
    """Проверка работы очереди со стандартными функциями Python (например, sum)."""
    total_priority = sum(task.priority for task in queue)
    assert total_priority == 250


def test_stop_iteration_handling(queue):
    """Проверка корректного истощения генератора и встроенной ошибки StopIteration."""
    gen = queue.filter_by_status("COMPLETED")

    task = next(gen)
    assert task.id == "4"

    with pytest.raises(StopIteration):
        next(gen)