
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