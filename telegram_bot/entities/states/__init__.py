from .dataset import Upload, Train



class DatasetState:
	"""
	A class to manage different states related to dataset handling.

	Attributes:
		Upload (StatesGroup): Represents the state group for uploading datasets.
		Train (StatesGroup): Represents the state group for training datasets.
	"""
	Upload = Upload
	Train = Train
