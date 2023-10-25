from pyrogram import Client
from pyrogram.types import SentCode
from pyrogram.errors import (
	SessionPasswordNeeded, PhoneCodeInvalid,
	FloodWait, PhoneCodeExpired, PasswordHashInvalid
)

from aiogram import Bot
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from database import operations

from telegram_bot.entities.states import UserBotState
from telegram_bot.utils import Env, UserBotProcess
from telegram_bot.assets import text as txt
from telegram_bot.keyboards import reply

from typing import NoReturn
from datetime import timedelta
from contextlib import suppress
from loguru import logger



_connecting_sessions: dict[int, Client] = {}


@logger.catch
async def _activate_user_bot(user_id: int, bot: Bot) -> NoReturn:
	"""
	Activate a user's bot session, connecting the Pyrogram client and starting the bot.

	Args:
		user_id (int): The unique identifier of the user.
		bot (Bot): The Aiogram bot.

	Note:
		This function is not a handler. It is called only from other functions to start the user's bot session.
	"""
	client = _connecting_sessions[user_id]
	string_session: str = await client.export_session_string()

	if operations.get_user(user_id): 
		operations.create_user_bot_session(user_id, string_session)

	await client.disconnect()
	del _connecting_sessions[user_id]

	UserBotProcess.activate(user_id, string_session)

	await bot.send_message(
		user_id, txt.user_bot_started, reply_markup=reply.MAIN_MENU
	)


@logger.catch
async def connect(message: Message):
	"""
	Handle the user's request to connect to the bot session.

	Args:
		message (Message): The user's message.

	Note:
		This function handles the initial steps for connecting to the bot session.
	"""
	user_id = message.from_user.id

	user = operations.get_user(user_id)

	if UserBotProcess.is_active(user_id):
		await message.answer(txt.user_bot_is_running)
		operations.set_user_bot_session_condition(user_id, True)
		return

	if user.user_bot_session:
		UserBotProcess.activate(user_id)
		await message.answer(
			txt.user_bot_started, reply_markup=reply.MAIN_MENU
		)
	else:
		await message.answer(
			txt.connect, reply_markup=reply.REQUEST_CONTACT,
		)
		await UserBotState.Connect.phone_number.set()


@logger.catch
async def phone_number(message: Message, state: FSMContext):
	"""
	Handle the user's phone number input for connecting to the bot session.

	Args:
		message (Message): The user's message.
		state (FSMContext): The finite state machine context.

	Note:
		This function handles the phone number input step for connecting to the bot session.
	"""
	user_id = message.from_user.id
	phone_number = message.contact.phone_number

	client = Client(
		name=str(user_id),
		api_id=Env.API_ID,
		api_hash=Env.API_HASH,
		in_memory=True,
	)

	# Ignore already connected client exception
	with suppress(Exception):
		try:
			on_success = await client.connect()

		except AttributeError as e:
			await message.answer(
				str(e), reply_markup=reply.USER_BOT_MENU
			)
			await state.finish()
			return

	_connecting_sessions[user_id] = client

	try:
		sent_code: SentCode = await client.send_code(phone_number)

	except FloodWait as e:
		logger.warning(e)
		await message.answer(
			txt.pyrogram_flood_wait_error.format(
				wait_for=timedelta(seconds=e.value)
			),
			reply_markup=reply.USER_BOT_MENU
		)
		await state.finish()
		return

	async with state.proxy() as data:
		data['phone_number'] = phone_number
		data['sent_code'] = sent_code

	await message.answer(
		txt.auth_code_input, reply_markup=reply.CANCEL
	)
	
	await UserBotState.Connect.next()


@logger.catch
async def auth_code(message: Message, state: FSMContext):
	"""
	Handle the user's authentication code input for connecting to the bot session.

	Args:
		message (Message): The user's message.
		state (FSMContext): The finite state machine context.

	Note:
		This function handles the authentication code input step for connecting to the bot session.
	"""
	user_id = message.from_user.id
	sign_in_data = await state.get_data()
	# For some reason client.sign_in() accepts only this way auth code
	auth_code = "".join(message.text.split('-'))

	client: Client = _connecting_sessions[user_id]

	try:
		await client.sign_in(
			sign_in_data['phone_number'],
			sign_in_data['sent_code'].phone_code_hash,
			auth_code
		)

	except PhoneCodeInvalid as e:
		logger.error(e)
		await message.answer(
			txt.phone_code_invalid
		)
		return

	except PhoneCodeExpired as e:
		logger.error(e)
		await message.answer(
			txt.phone_code_expired, reply_markup=reply.USER_BOT_MENU
		)
		await state.finish()
		return

	except SessionPasswordNeeded as e:
		await message.answer(
			txt.session_password_input, reply_markup=reply.CANCEL
		)
		await UserBotState.Connect.next()
		return

	await state.finish()
	await _activate_user_bot(user_id, message.bot)


@logger.catch
async def two_fa_password(message: Message, state: FSMContext):
	"""
	Handle the two-factor authentication password input for connecting to the bot session.

	Args:
		message (Message): The user's message.
		state (FSMContext): The finite state machine context.

	Note:
		This function handles the two-factor authentication password input step for connecting to the bot session.
	"""
	user_id = message.from_user.id
	client: Client = _connecting_sessions[user_id]

	try:
		await client.check_password(password=message.text)
	except PasswordHashInvalid:
		await message.answer(txt.two_fa_password_invalid)
		return

	await state.finish()
	await _activate_user_bot(user_id, message.bot)



@logger.catch
async def disconnect(message: Message):
	"""
	Handle the user's request to disconnect from the bot session.

	Args:
		message (Message): The user's message.

	Note:
		This function handles the user's request to stop the bot session.
	"""
	user_id = message.from_user.id
	user = operations.get_user(user_id)

	if not UserBotProcess.is_active(user_id):
		await message.answer(txt.user_bot_is_not_running)
		operations.set_user_bot_session_condition(user_id, False)
		return

	if user.user_bot_session:
		UserBotProcess.deactivate(user_id)
		await message.answer(
			txt.user_bot_stopped, reply_markup=reply.MAIN_MENU
		)
