"""

This file provides an interface to the Elasticsearch model

This file will work if Elasticsearch is downloaded anywhere locally
and is currently running. In order to start Elasticsearch, simply 
type "./bin/elasticsearch" into your terminal and execute the cmd. 

If on Windows, you will need to type ".\bin\elasticsearch.bat"

"""

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
from transformers import pipeline
import time

from aski.models.model import Model
from aski.model_helpers.helpers_semantic import answer_question
from aski.model_helpers.helpers_general import create_index, index_into_elasticsearch, search, segment_documents


class ElasticSearch(Model):

    """
    This function initializes the Elastic search. Make sure to have Elasticsearch 
    installed and running! This can be done via the following link (installation): 

    https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html


    In order to run, simply run "./bin/elasticsearch" in your terminal 

    """

    def __init__(self, file_name, file_content):

        string = "Powered by ElasticSearch BM25"

        summarizer = pipeline("summarization")

        self.tokenizer = AutoTokenizer.from_pretrained(
            "deepset/bert-large-uncased-whole-word-masking-squad2")

        self.model = AutoModelForQuestionAnswering.from_pretrained(
            "deepset/bert-large-uncased-whole-word-masking-squad2")

        self.filename = file_name
        self.docs = segment_documents([file_content])

        create_index()  # This is coming from another function!

        for doc in self.docs:
            index_into_elasticsearch(doc)

    """
    
    This function, given a file, searches it accordingly.

    """

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
