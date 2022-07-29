""" 
====================================================
Params
====================================================
This module stores a class to initialize, access and modify the parameters
of the dashboard used throughout the code.

"""

import json
from multiprocessing import Queue

# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def read_params():

    with open('params/data_dict.txt') as data_dict_file:
        data = data_dict_file.read()
        data_dict = json.loads(data)

    return data_dict

# ==============================================================================
# ============================ PARAMETERS CLASS ================================
# ==============================================================================

class Parameters:

    def __init__(self, data_dict=None):

        if data_dict is None:
            self._data_dict = read_params()
        else:
            self._data_dict = data_dict

    def _update_data_dict_model_used(self, model_used):

        self._data_dict['models_in_use'] = model_used
        self._dump_params()

    def _reset_data_dict_states(self):

        self._data_dict['states']['has_input_file'] = False
        self._data_dict['states']['has_indexed']    = False
        self._data_dict['states']['chosen_name']    = None
        self._data_dict['states']['chosen_path']    = None 
        self._data_dict['states']['q_placeholder']  = "Ask your question",
        self._data_dict['states']['a_placeholder']  = "The output will be here"
        self._dump_params()

    def _read_params(self):

        self._data_dict = read_params()

    def _dump_params(self):

        with open('params/data_dict.txt', 'w') as data_dict_file:
            data_dict_file.write(json.dumps(self._data_dict))
    
    def _update_params(self, params):

        self._data_dict = params



