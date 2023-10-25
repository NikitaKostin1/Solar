from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database.models import register_models
from telegram_bot.handlers import register_all_handlers
from telegram_bot.utils import Env

from loguru import logger



async def on_start_up(dp: Dispatcher) -> None:
	logger.success('Bot started')
	register_models()
	register_all_handlers(dp)


def start_telegram_bot() -> None:
	bot = Bot(token=Env.TOKEN, parse_mode='HTML')
	dp = Dispatcher(bot, storage=MemoryStorage())
	executor.start_polling(dp, skip_updates=True, on_startup=on_start_up)
