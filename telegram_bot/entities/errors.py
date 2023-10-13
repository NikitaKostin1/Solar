from dataclasses import dataclass



@dataclass(order=True)
class TxtExtensionError(Exception):
	"""
	Exception for the case where a file does not have a .txt extension.
	"""
	message: str = "File without .txt extension"



@dataclass(order=True)
class NoFilesUploadedError(Exception):
	"""
	Exception for the case where no files have been uploaded.
	"""
	message: str = "No files have been uploaded"
