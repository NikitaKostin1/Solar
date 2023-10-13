from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



DATASET_OPTIONS: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
DATASET_OPTIONS.add(KeyboardButton(text="Download dataset 📄"))
DATASET_OPTIONS.add(KeyboardButton(text="Choose dataset"))

CANCEL: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
CANCEL.add(KeyboardButton(text="Cancel ❌"))
