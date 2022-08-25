"""
XSumDataset
====================================================
This module extends the Dataset Class and is used to load specifically from the 
XSum Dataset.

https://huggingface.co/datasets/xsum
"""

from aski.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset

class XSum(HuggingFaceDataset):

	def __init__(self):
		super().__init__(
			dataset_name='xsum', 
			config='3.0.0',  
			class_name='XSum',
			document_column='document',
			summary_column='summary',
			split='validation')
		