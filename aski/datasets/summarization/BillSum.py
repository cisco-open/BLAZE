"""
BillSum
====================================================
This module extends the Dataset Class and is used to load specifically from the 
BillSum Dataset.

https://huggingface.co/datasets/billsum
"""

from aski.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset

class BillSum(HuggingFaceDataset):

	def __init__(self):
		super().__init__(
			dataset_name='billsum', 
			config='1.0.0', 
			class_name='BillSum',
			document_column='text',
			summary_column='summary',
			split='ca_test')
		