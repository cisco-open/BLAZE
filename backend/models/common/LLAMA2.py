import openai
from flask import current_app
from llama_cpp import Llama
import os
import inspect
import re
import json
from dotenv import load_dotenv
import requests
from typing import Callable, Dict
import datetime
from collections import defaultdict
import time

def get_LLAMA2_info():
    """ 
    Function to return a dictionnary containing the name, class name, 
    description, paper link and GitHub repo link of the BART model. It is used 
    throughout the code to get various information about the model.

    Returns
    -------
    model_info : a dictionnary
        A dictionnary containing the name, class name, 
        description, paper link and GitHub repo link of the T5 model
    """
    model_info = {
        'name': "LLAMA2",
        'class_name': 'LLAMA2',
        'desc': "LLAMA2",
    }
    return model_info

class LLAMA2():
    tasks_supported = ["actionables","summarization","chat"]
    model = None

    def __init__(self):
       
        self._info = get_LLAMA2_info()
    
    def load_model(self,*args):
        self.model = Llama(model_path="/home/vamsi/projects/llama2/llama2-webui/models/llama-2-7b-chat.Q4_0.gguf", n_ctx=2048)

    def _get_model_info(self):
        pass

    def _get_name(self):
        return self._info['name']

    def _get_class_name(self):
        return self._info['class_name']
    
    def file_search_prompt_format(self,search_term,context):
        return f"""
            Given story and question below. return appropriate answer in a word or two.

            ### Story:
            {context}

            ### Question:
            Q:{search_term}
            
            ### Answer:

            \n    
            """
    
    def file_search(self,search_term,context):
        # prompt = "You are a helpful assistant answering questions based on the context provided.Reply with value only, no other text."
        # message = f"{prompt}\n{context}\nQuestion:{search_term}"
        t_s = time.time()
        output = self.model(self.file_search_prompt_format(search_term,context), # Prompt
                max_tokens=32, # Generate up to 32 tokens
                echo=False # Echo the prompt back in the output
            )
        res = output["choices"][0]["text"]
        print(res)
        t_e = time.time()
        t_search = t_e - t_s

        return res, t_search
