# Homework Bot
Telegram-бот, оповещающий о статусе выполненной работы.

### Описание проекта:
Homework Bot - это Бот-ассистент, разработанный для взаимодействия с API сервиса Практикум.Домашка. Он проверяет статус вашей отправленной на ревью домашней работы и отправляет вам соответствующие уведомления в Telegram.
Реализован с помощью библиотеки python telegram bot.

Особенности
- Регулярная проверка API: Бот опрашивает API сервиса Практикум.Домашка каждые 10 минут, чтобы проверить статус вашей отправленной домашней работы.
- Уведомления о статусе: Обнаружив изменения статуса вашей работы, бот анализирует ответ API и отправляет вам соответствующие уведомления через Telegram.
- Логирование и отчеты об ошибках: Бот ведет журнал своей работы и уведомляет вас о важных проблемах через сообщения в Telegram.

### Технологии:

Python, Git

### Запуск проекта:

- Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/sh-dar/homework_bot.git

cd homework_bot
```

- Создать и активировать виртуальное окружение:

```
python -m venv venv 

source venv/bin/activate (Mac, Linux)
source venv/scripts/activate (Windows)
```

- Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip 

pip install -r requirements.txt
```

- Файл example.env переименовать в .env и заполнить своими данными. 
1. Получить PRACTICUM_TOKEN для доступа к Домашке можно по ссылке https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a 
2. TELEGRAM_TOKEN выдаст @BotFather при создании бота
3. TELEGRAM_CHAT_ID спросить у бота @userinfobot
```
PRACTICUM_TOKEN='token'
TELEGRAM_TOKEN='token'
TELEGRAM_CHAT_ID=<your chat id>
```

- Запустить бота:

```
python homework.py
```

### Автор
[Dari Sharapova - sh-dar](https://github.com/sh-dar)
