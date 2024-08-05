# Homework Bot
Telegram-бот, оповещающий о статусе выполненной работы.

### Описание проекта:
Homework Bot - это Бот-ассистент, разработанный для взаимодействия с API сервиса Практикум.Домашка. Он проверяет статус вашей отправленной на ревью домашней работы и отправляет вам соответствующие уведомления в Telegram.
Реализован с помощью библиотеки python telegram bot.

Особенности:
- Регулярная проверка API: Бот опрашивает API сервиса Практикум.Домашка каждые 10 минут, чтобы проверить статус вашей отправленной домашней работы.
- Уведомления о статусе: Обнаружив изменения статуса вашей работы, бот анализирует ответ API и отправляет вам соответствующие уведомления через Telegram.
- Логирование и отчеты об ошибках: Бот ведет журнал своей работы и уведомляет вас о важных проблемах через сообщения в Telegram.

### Технологии:

- Python 3.7
- python-telegram-bot 13.7
- python-dotenv 0.19.0

### Запуск проекта:

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/sh-dar/homework_bot.git

cd homework_bot
```

2. Создать и активировать виртуальное окружение:

```
python -m venv venv 

source venv/bin/activate (Mac, Linux)
source venv/scripts/activate (Windows)
```

3. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip 

pip install -r requirements.txt
```

4. Создать файл `.env` в корневом каталоге проекта и добавить в него ваши переменные окружения:

```
PRACTICUM_TOKEN=your_practicum_token
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```
- Получить PRACTICUM_TOKEN для доступа к Домашке можно [по ссылке](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a).
- TELEGRAM_TOKEN выдаст @BotFather при создании бота
- TELEGRAM_CHAT_ID спросить у бота @userinfobot

5. Запустить бота:

```
python homework.py
```

### Автор
[Dari Sharapova - sh-dar](https://github.com/sh-dar)