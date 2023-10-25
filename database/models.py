from sqlalchemy import (
	Column, ForeignKey,
	Integer, String, Boolean
)
from sqlalchemy.orm import relationship

from database import Database



class User(Database.BASE):
	"""
	Represents a user in the database.

	Attributes:
		user_id (int): The unique identifier for the user.
		username (str): The username of the user.
		user_bot_session (relationship): A one-to-one relationship with UserBotSession.
	"""
	__tablename__ = 'users'
	user_id = Column(Integer, primary_key=True)
	username = Column(String, nullable=False, default="None")
	user_bot_session = relationship("UserBotSession", uselist=False, backref="user", passive_deletes=True)

	def __init__(self, user_id: int, username: str):
		self.user_id = user_id
		self.username = username

	
	def __repr__(self):
		return f"<User: {self.user_id} | {self.username}>"



class UserBotSession(Database.BASE):
	"""
	Represents a user's bot session in the database.

	Attributes:
		user_id (int): The unique identifier of the user.
		string (str): A string associated with the session.
		is_enable (bool): Whether the session is enabled or not.
	"""
	__tablename__ = "user_bot_sessions"
	user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)
	string = Column(String, nullable=False)
	is_enable = Column(Boolean, default=False)

	def __init__(self, user_id: int, string: str, is_enable: int=False):
		self.user_id = user_id
		self.string = string
		self.is_enable = is_enable


	def __repr__(self):
		is_enable_string = "Enabled" if self.is_enable else "Disabled"
		return f"<Session: {self.user_id} ({is_enable_string})>"



def register_models():
	"""
	Create the database tables for the defined models.
	"""
	Database.BASE.metadata.create_all(Database().engine)
