import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (
    EndpointConnectionError,
    EndpointResponseError,
    HomeworkStatusError,
    MissingKeyError,
    VariableError,
)

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_VERDICTS = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


def check_tokens():
    """Проверяет доступность переменных окружения."""
    required_variables = (
        ("PRACTICUM_TOKEN", PRACTICUM_TOKEN),
        ("TELEGRAM_TOKEN", TELEGRAM_TOKEN),
        ("TELEGRAM_CHAT_ID", TELEGRAM_CHAT_ID)
    )
    for name, token in required_variables:
        if not token:
            logging.critical(
                f'Отсутствие обязательной переменной окружения: {name}.'
            )
            raise VariableError('Ошибка проверки необходимых данных.')


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        logging.debug(f'Попытка отправки cообщения "{message}".')
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        logging.debug(f'Сообщение "{message}" успешно отправлено')
        return True
    except telegram.error.NetworkError as error:
        logging.error(f'Ошибка сети: {error}')
        return False
    except telegram.error.TelegramError as error:
        logging.error(f'Сбой при отправке сообщения в Telegram: {error}')
        return False
    except Exception as error:
        logging.error(f'Неожиданная ошибка при отправке сообщения: {error}')
        return False


def get_api_answer(timestamp):
    """Отправляет запрос к эндпоинту API-сервиса."""
    request_params = {
        'url': ENDPOINT,
        'headers': HEADERS,
        'params': {'from_date': timestamp},
    }
    logging.debug(
        'Начало запроса к API со следующими параметрами: '
        'URL: {url}, headers: {headers}, params: {params}.'
        .format(**request_params)
    )
    try:
        response = requests.get(**request_params)
    except Exception:
        raise EndpointConnectionError(**request_params)
    if response.status_code != HTTPStatus.OK:
        raise EndpointResponseError(response)
    return response.json()


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Недопустимый тип ответа API.')
    homeworks = response.get('homeworks')
    if not isinstance(homeworks, list):
        raise TypeError('Недопустимый тип данных ответа API.')
    if 'homeworks' not in response.keys():
        raise KeyError('Отсутствие ожидаемых ключей в ответе API')
    return homeworks


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе её статус."""
    required_keys = {'homework_name', 'status'}
    for key in required_keys:
        if key not in homework:
            raise MissingKeyError(key)
    homework_name = homework['homework_name']
    status = homework['status']
    if status not in HOMEWORK_VERDICTS:
        raise HomeworkStatusError(status)
    verdict = HOMEWORK_VERDICTS[status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def main():
    """Основная логика работы бота."""
    check_tokens()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    previous_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            current_timestamp = response.get('current_date', timestamp)
            if not homeworks:
                message = 'Нет новых статусов'
            else:
                message = parse_status(homeworks[0])
            if message != previous_message and send_message(bot, message):
                timestamp = current_timestamp
                previous_message = message

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message, exc_info=True)
            if message != previous_message and send_message(bot, message):
                previous_message = message

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[
            logging.FileHandler(
                os.path.abspath('main.log'), mode='a', encoding='UTF-8'),
            logging.StreamHandler(stream=sys.stdout)],
        format=(
            '%(asctime)s - %(levelname)s - %(pathname)s - '
            '%(filename)s - %(lineno)d - %(message)s'
        )
    )
    main()
