"""
User
====================================================
This module is used to load custom text files uploaded by user(s).
"""

import os

from aski.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset

from aski.flask_servers.flask_constants import FILES_DIR 

class User():

	def __init__(self):
		self._class_name = 'User'
		self._dataset_name = 'User'
		self._dataset_type = 'search'

		self._topic_content = {} 

		for path in os.listdir(FILES_DIR):
			if os.path.isfile(os.path.join(FILES_DIR, path)) and path.endswith('.txt'):
				
				f = open(os.path.join(FILES_DIR, path), 'r', encoding='utf-8')
				lines = f.readlines() 
				f.close() 

				self._topic_content[path] = lines 

	def _get_class_name(self):
		return self._class_name

	def _get_dataset_name(self):
		return self._dataset_name

	
	''' Returns list of all available topics '''
	def _get_topic_titles(self): 
		return list(self._topic_content.keys())

	''' Returns entirety of info_dict for a given title '''
	def _get_title_info(self, title): 
		return self._topic_content[title]

	''' Returns text of a topic for a given title as list ''' 
	def _get_title_story(self, title):
		story = []
		for entry in self._topic_content[title]: 
			story.append(entry)
		return story 
