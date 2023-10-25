from subprocess import Popen
from sys import executable
from typing import NoReturn

from misc import PathManager, SingletonMeta
from database import operations
from database.models import UserBotSession

from loguru import logger



class UserBotProcess(metaclass=SingletonMeta):
	_processes: dict[int, Popen] = {}

	@classmethod
	@logger.catch
	def is_active(cls, user_id: int) -> bool:
		"""
		Check if a user's bot process is currently active.

		Args:
			user_id (int): The unique identifier of the user.

		Returns:
			bool: True if the user's bot process is active, False otherwise.
		"""
		return bool(cls._processes.get(user_id))


	@classmethod
	@logger.catch
	def activate(cls, user_id: int, user_bot_session: str=None) -> bool:
		"""
		Activate a user's bot process.

		Args:
			user_id (int): The unique identifier of the user.
			user_bot_session (str): The user's bot session string.

		Returns:
			bool: True if activation was successful, False otherwise.

		Note:
			This method starts the user's bot process and sets it as active.
		"""
		on_success = True

		if not cls.is_active(user_id):
			user_bot_dir: str = PathManager.get("run_user_bot.py")

			if not user_bot_session:
				user_bot_session: UserBotSession = operations.get_user_bot_session(user_id)
				if user_bot_session:
					user_bot_session: str = user_bot_session.string

			if not user_bot_session:
				logger.error(
					user_bot_process_session_lack.format(user_id=user_id)
				)
				on_success = False
				return on_success

			cls._processes[user_id] = True
			# Popen(
			# 	[executable, user_bot_dir, user_bot_session, str(user_id)]
			# )
			operations.set_user_bot_session_condition(user_id, True)

		return on_success


	@classmethod
	@logger.catch
	def deactivate(cls, user_id: int) -> NoReturn:
		"""
		Deactivate a user's bot process.

		Args:
			user_id (int): The unique identifier of the user.

		Note:
			This method stops the user's bot process and sets it as inactive.
		"""
		if cls.is_active(user_id):
			# cls._processes[user_id].kill()
			del cls._processes[user_id]
			operations.set_user_bot_session_condition(user_id, False)
