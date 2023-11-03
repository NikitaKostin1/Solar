from user_bot.handlers import register_all_handlers

from loguru import logger
from pyrogram import Client
import sys

from typing import NoReturn



@logger.catch
def start_user_bot() -> NoReturn:
	"""
	Start the user bot process with the provided Pyrogram session and user ID.

	Note:
		This function initializes and runs the user bot using the provided session and user ID.
		It also registers all the Pyrogram handlers for the user bot.

	Raises:
		No specific exceptions are raised, but it logs errors for missing command-line arguments.
	"""
	try:
		string_session = sys.argv[1]
		user_id = sys.argv[2]
	except IndexError:
		logger.error("""Please provide the required command-line arguments: <string_session> <user_id>""")
		logger.error("It seems you are trying to run 'run_user_bot.py', but you should use 'run.py' instead.")
		return

	client = Client(
		name=user_id,
		session_string=string_session,
		in_memory=True,
	)
	register_all_handlers(client)

	try:
		client.run()
	except:
		logger.error("""
			\rInvalid session_string for pyrogram client. 
			\rPlease provide valid credentials.
		""")
		return
