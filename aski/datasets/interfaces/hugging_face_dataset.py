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

	def __init__(self, dataset_name, config):

		self._config              = config
		self._dataset_name        = dataset_name
		self._dataset             = load_dataset(self._dataset_name, config)
		self._dataset_builder     = load_dataset_builder(self._dataset_name, 
														config)
		self._dataset_description = self._dataset_builder.info.description
		self._dataset_features    = self._dataset_builder.info.features

	def _compute_metric(self, metric_name, model):

		metric = load_metric(metric_name, self._dataset_name)

		#model_predictions = model(model_inputs)
		#final_score = metric.compute(predictions=model_predictions, references=gold_references)

	def _print_dataset_facts(self):

		print(self._dataset_description)
		print(self._dataset_features)

	def _get_random_example(self, text_column_name):

		# Get the size of the dataset
		dataset_len = self._dataset.num_rows

		# Generate a random index to shuffle from in the dataset
		random_index = randint(0, dataset_len - 1)

		return self._dataset[random_index][text_column_name]

	def _get_list_examples(self, text_column_name, number_examples):

		examples = []

		# Sample the first x examples from the dataset
		for index in range(0, number_examples):

			example = self._dataset[index][text_column_name]
			examples.append(example)

		return examples
