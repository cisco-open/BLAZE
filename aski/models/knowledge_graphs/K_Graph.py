""" 
====================================================
K-Graph
====================================================
This module generates a Knowledge Graph model and makes it available for the 
dashboard to use.

"""

from aski.models.search.model_search import ModelSearch
from aski.model_helpers.helpers_semantic import answer_question
from aski.model_helpers.helpers_general import create_index, index_into_elasticsearch, search, segment_documents

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import time

# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def get_ElasticBERT_info(): 

    model_info = {
        'name'       : "Knowledge Graph",
        'class_name' : 'K-Graph',
        'desc'       : "Knowledge Graph - Generation and Querying",
        'link'       : "TBD",
        'repo'       : "TBD"}

    return model_info

# ==============================================================================
# ============================= ELASTIC CLASS ==================================
# ==============================================================================


class ElasticBERT(ModelSearch):

    def __init__(self):
        self._info = get_ElasticBERT_info()

    def load_model(self, file_name, file_content): 
        pass 

    def file_search(self, search_term): 
        pass 