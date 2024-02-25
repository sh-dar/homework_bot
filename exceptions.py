class EndpointConnectionError(ConnectionError):
    """Исключение возникает при ошибке подключения к основному API."""

    def __init__(self, request_params):
        super().__init__(
            f'Ошибка подключения к основному API. '
            f'Параметры запроса: url = {request_params["url"]},\n'
            f'headers = {request_params["headers"]},\n'
            f'params = {request_params["params"]}'
        )


class EndpointResponseError(Exception):
    """Исключение возникает при неожиданном коде ответа основного API."""

    def __init__(self, response):
        super().__init__(
            f'Неожиданный ответ основного API. '
            f'Код ошибки: {response.status_code}\n'
            f'Причина: {response.reason}\n'
            f'Текст ошибки: {response.text}'
        )


class MissingKeyError(KeyError):
    """Исключение возникает, при отсутствии ключа homework_name."""

    def __init__(self, key):
        super().__init__(f'Ключ "{key}" отсутствует в ответе API')


class HomeworkStatusError(KeyError):
    """Исключение возникает, при неожиданном статусе."""

    def __init__(self, status):
        super().__init__(f'Неожиданный статус домашней работы - {status}')


class VariableError(KeyError):
    """Исключение возникает, при отсутствии переменной окружения."""

    def __init__(self):
        super().__init__('Отсутствует обязательная переменная окружения')
