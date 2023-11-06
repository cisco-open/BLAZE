import requests
import json
import os.path as path
import datetime
from backend.config import TestingConfig
from backend.datasets.common.escherauth import EscherRequestsAuth


class SwaggerBase:
    functions_supported = ["search","summarization","functions"]

    def __init__(self):
        self.date_format = '%Y%m%dT%H%M%SZ'
        self.date_string = datetime.datetime.utcnow().strftime(self.date_format)
        self.date = datetime.datetime.strptime(self.date_string, self.date_format)
        self.swagger_url= None
        self.headers = None
        self.auth = None
        self._class_name = 'Swagger'
        self._dataset_name = 'Swagger'

        self.fetch_api_docs()
        
        self.file_name = "functions.json"
        self.swagger_json = self.fetch_swagger_json()
        self.api_info = self.extract_api_information(self.swagger_json)

    def fetch_api_docs(self):
        pass

    
    def _get_class_name(self):
        return self._class_name

    def _get_dataset_name(self):
        return self._dataset_name
    
    def fetch_swagger_json(self):
        print(self.auth)
        response = requests.get(self.swagger_url,
                                headers=self.headers,
                                auth=self.auth)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch Swagger JSON. Status code: {response.status_code}")
            return None
    
    def dereference_schema(self,ref, definitions):
        """
        Dereference a $ref pointer to fetch the actual schema from definitions.
        
        :param ref: The $ref string.
        :param definitions: The Swagger definitions section.
        :return: The dereferenced schema.
        """
        if not ref.startswith("#/definitions/"):
            return {}
        ref_name = ref.split("/")[2]
        return definitions.get(ref_name, {})

    def extract_param_type(self,param, definitions):
        """
        Extract the type of a parameter from Swagger data.
        
        :param param: The Swagger parameter data.
        :param definitions: The Swagger definitions section.
        :return: The parameter type and description and item type
        to take care of the case where parameter type is array
        """
        # Direct type from parameter
        param_items = ''
        param_type = param.get('type')
        param_description = param.get('description', '')
        if param_type == 'array':
            param_items = param.get('items', '')
        # If not found, look inside the schema
        if 'schema' in param:
            schema = param['schema']
            if '$ref' in schema:
                schema = self.dereference_schema(schema['$ref'], definitions)
            param_type = schema.get('type', param_type)
            param_description = schema.get('description', param_description)
            
        return param_type or 'unknown', param_description, param_items
    
    def extract_api_information(self,swagger_data):
        api_info = []
        
        definitions = swagger_data.get('definitions', {})
    #    api_info_description = swagger_data.get('info', {}).get('description', '')

        paths = swagger_data.get('paths', {})
        for path, methods in paths.items():
            for method, details in methods.items():
                function_name = details.get('operationId', method + path.replace("/", "_"))
            
                # Extract parameters, their types, and descriptions
                params = details.get('parameters', [])
                properties = {}
                required = []
                for param in params:
                    param_type, param_description, param_items = self.extract_param_type(param, definitions)
                    if param_type == 'array':
                        properties[param['name']] = {'type': param_type, 'description': param_description, 'items': param_items}
                    else:
                        properties[param['name']] = {'type': param_type, 'description': param_description}
                    if param.get('required'):
                        required.append(param['name'])
                summary = details.get('summary')
                # Prioritize the description from the 'info' section
                description = details.get('description', '')
                tags = details.get('tags', [])

                api_info.append({
                    'name': function_name,
                    'description': description if description else summary,
                    'parameters': {
                        'type': 'object',
                        'properties': properties,
                        'required': required
                    },
                    'summary': summary,
                    'path': path,
                    'tags': tags
                })
                
        return api_info
    
