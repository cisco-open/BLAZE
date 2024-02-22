import openai
from flask import current_app
import openai
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

def get_openAI_info():
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
        'name': "OpenAI",
        'class_name': 'OpenAI',
        'desc': "OpenAI",
    }
    return model_info

class OpenAI():
    tasks_supported = ["actionables","summarization","chat","functions"]
    model = "gpt-3.5-turbo-0613"

    def __init__(self):
        self._info = get_openAI_info()
    
    def load_model(self,*args):
        openai.api_key = current_app.config.get('OPENAPI_KEY')
    
    def _get_model_info(self):
        pass

    def _get_name(self):
        return self._info['name']

    def _get_class_name(self):
        return self._info['class_name']
    
    def gpt_analysis(self, category, processed_text, prompt=None): 
        
        print("Reached GPT analysis")
        #return {'choices' : [{'text': "DUMMY RESPONSE"}]}
        if prompt is not None:
            message = f"{prompt}\n{processed_text}"
        else:
            if category == "summary": 
                print("Coming to summarize")
                prompt = "Analyze the following meeting transcript and generate a summary."
                message = f"{prompt}\n{processed_text}"
            elif category == "actionables": 
                prompt = "Analyze the following meeting transcript and identify actionable items (such as todo's) and return them in a list, separated by the pipeline '|' character" 
                message = f"{prompt}\n{processed_text}"
                print(message)
            elif category == "agenda": 
                prompt = "Analyze the following meeting transcript and idetnify discussed topics as well as the duration they were discussed and return them in a list, separated by the '-' between time and label, and separated by the pipeline '|' character between each item. For example, 'XX:XX - Introductions' may be a valid entry in the returned list, if the meeting contained an introduction." 
                message = f"{prompt}\n{processed_text}"
            else: 
                return None  

    
        openai.api_key = current_app.config.get('OPENAPI_KEY')
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0.7,
            max_tokens=892,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        return response 

    
    def _summarize_text(self, text_to_summarize):
        response = self.gpt_analysis("summary",text_to_summarize)
        return response['choices'][0]['text']
    
    def get_actionables(self,text):
        response = self.gpt_analysis("actionables",text)
        return response['choices'][0]['text']
    
    def parse_docstring(self,function: Callable) -> Dict:
        doc = inspect.getdoc(function)
        
        function_description = re.search(r'(.*?)Parameters', doc, re.DOTALL).group(1).strip()
        parameters_description = re.findall(r'(\w+)\s*:\s*([\w\[\], ]+)\n(.*?)(?=\n\w+\s*:\s*|\nReturns|\nExample$)', doc, re.DOTALL)
        
        returns_description_match = re.search(r'Returns\n(.*?)(?=\n\w+\s*:\s*|$)', doc, re.DOTALL)
        returns_description = returns_description_match.group(1).strip() if returns_description_match else None

        example = re.search(r'Example\n(.*?)(?=\n\w+\s*:\s*|$)', doc, re.DOTALL)
        example_description = example.group(1).strip() if example else None

        signature_params = list(inspect.signature(function).parameters.keys())
        properties = {}
        required = []
        for name, type, description in parameters_description:
            name = name.strip()
            type = type.strip()
            description = description.strip()

            required.append(name)
            properties[name] = {
                "type": type,
                "description": description,
            }
        if len(signature_params) != len(required):
            print(f'Signature params : {signature_params}, Required params : {required}')
            raise ValueError(f"Number of parameters in function signature ({signature_params}) does not match the number of parameters in docstring ({required})")
        for param in signature_params:
            if param not in required:
                raise ValueError(f"Parameter '{param}' in function signature is missing in the docstring")

        parameters = {
            "type": "object",
            "properties": properties,
            "required": required,
        }
        function_dict = {
            "name": function.__name__,
            "description": function_description,
            "parameters": parameters,
            "returns": returns_description,
            # "example": example_description,
        }

        return function_dict


    def run_with_functions(self,messages, function_dicts):
        response = ''
        print(f"within run_with_functions : {messages} and {function_dicts}")
        messages[0]["role"] = "system"
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=function_dicts,
            temperature=0,
        )

        return response

    def get_role_message_dict(role, content=None, fn_name=None, arguments=None, result=None):
        message_dict = {"role":role}
        if role == "user":
            message_dict["content"] = content
        elif role == "assistant":
            message_dict["content"] = content
            message_dict["function_call"] = {}
            message_dict["function_call"]["name"] = fn_name
            message_dict["function_call"]["arguments"] = arguments
        elif role == "function":
            message_dict["name"] = fn_name
            message_dict["content"] = f'{{"result": {str(result)} }}'
        return message_dict

    
    def translate_to_openai_functions(self,api_info):
        openai_functions = []
        tag_dict = defaultdict(list)
        count = 0
        for api in api_info:
            if not api['description']:
                print(api['name']+' does not have a description! and is using summary')
                count += 1
            function_info = {
                'name': api['name'],
                'description': api['description'] if api['description'] else api['summary'],
                'parameters': api['parameters'],
                'path': api['path'],
            }
            openai_functions.append(function_info)
            
            for tag in api['tags']:
                tag_dict[tag].append(function_info)
            
        print(f'Total number of api endpoints without description is {count}')
        return openai_functions, tag_dict
    
    def translate_swagger_data(self,swagger_dataset,description_text):
        api_info = swagger_dataset.api_info
        openai_functions, tag_dict = self.translate_to_openai_functions(api_info)

            
        description_text = description_text
        for index, tmp_dict in enumerate(swagger_dataset.swagger_json['tags']):
            description_text += f'{tmp_dict["name"]} is returned when the following description is satisfied {tmp_dict["description"]},'

        description_text = description_text[:-1] + '.'

        classifier_tag  = {
                'name': "classifies_the_tag",
                'description': description_text,
                'method': 'get',
                'path': '/',
                'tags': 'classifier'
            }
        
        openai_functions.append(classifier_tag)

        return openai_functions, swagger_dataset.swagger_json, tag_dict, classifier_tag
    
    def run_with_functions(self,messages,function_dicts):
        response = ''
        print(f"within run_with_functions : {messages} and {function_dicts}")
        # messages[0]["role"] = "system"
        openai.api_key = current_app.config.get('OPENAPI_KEY')
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            functions=function_dicts,
            temperature=0,
        )
        print(type(response))
        print(response)
        return response

    def file_search(self, search_term,context):
        prompt = "You are a helpful assistant answering questions based on the context provided.Reply with value only, no other text."
        message = f"{prompt}\n{context}\nQuestion:{search_term}"
        t_s = time.time()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0.7,
            max_tokens=892,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
            )
        res = response['choices'][0]['text']
        t_e = time.time()
        t_search = t_e - t_s

        return res, t_search
