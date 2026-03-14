from typing import Any

class Task:
    """
    Класс, представляющий модель отдельной задачи в системе.
    Использует __slots__ для оптимизации памяти.
    """
    __slots__ = ('id', 'payload')

    def __init__(self, id: int | str, payload: Any):
        """
        Инициализирует объект задачи.
        :param id: Уникальный идентификатор задачи (число или строка).
        :param payload: Полезная нагрузка задачи, содержащая произвольные данные. (например строчка, словарь)
        """
        self.id = id
        self.payload = payload

    def __str__(self) -> str:
        """
        Возвращает строковое представление объекта задачи.
        :return: Строка с ID и данными задачи.
        """
        return f'Task (id={self.id}, payload={self.payload})'