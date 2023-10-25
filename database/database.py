from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from typing import Final
from misc import SingletonMeta
from config import DATABASE



class Database(metaclass=SingletonMeta):
	"""
	A singleton class for managing a SQLAlchemy database connection and sessions.

	This class provides a single, shared database connection and session for the application.
	It uses SQLAlchemy to interact with the database.

	Attributes:
		BASE (Final): The declarative base class for defining database models.
	"""
	BASE: Final = declarative_base()

	def __init__(self):
		"""
		Initialize the Database instance and establish a database connection.

		The database connection details are retrieved from the 'DATABASE' configuration.
		"""
		db_url = f"{DATABASE['engine']}:///{DATABASE['name']}"
		self._engine = create_engine(db_url)
		session = sessionmaker(bind=self._engine)
		self._session = session()

	@property
	def session(self):
		"""
		Get the SQLAlchemy session for database interactions.

		Returns:
			Session: An SQLAlchemy session object.
		"""
		return self._session

	@property
	def engine(self):
		"""
		Get the SQLAlchemy engine used for the database connection.

		Returns:
			Engine: An SQLAlchemy engine object.
		"""
		return self._engine
