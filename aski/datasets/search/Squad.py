"""
Squad
====================================================
This module extends the HuggingFaceDataset Class and is used to load 
specifically from the Squad Dataset
"""

import requests 

from aski.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset
from aski.models.interfaces.model_search import was_correct 

from aski.flask_servers.flask_constants import PORT_REST_API, PREF_REST_API 

class Squad(HuggingFaceDataset):

	def __init__(self):
		super().__init__(
			dataset_name='squad_v2', 
			config='squad_v2', 
			class_name='Squad', 
			document_column='text', # <-- name of column with documents 
			summary_column=None, # <-- name of column with "answers"
			split=None) # <-- replace this with either train test or validation
			            # <-- take the smallest one (usually validation)
		
		self._topic_content = self._create_topic_content() 
		self._dataset_type = 'search'
	
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

	def _benchmark(self, model_name, file_name, value_obj): 

		value_obj['status'] = 'starting'
		value_obj['cur_q'] = [] 
		value_obj['tot_q'] = 0 
		value_obj['times'] = [] 
		value_obj['incor'] = [] 


		print("WE ENTERED BENCHMARK")

		topic = file_name 
		story = self._get_title_story(topic)

		for paragraph in story:
			value_obj['tot_q'] += len(self._topic_content[topic][paragraph])

		content = ' '.join(p for p in story)

		request = f"{PREF_REST_API}{PORT_REST_API}/models/initialize"
		response = requests.post(request, json={'model': model_name, 
												'filename': file_name, 
												'filecontent': content}
								)

		value_obj['status'] = 'running'

		print("STARTING TO GO THRU")

		for paragraph in story: 
			for (question, answers) in self._topic_content[topic][paragraph]: 
				print(f"(Squad._benchmark) > Value obj is {value_obj}")

				request = f"{PREF_REST_API}{PORT_REST_API}/models/search"
				response = requests.get(request, json={'model': model_name, 
													'query': question}
									)
				res, time = response.json()['result'], response.json()['latency']

				try: 
					ans = res[0]['res']
				except: 
					ans = None 
				

				if ans is not None: 
					valid = was_correct(ans, answers)

					value_obj['cur_q'] = value_obj['cur_q'] + [int(valid)]
					value_obj['times'] = value_obj['times'] + [round(time, 4)]

					if not valid: 
						value_obj['incor'] = value_obj['incor'] + [{question : [ans, answers, paragraph]}]
				

		value_obj['status'] = 'done' 
		print("FINISHED")