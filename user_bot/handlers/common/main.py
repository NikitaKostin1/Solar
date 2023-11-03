from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import Client, filters

from typing import Tuple 
from loguru import logger



@logger.catch
async def echo(client: Client, message: Message):
	"""
	Duplicates text message in the Saved messages

	Args:
		client (Client): The Pyrogram client.
		message (Message): The incoming message.
	"""
	await message.reply(message.text)


@logger.catch
def get_common_handlers() -> Tuple[MessageHandler]:
	"""
	Get a set of common Pyrogram message handlers for the user bot.

	Returns:
		Tuple[MessageHandler]: A tuple of common message handlers.
	"""
	return (
		MessageHandler(echo, filters=filters.chat("me") & filters.incoming & filters.private),
	)
