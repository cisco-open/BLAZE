"""
Squad
====================================================
This module extends the HuggingFaceDataset Class and is used to load 
specifically from the Squad Dataset
"""

from aski.datasets.hugging_face_dataset import HuggingFaceDataset

class Squad(HuggingFaceDataset):

	def __init__(self):
		super().__init__(dataset_name='squad', config='plain_text')