from database import Database
from database.models import User, UserBotSession

from sqlalchemy.exc import NoResultFound
from typing import Union
from loguru import logger



@logger.catch
def get_user(user_id: int) -> Union[User, None]:
	"""
	Get a user from the database by their unique identifier.

	Args:
		user_id (int): The unique identifier for the user.

	Returns:
		Union[User, None]: The User instance if found, or None if not found.
	"""
	try:
		return Database().session.query(User).filter(User.user_id == user_id).one()
	except NoResultFound:
		return None


@logger.catch
def get_user_bot_session(user_id: int) -> Union[UserBotSession, None]:
	"""
	Get a user's bot session from the database by their unique identifier.

	Args:
		user_id (int): The unique identifier of the user.

	Returns:
		Union[UserBotSession, None]: The UserBotSession instance if found, or None if not found.
	"""
	try:
		return Database().session.query(UserBotSession).filter(UserBotSession.user_id == user_id).one()
	except NoResultFound:
		return None
