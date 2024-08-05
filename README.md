# Homework Bot
Telegram bot that checks the status of homework assignments via the Practicum by Yandex API and notifies the user of any updates. 

### Project description:
Homework Bot is a Bot-assistant, developed to interact with the API of the Praktikum.Domashka service. It checks the status of your homework submitted for review and sends you corresponding notifications in Telegram.
Implemented using the python telegram bot library.

Features:
- Regular API check: The bot polls the API of the Praktikum.Domashka service every 10 minutes to check the status of your submitted homework.
- Status notifications: the bot analyzes the API response and sends you corresponding notifications via Telegram.
- Logging and error reporting: The bot keeps a log of its operations and notifies you about important issues via Telegram messages.

### Technologies:

- Python 3.7
- python-telegram-bot 13.7
- python-dotenv 0.19.0

### Launching the project:

1. Clone the repository:

```
git clone https://github.com/sh-dar/homework_bot.git

cd homework_bot
```

2. Create and activate a virtual environment:

```
python -m venv venv

source venv/bin/activate (Mac, Linux)
source venv/scripts/activate (Windows)
```

3. Install dependencies from the requirements.txt file:

```
python -m pip install --upgrade pip

pip install -r requirements.txt
```

4. Create an `.env` file in the root directory of the project and add your environment variables:

```
PRACTICUM_TOKEN=your_practicum_token
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```
- Obtain the PRACTICUM_TOKEN for accessing Homework from [this link](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a).
- You will receive the TELEGRAM_TOKEN from @BotFather when creating the bot.
- Ask the bot @userinfobot for your TELEGRAM_CHAT_ID.

5. Run the bot:

```
python homework.py
```

### Author
[Dari Sharapova - sh-dar](https://github.com/sh-dar)