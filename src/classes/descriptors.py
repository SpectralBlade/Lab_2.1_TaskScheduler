from src.classes.exceptions import InvalidPriorityError, InvalidStatusError


class PriorityDescriptor:
    """Data дескриптор для управления приоритетом задачи (от 1 до 100)."""

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, int) or not (1 <= value <= 100):
            raise InvalidPriorityError(f"Priority must be a whole number from 1 to 100. Received: {value}")
        setattr(obj, self.private_name, value)

class StatusDescriptor:
    """Data дескриптор для управления статусом задачи."""

    ALLOWED_STATUSES = {'NEW', 'IN_PROGRESS', 'FAILED', 'CANCELLED', 'COMPLETED'}

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise InvalidStatusError(f"Status must be a string. Received: {value}")

        normalized_status = value.upper()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise InvalidStatusError(f"Status must be one of {self.ALLOWED_STATUSES}. Received: {value}")

        setattr(obj, self.private_name, value)


class TaskSummary:
    """
    Non-data дескриптор для генерации сводки по задаче.
    """

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        return f"[{obj.status}] ID: {obj._id} | {obj._description} (Priority: {obj.priority})"