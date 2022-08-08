""" 
====================================================
ElasticBERT
====================================================
This module loads an Elastic+BERT model and makes it available for the 
dashboard to use.

This file will work if Elasticsearch is downloaded anywhere locally
and is currently running. In order to start Elasticsearch, simply 
type "./bin/elasticsearch" into your terminal and execute the cmd. 

If on Windows, you will need to type ".\bin\elasticsearch.bat"

"""

from aski.models.search.model_search import ModelSearch
from aski.models.model_helpers.helpers_semantic import answer_question
from aski.models.model_helpers.helpers_general import create_index, index_into_elasticsearch, search, segment_documents

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import time

# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def get_ElasticBERT_info(): 

    model_info = {
        'name'       : "ElasticBERT",
        'class_name' : 'ElasticBERT',
        'desc'       : "ElasticSearch + BERT to accelerate Q/A",
        'link'       : "TBD",
        'repo'       : "TBD"}

    return model_info

# ==============================================================================
# ============================= ELASTIC CLASS ==================================
# ==============================================================================


class ElasticBERT(ModelSearch):

    def __init__(self):
        self._info = get_ElasticBERT_info()
    
    def get_name(self): 
        return self._info['name']

    def load_model(self, file_name, file_content): 

        self.file_name = file_name 
        self.docs = segment_documents([file_content])

        self.tokenizer = AutoTokenizer.from_pretrained(
            "deepset/bert-large-uncased-whole-word-masking-squad2")

        self.model = AutoModelForQuestionAnswering.from_pretrained(
            "deepset/bert-large-uncased-whole-word-masking-squad2")
        
        create_index()  

        for doc in self.docs:
            index_into_elasticsearch(doc)


    def file_search(self, search_term): 
        result = sum_docs = orig_w_h = new_candidate_docs = []

        t_s = time.time()
        res = search(search_term)
        hits = res['hits']['hits']

        for i in range(len(hits)):
            c_d = hits[i]['_source']['text']
            r, start, end = answer_question(
                search_term, c_d, self.model, self.tokenizer)

            if r == '':
                continue
            result.append(r)
            orig_w_h.append([start, r, end])
            new_candidate_docs.append(c_d)

        sum_docs = ['']*len(new_candidate_docs)
        res = [{'res': r, 'sum': s, 'orig': o, 'orig_w_h': o_h}
               for r, s, o, o_h in zip(result, sum_docs, new_candidate_docs, orig_w_h)]

        t_e = time.time()
        t_search = t_e - t_s

        return res, t_search


