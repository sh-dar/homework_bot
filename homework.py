import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (
    EndpointUnavailableError,
    KeyHomeworkNameError,
    KeyStatusError,
    StatusNotInVerdictsError,
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
    required_variables = [
        PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    ]
    return all(required_variables)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
        )
        logging.debug(f'Сообщение "{message}" успешно отправлено')
    except telegram.error.NetworkError as error:
        logging.error(f'Ошибка сети: {error}')
    except telegram.error.TelegramError as error:
        logging.error(f'Сбой при отправке сообщения в Telegram: {error}')
    except Exception as error:
        logging.error(f'Неожиданная ошибка при отправке сообщения: {error}')


def get_api_answer(timestamp):
    """Отправляет запрос к эндпоинту API-сервиса."""
    params = {'from_date': timestamp}
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=params)
        if response.status_code != HTTPStatus.OK:
            raise EndpointUnavailableError(response)
        return response.json()
    except requests.RequestException as error:
        logging.error(error)


def check_response(response):
    """Проверяет ответ API на соответствие документации."""
    if not isinstance(response, dict):
        raise TypeError('Недопустимый тип ответа API.')
    if not isinstance(response.get('homeworks'), list):
        raise TypeError('Недопустимый тип данных ответа API.')
    required_keys = {'homeworks', 'current_date'}
    if not required_keys.issubset(response.keys()):
        raise KeyError('Отсутствие ожидаемых ключей в ответе API')
    return response.get('homeworks')


def parse_status(homework):
    """Извлекает из информации о конкретной домашней работе её статус."""
    homework_name = homework.get('homework_name')
    if homework_name is None:
        raise KeyHomeworkNameError()
    status = homework.get('status')
    if status is None:
        raise KeyStatusError()
    if status in HOMEWORK_VERDICTS:
        verdict = HOMEWORK_VERDICTS[status]
        return f'Изменился статус проверки работы "{homework_name}". {verdict}'
    else:
        raise StatusNotInVerdictsError()


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Отсутствие обязательной переменной окружения.')
        sys.exit('Ошибка проверки необходимых данных.')

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    timestamp = int(time.time())
    previous_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            homeworks = check_response(response)
            timestamp = response['current_date']
            if len(homeworks) == 0:
                message = 'Нет новых статусов'
            else:
                message = parse_status(homeworks[0])
            if message != previous_message:
                send_message(bot, message)
                previous_message = message

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.error(message)
            if message != previous_message:
                send_message(bot, message)
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
        format='%(asctime)s, %(levelname)s, %(message)s'
    )
    main()
