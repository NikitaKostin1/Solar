from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from telegram_bot.keyboards import reply, inline
from telegram_bot.entities.states import DatasetState
from telegram_bot.assets import text as txt

from . import util
from loguru import logger
import config
import os
import neural



@logger.catch
async def upload_menu(message: Message):
	"""
	Showing the upload menu.
	"""
	await message.answer(
		txt.upload_dataset,
		reply_markup=reply.CANCEL
	)
	await DatasetState.Upload.send_file.set()


@logger.catch
async def confirm_upload(message: Message, state: FSMContext):
	"""
	Confirmation of dataset upload and file processing.
	"""
	user_id = message.from_user.id
	file_name = message.document.file_name

	if not file_name.endswith(".txt"):
		await message.answer(txt.file_extension)
		return

	path = os.path.join(config.NEURAL_DATASETS_DIR, file_name)

	await message.document.download(destination_file=path)
	await message.answer(
		txt.download_successful.format(path=path),
		reply_markup=reply.DATASETS_MENU
	)
	await state.finish()


@logger.catch
async def cancel_upload(message: Message, state: FSMContext):
	"""
	Handle canceling the dataset download.
	"""
	await message.answer(
		txt.cancelled,
		reply_markup=reply.DATASETS_MENU
	)
	await state.finish()


@logger.catch
async def train_menu(message: Message):
	"""
	Show the training menu and list available datasets for training.
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
async def selected_dataset(callback: CallbackQuery):
	"""
	Handle the user's selection of a dataset for training.
	"""
	user_id = callback.message.from_user.id
	dataset_name = callback.data.split()[1]
	await callback.message.delete()

	await callback.message.answer(
		txt.selected_dataset.format(
			dataset_name=dataset_name
		),
		reply_markup=inline.create_confirm_training(dataset_name)
	)
	await DatasetState.Train.confirm_training.set()


@logger.catch
async def confirm_training(callback: CallbackQuery, state: FSMContext):
	"""
	Handle starting the training of a dataset.
	"""
	await state.finish()
	dataset_name = callback.data.split()[1]

	await callback.message.answer(
		txt.dataset_training_started.format(
			dataset_name=dataset_name
		),
		reply_markup=reply.DATASETS_MENU
	)

	await callback.message.edit_text(
		text=callback.message.text,
		reply_markup=None
	)
	neural.create_training_thread(dataset_name)


@logger.catch
async def cancel_training(callback: CallbackQuery, state: FSMContext):
	"""
	Handle canceling the training confirmation.
	"""
	await state.finish()

	await callback.message.answer(
		txt.cancelled,
		reply_markup=reply.DATASETS_MENU
	)
	await callback.message.edit_text(
		text=callback.message.text,
		reply_markup=None
	)
