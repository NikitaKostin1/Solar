from typing import Final
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


BACK_BTN: Final = KeyboardButton(text="Back ↩️")
CANCEL_BTN: Final = KeyboardButton(text="Cancel ❌")


MAIN_MENU: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
MAIN_MENU.add(KeyboardButton(text="User bot menu"))
MAIN_MENU.add(KeyboardButton(text="Datasets menu"))

USER_BOT_MENU: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
USER_BOT_MENU.add(KeyboardButton(text="Connect 🟢"))
USER_BOT_MENU.add(KeyboardButton(text="Disconnect 🔴"))
USER_BOT_MENU.add(BACK_BTN)

DATASETS_MENU: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
DATASETS_MENU.add(KeyboardButton(text="Upload dataset 📥"))
DATASETS_MENU.add(KeyboardButton(text="Select dataset 📄"))
DATASETS_MENU.add(BACK_BTN)

CANCEL: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
CANCEL.add(CANCEL_BTN)

REQUEST_CONTACT: Final = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
REQUEST_CONTACT.add(KeyboardButton("Send contact 📞", request_contact=True))
REQUEST_CONTACT.add(CANCEL_BTN)
