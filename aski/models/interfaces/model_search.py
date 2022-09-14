class ModelSearch():

    def __init__(self):
        pass

    def load_model(self, file_name, file_content): 
        self.file_name = file_name
        self.file_content = file_content
        pass 

    def file_search(self, search_term):
        ''' Load a model from a directory or library'''
        pass
    
    def _get_model_info(self):
        pass
        
    def _get_name(self):
        return self._info['name']

    def _get_class_name(self):
        return self._info['class_name']
    
    @classmethod 
    def _parse_raw_ans(self, res, time): 

        try:
            ans = res[0]['res'] + f" ({round(time, 2)}s)"
        except:
            ans = "Unable to find an answer."

        return ans 

"""

This file contains several helper functions utilized by the ASKI dashboard. 

All functions (as well as their descriptions) are listed below: 

    answer_question(question, answer_text, model, tokenizer) - internal 
    dedup(hits) - returns list of potential hits in document, internal 
    summarize_answer(candidate_docs, summarized=None) - summarizer, internal 

"""

from transformers import pipeline
from transformers import BertTokenizer, BertForQuestionAnswering

import collections, torch, re


"""

Internal helper function used by BERT/ColBERT 

"""

def answer_question(question, answer_text, model, tokenizer):
    #global model, tokenizer

    input_ids = tokenizer.encode(
        question, answer_text, max_length=512, truncation=True)

    # ======== Set Segment IDs ========
    # Search the input_ids for the first instance of the `[SEP]` token.
    sep_index = input_ids.index(tokenizer.sep_token_id)

    # The number of segment A tokens includes the [SEP] token istelf.
    num_seg_a = sep_index + 1

    # The remainder are segment B.
    num_seg_b = len(input_ids) - num_seg_a

    # Construct the list of 0s and 1s.
    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    # There should be a segment_id for every input token.
    assert len(segment_ids) == len(input_ids)

    outputs = model(torch.tensor([input_ids]),  # The tokens representing our input text.
                    # The segment IDs to differentiate question from answer_text
                    token_type_ids=torch.tensor([segment_ids]),
                    return_dict=True)

    start_scores = outputs.start_logits
    end_scores = outputs.end_logits

    # ======== Reconstruct Answer ========
    # Find the tokens with the highest `start` and `end` scores.
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    # Get the string versions of the input tokens.
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    # Start with the first token.
    answer = tokens[answer_start]
    # print(tokens)
    beg, end = tokens[0], tokens[answer_end+1]
    # Select the remaining answer tokens and join them with whitespace.
    for i in range(answer_start+1, answer_end+1):
       # print(f'{i},{tokens[i]}')
        # If it's a subword token, then recombine it with the previous token.
        if len(tokens[i]) > 2 and tokens[i][0:2] == '##':
            if 0 < i < answer_start:
                beg += tokens[i][2:]
            elif answer_start < i < answer_end+1:
                answer += tokens[i][2:]
            elif answer_end+1 < i:
                end += tokens[i][2:]

        # Otherwise, add a space then the token.
        else:
            if 0 < i < answer_start:
                beg += ' ' + tokens[i]
            elif answer_start < i < answer_end+1:
                if tokens[i] in [',', '.', ':']:
                    answer += tokens[i]
                else:
                    answer += ' ' + tokens[i]
            elif answer_end+1 < i:
                end += ' ' + tokens[i]

    print('Answer: "' + answer + '"')
    if answer == "[CLS]":
        answer, beg, end = '', '', ''
    else:
        m = re.search(answer, answer_text, re.IGNORECASE)
        if m:
            beg = answer_text[:m.start()]
            answer = answer_text[m.start():m.end()]
            end = answer_text[m.end()+1:]

    return answer, beg, end


"""

Returns list of potential hits in candidate document 

"""

def dedup(hits):
    candidate_docs = [h['_source']['message_body'] for h in hits]

    tmp = collections.Counter(candidate_docs)
    tmp = sorted(tmp, key=tmp.get, reverse=True)
    return list(tmp)


"""

Summarized answer found in candidate documents 

"""

def summarize_answer(candidate_docs, summarizer=None):
    if summarizer is None:
        summarizer = pipeline("summarization")
    sum_docs = []
    for doc in candidate_docs:
        if len(doc) > 300:
            doc = doc[:300]
        sum_docs.append(summarizer(
            doc, min_length=min(len(doc), 50), max_length=min(len(doc), 300)))

    return sum_docs

"""

This file contains several helper functions utilized by the ASKI dashboard. 

All functions (as well as their descriptions) are listed below: 

    create_index() - cleans up index, creates fresh new one 
    putMapping() - puts mapping, returns config dictionary 
    index_into_elasticsearch(contents) - indexes inputted document 
    basic_search(query) - converts english question into search query
    search(query) - performs a search, returns results
    print_index_dump(query) - helper function, verbose print

    segement_documents(doc, doc_max_length=300) - splits document into chunks


A reference: http://praveendiary.blogspot.com/2014/10/elastic-search-experimentation-with.html

"""


from email.parser import Parser
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
from importlib import import_module
import traceback 

# Global Variables utilized by the following helper functions (elasticsearch client)

INDEX_NAME = 'text_file_search'
es = Elasticsearch( hosts=[{'host': 'localhost', 'port': 9200, 'scheme': 'http'}], verify_certs=False, timeout=60, connection_class=RequestsHttpConnection )
p = Parser()
count = 0



"""

(Elastic) Cleans up the index if exists & then creates a fresh index

"""

def create_index():

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print('DELETED EXISTING INDEX \'{}\' to create new one '.format(INDEX_NAME))
    config = putMapping()
    result = es.indices.create(index=INDEX_NAME, body=config, ignore=400)

    return



"""

(Elastic) Puts new mapping and returns config dictionary 

"""

def putMapping():
    config = {}
    config['settings'] = {
        'analysis': {
            'analyzer': {
                'default': {
                    'type': 'standard',
                    'stopwords': '_english_',
                }
            }
        }
    }

    config['mappings'] = {
        "dynamic": "strict",
        "_source": {"enabled": "true"},
        "properties":
        {
            "text": {"type": "text", "store": "false"},
        }
    }

    return config



"""

(Elastic) Indexes into elasticsearh given the current document 

"""

def index_into_elasticsearch(contents):
    global count
    msg = p.parsestr(contents)
    jsonMapDoc = {}

    jsonMapDoc["text"] = contents

    try:
        es.index(index=INDEX_NAME, body=jsonMapDoc)

    except Exception as ex:
        traceback.print_exc()
        count += 1
        if count > 5:
            exit()
        print("Failed to index the document {}".format(jsonMapDoc))
    return



"""

(Elastic) Returns an english query in the form of an elastic query

"""

def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }, 
        "size": 1
    }
    return q


"""

(Elastic) Performs a search given an query, returns results 

"""

def search(query):
    INDEX = 'text_file_search'
   
    es.indices.refresh(index=INDEX) # THIS WAS THE MAGIC LINE THAT FIXED IT!

    query_body = basic_search(query)
    res = es.search(index=INDEX, body=query_body)
    return res



"""

(Elastic) Helper function given a query, returns dump of retrieved index 

"""

def print_index_dump(query): 

    all_indices = es.indices.get_alias("*")
    all_docs = {} 
    print("--------------------------------------------")
    # iterate over the index names
    for ind in all_indices:

        # skip hidden indices with '.' in name
        if "." not in ind[:1]:

            # nest another dictionary for index inside
            all_docs[ind] = {}

            # print the index name
            print("\nindex:", ind)

            # get 20 of the Elasticsearch documents from index
            docs = es.search(
                from_=0,  # for pagination
                index=ind,
                body={
                    'size': 10,
                    'query': {
                        # pass query paramater
                        'match_all': {}
                    }
                })

            # get just the doc "hits"
            docs = docs["hits"]["hits"]

            # print the list of docs
            print("index:", ind, "has", len(docs), "num of docs.")

            # put the list of docs into a dict key
            all_docs[ind]["docs"] = docs

            try:
                # returns dict object of the index _mapping schema
                raw_data = es.indices.get_mapping(ind)
                print("get_mapping() response type:", type(raw_data))

                # returns dict_keys() obj in Python 3
                mapping_keys = raw_data[ind]["mappings"].keys()
                print("\n_mapping keys():", mapping_keys)

                # get the index's doc type
                doc_type = list(mapping_keys)[0]
                print("doc_type:", doc_type)

                # get the schema by accessing index's _doc type
                schema = raw_data[ind]["mappings"][doc_type]["properties"]
                print("all fields:", list(schema.keys()))

                all_docs[ind]["fields"] = schema
                all_docs[ind]["doc_type"] = doc_type
            except Exception as err:
                print("client.indices error:", err)
                all_docs[ind]["fields"] = {}
                all_docs[ind]["doc_type"] = doc_type
    print("----------------------------------------------")



"""

(General) Segments a given document (into list, if beyond max_doc_length)

"""

def segment_documents(docs, max_doc_length=300):
    # List containing full and segmented docs
    segmented_docs = []

    for doc in docs:
        # Split document by spaces to obtain a word count that roughly approximates the token count
        split_to_words = doc.split(" ")

        # If the document is longer than our maximum length, split it up into smaller segments and add them to the list
        if len(split_to_words) > max_doc_length:
            for doc_segment in range(0, len(split_to_words), max_doc_length):
                segmented_docs.append(
                    " ".join(split_to_words[doc_segment:doc_segment + max_doc_length]))

        # If the document is shorter than our maximum length, add it to the list
        else:
            segmented_docs.append(doc)

    return segmented_docs

"""

This file contains several helper functions used to benchmark. 

All functions (as well as their descriptions) are listed below: 

    squad_benchmark(pQueue, name, dir, m_name) - main function called by ASKI
    was_correct(m_ans, q_ansl) - given list of answers, determines correctness


NOTE: ASKI's solo benchmarking feature may not work at the moment 
      due to ongoing changes in this file (no longer stable). Will
      be fixed shortly in a future commit! 
   
"""

from aski.dash_files.app_constants import * 
import os
import json

import numpy as np
from fuzzywuzzy import fuzz
import logging
import sys


"""

Runs the inputted model (either ColBERT or Elastic) on a SQUAD dataset

"""


def squad_benchmark(queue, file_name, file_path, model_obj):


    # Load all questions/files for associated dataset (SQUAD)

    f = open(file_path, "r")
    lines = f.readlines()[1:]
    f.close()
    file_content = "".join(lines)

    q_dir = "/".join(file_path.split("/")[:-1]) + "/"
    files = [files[2] for files in os.walk(q_dir)][0]
    questions = [file for file in files if file[:3] == "qas"]


    # Creating results dictionary (use to store/dump in queue)

    results = CONST_RESULTS

    results['m_name'] = model_obj._info['class_name']
    results['f_name'] = file_name 
    results['root'] = q_dir 

    results['questions']['num_qf'] = len(questions) 
    results['questions']['all_qs'] = questions 



    model_obj.load_model(file_name, file_content)
    queue.put_nowait(results)


    # Find number of answerable questions (some are impossible)

    tot_q = 0
    for q_file in questions:
        q = open(q_dir + q_file, "r")
        q_data = json.load(q)
        q.close()
        for qas in q_data['qas']:
            if len(qas['answers']) == 0:
                continue
            if qas["is_impossible"]:
                continue
            tot_q = tot_q + 1

    results["questions"]["num_qs"] = tot_q


    # TODO: go through all files and index at once (giant txt)
    # TODO: make this a new function ^^ (test retriever + q/a)
    # TODO: currently retriever has little work to do 

    # Start iterating through all answerable questions

    for q_file in questions:

        q = open(q_dir + q_file, "r")
        q_data = json.load(q)
        q.close()

        for qas in q_data['qas']:
            try:
                q_text = qas['question']
                q_anss = qas['answers']
                q_ansl = []
                for ans in q_anss:
                    q_ansl.append(ans['text'])
                if len(q_ansl) == 0:
                    break

                print(f"(squad_benchmark) > Question: {q_text}")
                print(f"(squad_benchmark) > Valid ans: {q_ansl}")

                res, time = model_obj.file_search(q_text)
                m_ans = res[0]['res']

                valid = was_correct(m_ans, q_ansl)

                print(f"(squad_benchmark) > Time Taken: {time}")
                print(f"(squad_benchmark) > Corect?: {valid}")

                results["questions"]["tot_qs"] = results["questions"]["tot_qs"] + 1
                results["times"]["all_ts"].append(time)
                results["metrics"]["correct_arr"].append(valid)

                if valid == 0:
                    results["metrics"]["incorrect_d"][q_text] = [
                        m_ans, q_ansl, q_data['context']]

                queue.put_nowait(results)

            except:
                print(f"(squad_benchmark) > Exited prematurely, skipping question.")
                pass



    results["times"]["avg_ts"] = np.mean(results["times"]["all_ts"])
    results["metrics"]["accuracy_num"] = results["metrics"]["correct_arr"].count(1)
    results["metrics"]["accuracy_prc"] = np.mean(results["metrics"]["correct_arr"])

    queue.put("DONE")


"""

Determines whether the model's answer matches the ground truth 

"""


def was_correct(m_ans, q_ansl):

    m_ans = m_ans.lower()
    m_ans = m_ans.replace(" ", "")

    for poss_ans in q_ansl:
        poss_ans = poss_ans.lower()
        poss_ans = poss_ans.replace(" ", "")

        if m_ans in poss_ans or poss_ans in m_ans or fuzz.partial_ratio(m_ans, poss_ans):
            return 1

    return 0