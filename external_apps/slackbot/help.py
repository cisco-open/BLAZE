"""

This file implements the commands of the webex bot, via the underlying class `PrevMeetings`.

"""

from constants import CONSTANTS
import requests
import json
import datetime
import os
import inspect
import re
from dotenv import load_dotenv
from typing import Callable, Dict
from collections import defaultdict
from escherauth import EscherRequestsAuth


base_url = "https://appsecurity.cisco.com/api"


def LoadTranscripts():
    transcriptFileName = "webex_transcripts.json"
    return transcriptFileName
        
"""

HELPER FUNCTIONS LISTED BELOW 

"""

def InitilizeSwaggerFunctions():
    url = CONSTANTS.get("webex_api_endpoint")+"/functions"

    payload = json.dumps({
        "model": "OpenAI",
        "dataset":"Swagger",
        "description_text":"Used when given a question about panoptica to identify the  tag of the api that needs to be referenced."
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return json.loads(response.text)

def GetAPIKeys():
    url = CONSTANTS.get("webex_api_endpoint")+"/swagger_config"

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers)
    print(response.text)
    return json.loads(response.text)

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


def panoptica_call_functions(full_url):
    getKeys = GetAPIKeys()
    access_key = getKeys["response"]["config"]["Swagger"]["access_key"]
    secret_key = getKeys["response"]["config"]["Swagger"]["access_secret"]
    date_format = '%Y%m%dT%H%M%SZ'
    date_string = datetime.datetime.utcnow().strftime(date_format)
    date = datetime.datetime.strptime(date_string, date_format)
    print(f'the full url is {full_url}')
    response = requests.get(full_url,
                          headers={'X-Escher-Date': date_string,
                                   'host': 'appsecurity.cisco.com',
                                   'content-type': 'application/json'},
                          auth=EscherRequestsAuth("global/services/portshift_request",
                                                  {'current_time': date},
                                                  {'api_key': access_key, 'api_secret': secret_key}))

    print("response.status_code = " + str(response.status_code))
    return response

def parse_docstring(function: Callable) -> Dict:
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

def run_with_functions(messages):
    url = "http://127.0.0.1:3000//run_function"

    payload = json.dumps({
        "model": "OpenAI",
        "messages": messages
        })
    headers = {
        'Content-Type': 'application/json'
        }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    
    return json.loads(response.text)
     

def prompt_with_functions(prompt, functions, function_dict):
    # setup_database()
    #prompt += prompt_append()
    prompt = "You are an expert in Panoptica, which is a tool to give security insights in Kubernetes Clusters, API security. You are not aware of anything else. All queries should either use one of the APIs provided or should ask the user to rephrase the qurey: " + prompt
    output = []
    fn_names_dict = {}    
        
    if function_dict:
        function_dicts = functions
        for fn in functions:
            fn_names_dict[fn['name']] = fn
    else:
        for fn in functions:
            fn_names_dict[fn.__name__] = fn
        function_dicts = [parse_docstring(fun) for fun in functions]
    # print(function_dicts)
    messages = [get_role_message_dict("user", content=(prompt))]

    response = run_with_functions(messages)

    if response["choices"][0]["finish_reason"] == "stop":
        print("Received STOP signal from GPT.")
        print()
        print()

    elif response["choices"][0]["finish_reason"] == "function_call":
        print("Received FUNCTION_CALL signal from GPT.")
        fn_name = response["choices"][0]["message"]["function_call"]["name"]
        arguments = response["choices"][0]["message"]["function_call"]["arguments"]
        #json_arguments = json.loads(arguments)
        #function = fn_names_dict[fn_name]
        paths = fn_names_dict[fn_name]['path']
        full_url = base_url + paths
        print(f"Running the {fn_name} function locally with args {arguments}")
        response = panoptica_call_functions(full_url)
        #result = function(**json_arguments)
        print(f"Finished running {fn_name}. Output is {response._content}")
        print()
        print()
        output.append(response._content.decode('utf-8'))
        # output.append(f'You should call the {response.choices[0].message["function_call"].name} function using the following arguments : \n {response.choices[0].message["function_call"].arguments} \n Function raw output : {str(result)}')
        messages.append(get_role_message_dict("assistant", fn_name=fn_name, arguments=arguments))
        messages.append(get_role_message_dict("function", fn_name=fn_name))
        response = run_with_functions(messages)
        

    return output

def RunFunction(message,functions):
    #   print(message,functions)
      output = prompt_with_functions(message, functions["tag_dict"]['dashboard-controller'],function_dict=True)
      return output