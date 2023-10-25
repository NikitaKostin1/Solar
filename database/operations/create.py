from database import Database, operations
from database.models import User, UserBotSession

from typing import NoReturn
from loguru import logger



@logger.catch
def create_user(user_id: int, username: str) -> User:
	"""
	Create a new user in the database if it doesn't already exist.

	Args:
		user_id (int): The unique identifier for the user.
		username (str): The username of the user.

	Returns:
		User: The created or existing User instance.
	"""
	session = Database().session
	user = operations.get_user(user_id)

	if not user:
		user = User(user_id=user_id, username=username)
		session.add(user)
		session.commit()

	return user


@logger.catch
def create_user_bot_session(user_id: int, session_string: str) -> UserBotSession:
	"""
	Create a new user bot session in the database if it doesn't already exist.

	Args:
		user_id (int): The unique identifier of the user.
		session_string (str): A string associated with the session.

	Returns:
		UserBotSession: The created or existing UserBotSession instance.
	"""
	session = Database().session
	user_bot_session = operations.get_user_bot_session(user_id)

	if not user_bot_session:
		user_bot_session = UserBotSession(user_id=user_id, string=session_string)
		session.add(user_bot_session)
		session.commit()

	return user_bot_session
