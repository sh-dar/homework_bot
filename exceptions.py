class EndpointUnavailableError(Exception):
    """Исключение возникает, при ошибке доступа к основному API."""

    def __init__(self, response):
        super().__init__(f'Эндпоинт недоступен:  {response.status_code}')


class KeyHomeworkNameError(KeyError):
    """Исключение возникает, при отсутствии ключа homework_name."""

    def __init__(self):
        super().__init__('Ключ "homework_name" отсутствует в ответе API')


class KeyStatusError(KeyError):
    """Исключение возникает, при отсутствии ключа status."""

    def __init__(self):
        super().__init__('Ключ "status" отсутствует в ответе API')


class StatusNotInVerdictsError(KeyError):
    """Исключение возникает, при неожиданном статусе."""

    def __init__(self):
        super().__init__('Ключ "status" отсутствует в словаре вердиктов')
