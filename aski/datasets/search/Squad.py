"""
Squad
====================================================
This module extends the HuggingFaceDataset Class and is used to load 
specifically from the Squad Dataset
"""

from aski.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset

class Squad(HuggingFaceDataset):

	def __init__(self):
		super().__init__(
			dataset_name='squad_v2', 
			config='squad_v2', 
			class_name='Squad', 
			document_column='text',
			summary_column=None, 
			split=None)
		
		self._topic_content = self._create_topic_content() 
	
	''' Internal helper function to parse through dataset ''' 
	def _create_topic_content(self):  
		topic_content = {} 

		# topic_content: title --> {context : [q/a pairs]}

		for entry in self._dataset['train']: 

			title = entry['title'] # is a string 
			context = entry['context'] # is a string
			question = entry['question'] # is a string 
			answers = entry['answers']['text'] # can be a list 

			if title not in topic_content: 
				topic_content[title] = {context : [(question, answers)]}

			elif context not in topic_content[title]: 
				topic_content[title][context] = [(question, answers)]
			
			else: 
				topic_content[title][context].append((question, answers))

		return topic_content 
	
	''' Returns list of all available topics (442 total) '''
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
