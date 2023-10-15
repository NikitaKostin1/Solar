from aiogram.dispatcher.filters.state import State, StatesGroup



class Upload(StatesGroup):
	send_file = State()



class Train(StatesGroup):
	confirm_training = State()
