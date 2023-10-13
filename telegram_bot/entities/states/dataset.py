from aiogram.dispatcher.filters.state import State, StatesGroup



class Download(StatesGroup):
	download = State()



class Train(StatesGroup):
	train = State()



class Dataset(Download, Train):
	pass
	