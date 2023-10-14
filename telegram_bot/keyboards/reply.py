from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



DATASETS_MENU: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
DATASETS_MENU.add(KeyboardButton(text="Upload dataset 📥"))
DATASETS_MENU.add(KeyboardButton(text="Choose dataset 📄"))

CANCEL: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
CANCEL.add(KeyboardButton(text="Cancel ❌"))
