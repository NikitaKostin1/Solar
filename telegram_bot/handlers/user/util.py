from loguru import logger
from typing import List
import config
import os



@logger.catch
def get_neural_dataset_files() -> List[str]:
	"""
	Get a list of dataset file names in the NEURAL_DATASETS_DIR.

	Returns:
		List[str]: A list of dataset file names.
	"""
	all_files = os.listdir(config.NEURAL_DATASETS_DIR)
	# Filter out any cached files created by transformers module
	datasets_files = [name for name in all_files if "cached" not in name]

	return datasets_files
