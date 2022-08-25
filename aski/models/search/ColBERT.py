""" 
====================================================
ColBERT 
====================================================
This module loads a ColBERT model and makes it available for the 
dashboard to use.

This file provides an interface to the ColBERT model proposed in: 
- https://github.com/stanford-futuredata/ColBERT/tree/new_api


"""


from aski.models.interfaces.model_search import ModelSearch, segment_documents, \
answer_question

from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import os, sys, time, torch, shutil

print(os.getcwd() + "/ColBERT/")
sys.path.insert(0, f"{os.getcwd()}/ColBERT/")
from colbert.infra import Run, RunConfig, ColBERTConfig
from colbert import Indexer, Searcher
from colbert.data import Queries
sys.path.insert(0, f"{os.getcwd()}/")

# ==============================================================================
# =========================== AUXILIARY FUNCTIONS ==============================
# ==============================================================================

def get_ColBERT_info(): 

    model_info = {
        'name'       : "ColBERT",
        'class_name' : "ColBERT",
        'desc'       : "ColBERT - Scalable BERT-Based Search",
        'link'       : "https://arxiv.org/abs/2004.12832",
        'repo'       : "https://github.com/stanford-futuredata/ColBERT"}

    return model_info

# ==============================================================================
# ============================= MUPPET CLASS ===================================
# ==============================================================================

class ColBERT(ModelSearch):

    def __init__(self):
        self._info = get_ColBERT_info()
    
    
    def load_model(self, file_name, file_content):
        self.filename = file_name

        self.string = f"ColBERT for {self.filename}"
        self.docs = segment_documents([file_content])

        self.tokenizer = AutoTokenizer.from_pretrained(
            "deepset/bert-large-uncased-whole-word-masking-squad2")

        self.model = AutoModelForQuestionAnswering.from_pretrained(
            "deepset/bert-large-uncased-whole-word-masking-squad2")

        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"

        nbits = 2   # encode each dimension with 2 bits
        self.index_name = f'trial.{nbits}bits'

        doc_maxlen = 300   # truncate passages at 300 tokens
        self.checkpoint = 'ColBERT/docs/downloads/colbertv2.0'

        self.experiment = 'notebook'
        self.searcher = None
        self.indexer = None

        self.f_index_name = f"{os.getcwd()}/experiments/{self.experiment}/indexes/{self.index_name}"

        if os.path.exists(self.f_index_name) and os.path.isdir(self.f_index_name):
            shutil.rmtree(self.f_index_name)

        t_s = time.time()
        with Run().context(RunConfig(nranks=1, experiment=self.experiment)):
            self.config = ColBERTConfig(doc_maxlen=doc_maxlen, nbits=nbits)

            self.indexer = Indexer(
                checkpoint=self.checkpoint, config=self.config)
            self.indexer.index(name=self.index_name,
                               collection=self.docs, overwrite=True)

            self.searcher = Searcher(index=self.index_name)

        t_e = time.time()
        self.t_startup = t_e - t_s



    def file_search(self, search_term):

        result = sum_docs = orig_w_h = new_candidate_docs = []

        query = ""
        if search_term[-1] in '?!,.':
            query = search_term[:-1]
        query = [w.lower() for w in query.split(" ")]
        search_term = " ".join(query)
        print(query)
        t_s = time.time()
        docs = self.searcher.search(search_term, k=3)

        for i, _, _ in zip(*docs):
            c_d = self.searcher.collection[i]

            r, start, end = answer_question(
                search_term, c_d, self.model, self.tokenizer)
            if r == "":
                continue

            result.append(r)
            orig_w_h.append([start, r, end])
            new_candidate_docs.append(c_d)

        res = [{'res': r, 'sum': s, 'orig': o, 'orig_w_h': o_h}
               for r, s, o, o_h in zip(result, sum_docs, new_candidate_docs, orig_w_h)]

        t_e = time.time()
        t_search = t_e - t_s

        return res, t_search
