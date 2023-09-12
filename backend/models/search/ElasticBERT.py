
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0


""" 
====================================================
ElasticBERT
====================================================
This module loads an Elastic+BERT model and makes it available for the 
dashboard to use.

This file will work if Elasticsearch is downloaded anywhere locally
and is currently running. In order to start Elasticsearch, simply 
type "./bin/elasticsearch" into your terminal and execute the cmd. 

If on Windows, you will need to type ".\bin\\elasticsearch.bat"

"""

from backend.models.interfaces.model_search import ModelSearch, answer_question, \
    create_index, index_into_elasticsearch, search, segment_documents

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import time

# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================


def get_ElasticBERT_info():

    model_info = {
        'name': "ElasticBERT",
        'class_name': 'ElasticBERT',
        'desc': "ElasticSearch + BERT to accelerate Q/A",
        'link': "TBD",
        'repo': "TBD"}

    return model_info

# ==============================================================================
# ============================= ELASTIC CLASS ==================================
# ==============================================================================


class ElasticBERT(ModelSearch):

    def __init__(self):
        self._info = get_ElasticBERT_info()

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
