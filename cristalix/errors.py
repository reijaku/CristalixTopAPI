class CristalixError(Exception):
    """Базовая ошибка библиотеки."""
    pass


class Unauthorized(CristalixError):
    """Неверный токен или project_key."""
    pass


class NotFound(CristalixError):
    """Ресурс не найден."""
    pass


class ApiError(CristalixError):
    """Любая другая ошибка API."""
    pass
