import requests
import json
import os.path as path
import datetime
from backend.config import TestingConfig
from backend.datasets.common.escherauth import EscherRequestsAuth
from backend.datasets.interfaces.SwaggerBase import SwaggerBase
from tinydb import TinyDB, Query


class Swagger(SwaggerBase):
    def fetch_api_docs(self):
        
        db = TinyDB("/home/vamsi/projects/Blaze/config.json")
        Config = Query()
        yaml_config = db.get(Config.type == 'yaml_config')

        ######## Change according to swagger link 
        self.swagger_url = yaml_config["config"]["Swagger"]["url"]
        self.headers = {'X-Escher-Date': self.date_string,
                                        'host': yaml_config["config"]["Swagger"]["host"],
                                        'content-type': 'application/json'}
        self.auth=EscherRequestsAuth("global/services/portshift_request",
                                                        {'current_time': self.date},
                                                        {'api_key': yaml_config["config"]["Swagger"]["api_key"], 'api_secret': yaml_config["config"]["Swagger"]["api_secret"]})
        
        
        ##############
        return super().fetch_api_docs()