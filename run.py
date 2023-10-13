#!/usr/bin/python
from loguru import logger
from misc.path import PathManager
from telegram_bot import start_telegram_bot

import config



def main():
	log_path = PathManager.get(config.LOGS_DIR)
	logger.add(
		log_path, format="{time} {level} {message}",
		level="DEBUG", rotation="1 MB", compression="zip"
	)
	start_telegram_bot()


if __name__ == "__main__":
	main()
