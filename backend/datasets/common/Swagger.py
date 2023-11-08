import requests
import json
import os.path as path
import datetime
from backend.config import TestingConfig
from backend.auth.escherauth import EscherRequestsAuth
from backend.datasets.interfaces.SwaggerBase import SwaggerBase
from backend.utils import make_request



class Swagger(SwaggerBase):
    def fetch_api_docs(self):

        yaml_config = TestingConfig.db.get(TestingConfig.DBConfig.type == 'yaml_config')

        ######## Change according to swagger link ##########
        response = make_request(yaml_config["config"]["Swagger"]["auth_type"], 'get', yaml_config["config"]["Swagger"]["url"], yaml_config["config"]["Swagger"])
        ##############
        
        return response