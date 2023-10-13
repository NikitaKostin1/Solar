import os
from abc import ABC
from typing import Final



class Env(ABC):
	TOKEN: Final = os.getenv("TOKEN", None)
