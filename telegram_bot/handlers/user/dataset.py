from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from telegram_bot.keyboards import reply, inline
from telegram_bot.entities.states import DatasetState
from telegram_bot.entities.errors import TxtExtensionError
from telegram_bot.assets import text as txt

from loguru import logger
import config
import os
import neural



@logger.catch
async def download(message: Message, state: FSMContext):
	"""
	Handle downloading a dataset.
	"""
	user_id = message.from_user.id
	file_name = message.document.file_name

	if not file_name.endswith(".txt"):
		await message.answer(TxtExtensionError.message)
		return

	path = os.path.join(config.NEURAL_DATASETS_DIR, file_name)

	await message.document.download(destination_file=path)
	await message.answer(
		txt.download_successful.format(path=path),
		reply_markup=reply.DATASET_OPTIONS
	)
	await state.finish()


@logger.catch
async def cancel_download(message: Message, state: FSMContext):
	"""
	Handle canceling the dataset download.
	"""
	await message.answer(
		txt.cancelled,
		reply_markup=reply.DATASET_OPTIONS
	)
	await state.finish()


@logger.catch
async def choose_for_training(callback: CallbackQuery):
	"""
	Handle choosing a dataset for training.
	"""
	user_id = callback.message.from_user.id
	dataset_name = callback.data.split()[1]
	await callback.answer()
	await callback.message.delete()

	await callback.message.answer(
		txt.selected_dataset.format(
			dataset_name=dataset_name
		),
		reply_markup=inline.create_start_training(dataset_name)
	)
	await DatasetState.train.set()


@logger.catch
async def start_training(callback: CallbackQuery, state: FSMContext):
	"""
	Handle starting the training of a dataset.
	"""
	await state.finish()
	dataset_name = callback.data.split()[1]

	await callback.message.answer(
		txt.dataset_training_started.format(
			dataset_name=dataset_name
		),
		reply_markup=reply.DATASET_OPTIONS
	)

	await callback.message.edit_text(
		text=callback.message.text,
		reply_markup=None
	)
	neural.create_training_thread(dataset_name)


@logger.catch
async def cancel_training(callback: CallbackQuery, state: FSMContext):
	"""
	Handle canceling the training process.
	"""
	await state.finish()

	await callback.message.answer(
		txt.cancelled,
		reply_markup=reply.DATASET_OPTIONS
	)
	await callback.message.edit_text(
		text=callback.message.text,
		reply_markup=None
	)