import json
from src.sources import GeneratorSource, FileSource, ApiSource
from src.classes.task import Task


def test_generator_source_count():
    count = 10
    source = GeneratorSource(count=count)
    tasks = list(source.get_tasks())

    assert len(tasks) == count
    assert all(isinstance(t, Task) for t in tasks)
    assert tasks[0].id == 'Task_0'
    assert tasks[0]._description == 'Auto-generated task №0'


def test_file_source_success(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    file_path = d / "test_tasks.json"

    test_data = [
        {"id": "file_1", "payload": "data_1"},
        {"id": "file_2", "description": "Basic task example", "priority": 99, "status": "COMPLETED", "payload": "data_2"}
    ]
    file_path.write_text(json.dumps(test_data))

    source = FileSource(str(file_path))
    tasks = source.get_tasks()

    assert len(tasks) == 2

    assert tasks[0].id == "file_1"
    assert tasks[0]._description == "Standard task description here."
    assert tasks[0].priority == 1
    assert tasks[0].status == "NEW"

    assert tasks[1].id == "file_2"
    assert tasks[1]._description == "Basic task example"
    assert tasks[1].priority == 99
    assert tasks[1].status == "COMPLETED"


def test_file_source_not_found():
    source = FileSource("non_existent_file.json")
    tasks = source.get_tasks()
    assert tasks == []


def test_api_source_retrieval():
    source = ApiSource(endpoint="http://fake-api.com", retries=3)
    tasks = source.get_tasks()

    assert len(tasks) == 3
    assert tasks[0].id == "API_1"
    assert isinstance(tasks[0], Task)