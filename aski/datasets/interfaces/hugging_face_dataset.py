""" 
====================================================
HuggingFaceDataset 
====================================================
This module loads HuggingFace datasets and makes them available for the 
dashboard and the models to use.
"""

from datasets import load_dataset_builder, load_dataset, load_metric
from random import randint
from transformers import AutoTokenizer

from aski.datasets.interfaces.dataset import Dataset

# ==============================================================================
# ======================= HUGGING FACE DATASET CLASS ===========================
# ==============================================================================

class HuggingFaceDataset(Dataset):

	def __init__(self, dataset_name, config, class_name, document_column, summary_column, split):

		self._class_name          = class_name
		self._config              = config
		self._dataset_name        = dataset_name
		self._dataset             = load_dataset(self._dataset_name, config)
		self._dataset_builder     = load_dataset_builder(self._dataset_name, 
														config)
		self._dataset_description = self._dataset_builder.info.description
		self._dataset_features    = self._dataset_builder.info.features

		self._document_column     = document_column
		self._summary_column      = summary_column
		self._split				  = split

	def _get_class_name(self):
		return self._class_name

	def _get_dataset_name(self):
		return self._dataset_name

	def _print_dataset_facts(self):

		print(self._dataset_description)
		print(self._dataset_features)

	def _get_random_example(self):

		# Get the size of the dataset
		dataset_len = self._dataset.num_rows

		# Generate a random index to shuffle from in the dataset
		random_index = randint(0, dataset_len - 1)

		return self._dataset[random_index][self._document_column]

	def _get_list_examples(self, number_examples):

		examples = []

		# Sample the first x examples from the dataset
		for index in range(0, number_examples):

			example = self._dataset[index][self._document_column]
			examples.append(example)

		return examples
