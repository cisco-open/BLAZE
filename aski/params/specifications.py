""" 
====================================================
Specifications
====================================================
This module parses the list of models and datasets available to
the user by going through the directories of the folder and parsing 
all the available .py files.

"""

import glob

def parse_objects(folder, task):
    """ 
    Functions that takes as input a specific folder (for examples aski/models/
    or aski/datasets/) and a task (for example, 'summarization/' or 'search/') 
    and returns a list with the names of all the files within these folders. 
    It is important to specify the slashes or the function will not run properly.

    Parameters
    ----------
    folder : str
        The folder we want to parse for
    task : str
    	The task (here, either 'search/' or 'summarization/')

    Returns
    -------
    list_models : List of str
        A list of strings containing the names of all the available objects

    Examples
    --------
	Here, we parse all the available models for summarization and print the 
	output of the function.

    >>> print(parse_objects('aski/models/', 'summarization/'))

    ['T5', 'Bart']
    """

	list_models = []

	# Get the path of the directory we want to look through
	path = folder + task

	# Iterate over the paths of all files in the directory
	for file_path in glob.iglob(path + '*.py'):

		# Remove the file path (aski/models/search/ColBERT.py --> ColBERT.py)
		file_name = file_path.replace(path, '')

		# Skip __init__.py files
		if file_name == '__init__.py':
			pass

		else:
			# Remove the .py suffix 
			file_name = file_name.rstrip(".py")
			list_models.append(file_name)

	return(list_models)

class Specifications:

	def __init__(self):

		self._list_datasets_summarization = parse_objects('aski/datasets/', 'summarization/')
		self._list_datasets_search        = parse_objects('aski/datasets/', 'search/')

		self._list_models_summarization   = parse_objects('aski/models/', 'summarization/')
		self._list_models_search          = parse_objects('aski/models/', 'search/')

	def _get_models_search(self):
		return self._list_models_search

	def _get_models_summarization(self):
		return self._list_models_summarization

	def _get_datasets_search(self):
		return self._list_datasets_search

	def _get_datasets_summarization(self):
		return self._list_datasets_summarization
