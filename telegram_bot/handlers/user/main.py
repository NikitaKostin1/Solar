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
	Handle the "/start" command to start the bot and create a user.
	"""
	await message.answer(
		txt.start.format(first_name=message.from_user.first_name),
		reply_markup=reply.DATASET_OPTIONS
	)


@logger.catch
async def upload_dataset(message: Message):
	"""
	Handle uploading a dataset.
	"""
	await message.answer(
		txt.upload_dataset,
		reply_markup=reply.CANCEL
	)
	await DatasetState.download.set()


@logger.catch
async def choose_training_dataset(message: Message):
	"""
	Handle choosing a training dataset.
	"""
	datasets_files = util.get_neural_dataset_files()

	if not datasets_files:
		await message.answer(txt.no_files_uploaded)
	else:
		await message.answer(
			txt.select_dataset,
			reply_markup=inline.create_dataset_selection(datasets_files)
		)


@logger.catch
def register_users_handlers(dp: Dispatcher) -> None:
	dp.register_message_handler(start, commands=["start"], chat_type=ChatType.PRIVATE)
	dp.register_message_handler(upload_dataset, lambda message: message.text == "Download dataset 📄", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(choose_training_dataset, lambda message: message.text == "Choose dataset", chat_type=ChatType.PRIVATE)

	dp.register_message_handler(dataset.download, content_types=MessageContentType.DOCUMENT, state=DatasetState.download, chat_type=ChatType.PRIVATE)
	dp.register_message_handler(dataset.cancel_download, lambda message: message.text == "Cancel ❌", state=DatasetState.download, chat_type=ChatType.PRIVATE)

	dp.register_callback_query_handler(dataset.choose_for_training, lambda callback: callback.data.startswith("choose_dataset"), chat_type=ChatType.PRIVATE)
	dp.register_callback_query_handler(dataset.start_training, lambda callback: callback.data.startswith("start_training"), state=DatasetState.train, chat_type=ChatType.PRIVATE)
	dp.register_callback_query_handler(dataset.cancel_training, lambda callback: callback.data == "cancel_training", state=DatasetState.train, chat_type=ChatType.PRIVATE)
