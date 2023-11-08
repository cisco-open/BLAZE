import os
import os.path as path
import datetime
import requests
from backend.auth.escherauth import EscherRequestsAuth

def EscherRequest(request_type,url,config, params=None, data=None):
    date_format = '%Y%m%dT%H%M%SZ'
    date_string = datetime.datetime.utcnow().strftime(date_format)
    date = datetime.datetime.strptime(date_string, date_format)
    url = url
    headers = {'X-Escher-Date': date_string,
                    'host': config["host"],
                    'content-type': 'application/json'}
    auth=EscherRequestsAuth(config["credential_scope"],
                                    {'current_time': date},
                                    {'api_key': config["api_key"], 'api_secret': config["api_secret"]})

    response = requests.request(request_type,url,headers=headers, auth=auth, params=params, data=data)
    return response 


request_function_dict = {
    "Escher": EscherRequest,
}

def make_request(authentication_type, request_type, url, config,params=None, data=None):
    response = request_function_dict.get(authentication_type)(request_type, url, config,params=None, data=None)
    return response