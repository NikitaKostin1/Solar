from aiogram import Dispatcher
from aiogram.types.message import ContentType as MessageContentType
from aiogram.types import InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import (
	Message, CallbackQuery, ChatType, ContentType
)

from database import operations

from telegram_bot.entities.states import (
	DatasetState, UserBotState
)
from telegram_bot.keyboards import reply, inline
from telegram_bot.assets import text as txt

from . import util
from . import dataset
from . import user_bot

from contextlib import suppress
from loguru import logger



@logger.catch
async def start(message: Message):
	"""
	"/start" command to start the bot.
	"""
	user_id = message.from_user.id
	username = str(message.from_user.username)

	user = operations.create_user(user_id, username)
	logger.info(user.user_bot_session)

	await message.answer(
		txt.start.format(
			first_name=message.from_user.first_name
		),
		reply_markup=reply.MAIN_MENU
	)


@logger.catch
async def user_bot_menu(message: Message):
	"""
	User bot menu command.
	"""
	await message.answer(
		txt.user_bot_menu, reply_markup=reply.USER_BOT_MENU,
	)


@logger.catch
async def datasets_menu(message: Message):
	"""
	Datasets menu command.
	"""
	await message.answer(
		txt.datasets_menu, reply_markup=reply.DATASETS_MENU,
	)


@logger.catch
async def back(message: Message):
	"""
	Back command to return to the main menu.
	"""
	await message.answer(
		txt.main_menu, reply_markup=reply.MAIN_MENU
	)


@logger.catch
async def cancel(message: Message, state: FSMContext):
	"""
	Cancel command to cancel the current operation and return to the main menu.
	"""
	await message.answer(
		txt.cancelled, reply_markup=reply.MAIN_MENU
	)
	await state.finish()


@logger.catch
async def callback_cancel(callback: CallbackQuery, state: FSMContext):
	"""
	Cancel command from a callback query to cancel the current operation and return to the main menu.
	"""
	with suppress(Exception):
		await callback.message.edit_text(
			text=callback.message.text,
			reply_markup=None
		)
	await callback.message.answer(
		txt.cancelled, reply_markup=reply.MAIN_MENU
	)
	await state.finish()


@logger.catch
def register_users_handlers(dp: Dispatcher) -> None:
	"""
	Register user message handlers with the dispatcher.
	"""
	dp.register_message_handler(start, commands=["start"], chat_type=ChatType.PRIVATE)
	dp.register_message_handler(user_bot_menu, lambda message: message.text == "User bot menu", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(datasets_menu, lambda message: message.text == "Datasets menu", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(back, lambda message: message.text == "Back ↩️", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(cancel, lambda message: message.text == "Cancel ❌", chat_type=ChatType.PRIVATE, state="*")
	dp.register_callback_query_handler(callback_cancel, lambda callback: callback.data == "cancel", chat_type=ChatType.PRIVATE, state="*")

	# Dataset region
	dp.register_message_handler(dataset.upload_menu, lambda message: message.text == "Upload dataset 📥", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(dataset.train_menu, lambda message: message.text == "Select dataset 📄", chat_type=ChatType.PRIVATE)

	dp.register_message_handler(dataset.confirm_upload, content_types=MessageContentType.DOCUMENT, state=DatasetState.Upload.send_file, chat_type=ChatType.PRIVATE)

	dp.register_callback_query_handler(dataset.selected_dataset, lambda callback: callback.data.startswith("choose_dataset"), chat_type=ChatType.PRIVATE)
	dp.register_callback_query_handler(dataset.confirm_training, lambda callback: callback.data.startswith("confirm_training"), state=DatasetState.Train.confirm_training, chat_type=ChatType.PRIVATE)

	# User bot region
	dp.register_message_handler(user_bot.connect, lambda message: message.text == "Connect 🟢", chat_type=ChatType.PRIVATE)
	dp.register_message_handler(user_bot.disconnect, lambda message: message.text == "Disconnect 🔴", chat_type=ChatType.PRIVATE)

	dp.register_message_handler(user_bot.phone_number, content_types=ContentType.CONTACT, state=UserBotState.Connect.phone_number)
	dp.register_message_handler(user_bot.auth_code, content_types=ContentType.TEXT, state=UserBotState.Connect.auth_code)
	dp.register_message_handler(user_bot.two_fa_password, content_types=ContentType.TEXT, state=UserBotState.Connect.two_fa_password)
