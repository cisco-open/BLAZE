import json
from flask_restful import Resource, Api, fields, marshal_with
from flask import current_app,request


class Default(Resource):
    
    def get(self):
        """
        This is an example
        ---
        tags:
          - Basic
        responses:
          200:
            description: Returns message if api is working
            schema:
              id: Basic
              properties:
                response:
                  type: string
                  default: Working API server
        """
        print(current_app.config)
        return {'response': "Working API server"}, 200

    def post(self):
        print(current_app.config)
        return {'response': "Working API server"}, 200

class ResetServer(Resource):
    def __init__(self,**kwargs):
        self.server_config = kwargs['server_config']
        self.initial_server_config = kwargs['initial_server_config']
    
    def get(self):
        self.server_config = self.initial_server_config
        return {'response': "reset successful"}, 200

class Models(Resource):
    def get_select_model_options(self,list_models, task):
        list_options = []

        for model in list_models:
            model_name = model._info['name']
            model_class_name = model._info['class_name']
            option = {
                "label": ' ' + model_name,
                "value": str(model_class_name),
            }

            list_options.append(option)

        return [list_options, task]

    def get(self):
        list_models = []
        list_tasks = []
        for key in current_app.config["server_config"]['model_objs']:
            list_models.append(current_app.config["server_config"]['model_objs'][key])
            list_tasks.append(key)

        select_model_options = []
        print(list_models)
        for i in range(len(list_models)):
            select_model_options.append(
                self.get_select_model_options(list_models[i], list_tasks[i]))
        print(select_model_options)
        return {'data': select_model_options}


