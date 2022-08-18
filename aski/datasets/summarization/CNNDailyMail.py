"""
CNN/DailyMail Dataset
====================================================
This module extends the Dataset Class and is used to load specifically from the 
CNN/DailyMail Dataset.

https://huggingface.co/datasets/cnn_dailymail
"""

from aski.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset

class CNNDailyMail(HuggingFaceDataset):

	def __init__(self):
		super().__init__(
			dataset_name='cnn_dailymail', 
			config='3.0.0', 
			class_name='CNNDailyMail',
			document_column='article',
			summary_column='highlights',
			split='validation')
		