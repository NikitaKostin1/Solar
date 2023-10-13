from transformers import (
	AutoModelForCausalLM, AutoTokenizer,
	TextDataset, DataCollatorForLanguageModeling, 
	Trainer, TrainingArguments
)
from config import (
	NEURAL_DATASETS_DIR, NEURAL_MODELS_DIR
)

from loguru import logger
import threading
import os



@logger.catch
def train_model(dataset_name: str) -> None:
	"""
	Fine-tunes a pretrained neural language model on a specified dataset.

	Args:
		dataset_name (str): The name of the dataset to use for training.
	"""
	# Download model and tokenizer
	checkpoint = "Kirili4ik/ruDialoGpt3-medium-finetuned-telegram"   
	tokenizer = AutoTokenizer.from_pretrained(checkpoint)
	model = AutoModelForCausalLM.from_pretrained(checkpoint)
	model.eval()

	# Define a TextDataset and DataCollator
	dataset_path = os.path.join(NEURAL_DATASETS_DIR, f"{dataset_name}.txt")

	# Create a TextDataset and DataCollator
	dataset = TextDataset(
		tokenizer=tokenizer, file_path=dataset_path,
		block_size=128, overwrite_cache=False
	)
	data_collator = DataCollatorForLanguageModeling(
		tokenizer=tokenizer, mlm=False
	)

	# Define training arguments
	output_dir = os.path.join(NEURAL_MODELS_DIR, f"{dataset_name}_finetuned")
	training_args = TrainingArguments(
		output_dir=output_dir,
		overwrite_output_dir=True,
		num_train_epochs=2,
		per_device_train_batch_size=2,
		save_steps=10_000,
		save_total_limit=2,
	)

	# Create Trainer and start fine-tuning
	trainer = Trainer(
		model=model,
		args=training_args,
		data_collator=data_collator,
		train_dataset=dataset,
	)

	# Fine-tune the model
	trainer.train()

	# Save the fine-tuned model and tokenizer
	model.save_pretrained(output_dir)
	tokenizer.save_pretrained(output_dir)


@logger.catch
def create_training_thread(dataset_name: str) -> None:
	"""
	Create and start a new thread for training a model on a specified dataset.

	Args:
		dataset_name (str): The name of the dataset to use for training.
	"""
	training_thread = threading.Thread(
		target=train_model, args=(dataset_name,)
	)
	training_thread.daemon = True
	training_thread.start()	
