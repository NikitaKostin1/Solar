from user_bot.handlers.common import get_common_handlers
from pyrogram import Client

from typing import NoReturn



def register_all_handlers(client: Client) -> NoReturn:
	"""
	Register all Pyrogram event handlers for the user bot.

	Args:
		client (Client): The Pyrogram client to which the handlers will be added.
	"""
	handlers = (
		*get_common_handlers(),
	)
	for handler in handlers:
		client.add_handler(handler)
