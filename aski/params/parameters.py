""" 
====================================================
Params
====================================================
This module stores a class to initialize, access and modify the parameters
of the dashboard used throughout the code.

"""

import json
from multiprocessing import Queue
from aski.utils.helpers import get_list_objects
from aski.dash_files.app_constants import *

# ==============================================================================
# ============================ PARAMETERS CLASS ================================
# ==============================================================================

class Parameters:

    def __init__(self, data_dict=None):

        """
        
        What yml will contain: 

        "Title": "Solo Question Answering on Custom Text", 
        "function": {"task": "Search", "custom": true, "benchmarking": false, "comparing": false}, 
        "data": {"DATA_PATH": "./data/squad2_data", "DATA_SETS": "1", "DEFAULT": "1973_oil_crisis", "FILES_PATH": "./data/user_files"}, 
        "models": ["ElasticBERT"]}
        

        What will be added by this class: 

        "states" : {"chosen_data": None, "chosen_path": None, "has_input_file": False, "has_indexed": False, "model_objs": []}

        """


        self._data_dict = data_dict
        
        self._data_dict['states'] = {} 

        self._data_dict['states']['chosen_data'] = None 
        self._data_dict['states']['chosen_path'] = None 
        self._data_dict['states']['has_input_file'] = False  
        self._data_dict['states']['has_indexed'] = False 
        self._data_dict['states']['has_summarized'] = False 

        self._data_dict['states']['has_dataset'] = False  
        self._data_dict['states']['has_metric'] = False  

        print(f"\n==== Loading Models ===\n")

        self._data_dict['states']['model_dict']   = {}
        self._data_dict['states']['model_active'] = {}

        tasks_list = self._data_dict['function']['task'].split('/')

        for task in tasks_list:

            self._data_dict['states']['model_dict'][task]   = get_list_objects(self._data_dict['models_' + task], task, 'models') 
            self._data_dict['states']['model_active'][task] = None

        #print(f"\n==== Loading Datasets ===\n")
        #self._data_dict['states']['dataset_active']  = []     
        #print(f"\n==== Loading Metrics ===\n")
        #self._data_dict['states']['model_active'] = []
        #self._data_dict['states']['metric_objs']     = get_list_objects(self._data_dict['metrics'], self._data_dict['function']['task'], 'metrics') 
        #self._data_dict['states']['metrics_results'] = [] 

        self._data_dict['states']['query'] = SEARCH_BOX_PLACEHOLDER
        self._data_dict['states']['result_search']        = ANSWER_BOX_PLACEHOLDER
        self._data_dict['states']['result_summarization'] = ANSWER_BOX_PLACEHOLDER
        self._data_dict['states']['reset_presses'] = 0 

        self._data_dict['states']['processes'] = {} # Dictionary with: {model_name: [process, queue, old_results]}
        self._data_dict['states']['begun_queue'] = False 
        


    def _update_data_dict_model_used(self, model_used):

        self._data_dict['states']['model_active'] = model_used 

    def _reset_data_dict_states(self):

        self._data_dict['states']['has_input_file'] = False
        self._data_dict['states']['has_indexed']    = False
        self._data_dict['states']['chosen_name']    = None
        self._data_dict['states']['chosen_path']    = None 

        self._data_dict['states']['query'] = SEARCH_BOX_PLACEHOLDER
        self._data_dict['states']['result'] = ANSWER_BOX_PLACEHOLDER


        # Killing/resetting all multi-processing related things 

        for model_name in self._data_dict['states']['processes']: 
            p = self._data_dict['states']['processes'][model_name][0]
            p.kill() 
        
        self._data_dict['states']['processes'] = {}
        self._data_dict['states']['begun_queue'] = False 



    def _update_params(self, params):

        self._data_dict = params
    
    def _get_params(self): 

        return(self._data_dict)

    def get_function_task(self): 
        return self._data_dict['function']['task']

    def get_title(self): 
        return self._data_dict['Title']