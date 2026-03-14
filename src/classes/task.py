from typing import Any

class Task:
    __slots__ = ('id', 'payload')

    def __init__(self, id: int | str, payload: Any):
        self.id = id
        self.payload = payload

    def __str__(self):
        return f'Task (id={self.id}, payload={self.payload})'