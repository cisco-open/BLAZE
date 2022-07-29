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
