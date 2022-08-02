"""
CNN/DailyMail Dataset
====================================================
This module extends the Dataset Class and is used to load specifically from the 
CNN/DailyMail Dataset
"""

from aski.datasets.hugging_face_dataset import HuggingFaceDataset

class CNNDailyMail(HuggingFaceDataset):

	def __init__(self, dataset_name, config):
		super().__init__(dataset_name, config)
		