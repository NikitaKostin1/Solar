from database import Database, operations
from database.models import User, UserBotSession

from typing import NoReturn
from loguru import logger



@logger.catch
def set_user_bot_session_condition(user_id: int, new_condition: bool) -> NoReturn:
	"""
	Update the condition (enable/disable) of a user's bot session in the database.

	Args:
		user_id (int): The unique identifier of the user.
		new_condition (bool): The new condition for the bot session.

	Raises:
		NoReturn: No specific return value.

	Note:
		If the user bot session is not found, a warning is logged, but no exception is raised.
	"""
	user_bot_session = operations.get_user_bot_session(user_id)

	if not user_bot_session:
		logger.warning(f"None user bot session found for {user_id}")
		return

	user_bot_session.is_enable = new_condition
	Database().session.commit()
