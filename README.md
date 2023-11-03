# Solar Telegram Bot

This Python project features a Telegram bot that allows you to run a chatbot on your local machine. With the bot, you can upload Russian language text datasets and fine-tune a language model using them.
The result is a finetuned model that can be used for various natural language processing tasks.
Additionally, you have the ability to connect your user bot. This user bot can replicate text messages in your saved messages and provides options to manage its connection.


--------

## Tech Stack 💻

- **Languages:**
	- Python 3.10
- **Telegram:**
	- [Aiogram](https://docs.aiogram.dev/en/latest/)
	- [Pyrogram](https://docs.pyrogram.org/)
- **Database:**
	- Sqlite3
	- [Sqlalchemy](https://docs.sqlalchemy.org/en/14/)
- **Neural training:**
	- [Transformers\[torch\]](https://huggingface.co/docs/transformers/index)
- **Debug:**
	- Loguru

--------

## QUICK_START 💾

1. Clone project
2. Create a virtual venv
3. Install requirements:
	```
 	pip install --upgrade pip
 	pip install -r requirements.txt
 	```
4. Setup environment variables:
	- [TOKEN](https://telegram.me/BotFather)
	- [API_HASH](https://my.telegram.org/)
	- [API_ID](https://my.telegram.org/)

5. Run 
	```
	python run.py
	```

--------
