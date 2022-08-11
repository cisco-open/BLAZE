""" 
====================================================
Specifications
====================================================
This module parses the list of models and datasets available to
the user by going through the directories of the folder and parsing 
all the available .py files.

"""

import glob

from aski.utils.helpers import dump_yaml

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
    list_objects : List of str
        A list of strings containing the names of all the available objects

    Examples
    --------
    Here, we parse all the available models for summarization and print the 
    output of the function.

    >>> print(parse_objects('aski/models/', 'summarization/'))

    ['T5', 'Bart']
    """

    list_objects = []

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
            list_objects.append(file_name)

    return(list_objects)

class Specifications:

    def __init__(self):

        self._list_datasets_summarization = parse_objects('aski/datasets/', 'summarization/')
        self._list_datasets_search        = parse_objects('aski/datasets/', 'search/')

        self._list_models_summarization   = parse_objects('aski/models/', 'summarization/')
        self._list_models_search          = parse_objects('aski/models/', 'search/')

    def _specs_to_yaml(self, title, task, custom, benchmarking, comparing, yaml_path):
        """ 
        Method to build a yaml file from the specifications of the code. For 
        example, if the codebase has 3 models for summarization (for example,
        BART, T5 and GPT-2), this method will return a yaml file with the list
        of models available for summarization. It will do the same for the
        datasets available for the task.

        Parameters
        ----------
        title : str
            The title for the dashboard
        task : str
            The task (here, either 'search' or 'summarization')
        custom : str
            The option to have the custom page or not
        benchmarking : str
            The option to have the custom page or not
        comparing : str
            The option to have the custom page or not
        yaml_path : str
            The path to dump the yaml file

        Examples
        --------
        Here, we parse all the available models and datasetsfor search and 
        generate the corresponding yaml file.
    
        >>> specs = Specifications()
        >>>     specs._specs_to_yaml(title="Dashboard", task='search',
        custom='true', benchmarking='true', comparing='true', yaml_path='yaml/trial_yaml.yaml')

        """

        if task == 'search':
            task_data = {
            'models'   : self._list_models_search,
            'datasets' : self._list_datasets_search}

        elif task == 'summarization':

            task_data = {
            'models'   : self._list_models_summarization,
            'datasets' : self._list_datasets_summarization}

        yaml_data = {

        'Title' : title,

        'function': 
        {
        'task'        :task,
        'custom'      :custom,
        'benchmarking':benchmarking
        },

        'data': 
        {
        'DATA_PATH'  : './data/squad2_data',
        'DATA_SETS'  : '1',
        'DEFAULT'    : '1973_oil_crisis',
        'FILES_PATH' : './data/user_files'
        }}

        yaml_data = {**task_data, **yaml_data}

        dump_yaml(yaml_data, yaml_path)

    def _get_models_search(self):
        return self._list_models_search

    def _get_models_summarization(self):
        return self._list_models_summarization

    def _get_datasets_search(self):
        return self._list_datasets_search

    def _get_datasets_summarization(self):
        return self._list_datasets_summarization
