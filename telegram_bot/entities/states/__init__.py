from .dataset import Upload, Train
from .user_bot import Connect



class DatasetState:
	"""
	A class to manage different states related to dataset handling.
	Attributes:
		Upload (StatesGroup): Represents the state group for uploading datasets.
		Train (StatesGroup): Represents the state group for training datasets.
	"""
	Upload = Upload
	Train = Train



class UserBotState:
	"""
	A class representing the state for working with user bot
	Attributes:
		Connect (StatesGroup): Represents the state group for connecting.
	"""
	Connect = Connect
