from aiogram.dispatcher.filters.state import State, StatesGroup



class Connect(StatesGroup):
	phone_number = State()
	auth_code = State()
	two_fa_password = State()
