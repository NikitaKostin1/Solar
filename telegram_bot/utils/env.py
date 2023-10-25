import os
from abc import ABC
from typing import Final



class Env(ABC):
	TOKEN: Final = os.getenv("TOKEN", None)
	API_ID: Final = os.getenv("API_ID", None)
	API_HASH: API_HASH = os.getenv("API_HASH", None)
