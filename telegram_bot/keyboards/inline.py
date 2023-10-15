from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List
from loguru import logger



@logger.catch
def create_dataset_selection(datasets_files: List[str]) -> InlineKeyboardMarkup:
	"""
	Creates an InlineKeyboardMarkup for selecting a dataset.

	Args:
		datasets_files (List[str]): List of dataset file names.
	"""
	keyboard = InlineKeyboardMarkup(row_width=1)

	for file_name in datasets_files:
		dataset_name = file_name.replace(".txt", "")
		callback_data = f"choose_dataset {dataset_name}"
		keyboard.add(InlineKeyboardButton(text=dataset_name, callback_data=callback_data))

	return keyboard


@logger.catch
def create_confirm_training(dataset_name: str) -> InlineKeyboardMarkup:
	"""
	Creates an InlineKeyboardMarkup for starting the neural model training process.

	Args:
		dataset_name (str): Name of the dataset.
	"""
	keyboard = InlineKeyboardMarkup(row_width=1)
	start_button = InlineKeyboardButton(text="Start ✅", callback_data=f"confirm_training {dataset_name}")
	cancel_button = InlineKeyboardButton(text="Cancel ❌", callback_data="cancel_training")
	keyboard.add(start_button, cancel_button)

	return keyboard
