from aiogram import Dispatcher
from aiogram.types import Message, ChatType, ContentType
from aiogram.types.message import ContentType as MessageContentType
from aiogram.types import InlineKeyboardButton

from telegram_bot.entities.states import DatasetState
from telegram_bot.keyboards import reply, inline
from telegram_bot.assets import text as txt

from loguru import logger
from . import util
from . import dataset



@logger.catch
async def start(message: Message):
	"""
	Handle the "/start" command to start the bot.
	"""
	await message.answer(
		txt.start.format(
			first_name=message.from_user.first_name
		),
		reply_markup=reply.DATASETS_MENU
	)


@logger.catch
def register_users_handlers(dp: Dispatcher) -> None:
	"""
	Register user message handlers with the dispatcher.
	"""
	dp.register_message_handler(start, commands=["start"], chat_type=ChatType.PRIVATE)

	# Dataset region
	dp.register_message_handler(dataset.upload_menu, lambda message: message.text == "Upload dataset 📥", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(dataset.train_menu, lambda message: message.text == "Choose dataset 📄", chat_type=ChatType.PRIVATE)

	dp.register_message_handler(dataset.confirm_upload, content_types=MessageContentType.DOCUMENT, state=DatasetState.Upload.send_file, chat_type=ChatType.PRIVATE)
	dp.register_message_handler(dataset.cancel_upload, lambda message: message.text == "Cancel ❌", state=DatasetState.Upload.send_file, chat_type=ChatType.PRIVATE)

	dp.register_callback_query_handler(dataset.selected_dataset, lambda callback: callback.data.startswith("choose_dataset"), chat_type=ChatType.PRIVATE)
	dp.register_callback_query_handler(dataset.confirm_training, lambda callback: callback.data.startswith("confirm_training"), state=DatasetState.Train.confirm_training, chat_type=ChatType.PRIVATE)
	dp.register_callback_query_handler(dataset.cancel_training, lambda callback: callback.data == "cancel_training", state=DatasetState.Train.confirm_training, chat_type=ChatType.PRIVATE)
