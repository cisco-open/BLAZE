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
class Config(Resource):
    
    def get(self):
        
        print(current_app.config)
        return {'response': current_app.config.get('frontend_config')}, 200

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

import imp
import importlib
from flask import jsonify

class TestDynamicApis(Resource):
    loaded_classes = {}
    loaded_modules = {}

    def load_module(self):
        data = request.json
        module_name = data.get('module_name')
        class_name = data.get('class_name',None)

        try:
            module = importlib.import_module(module_name)
            if class_name:
                class_ = getattr(module, class_name)
                instance = class_(data.get('init_data', {}))  # Initialize class with data
                self.loaded_classes[class_name] = instance
            if module:
                self.loaded_modules[module_name] = module
            return jsonify({"message": f"Module '{module_name}' loaded and class '{class_name}' initialized."})
        except Exception as e:
            return jsonify({"error": str(e)})
    
    def invoke_function(self):
        data = request.json
        class_name = data.get('class_name',None)
        module_name = data.get('module_name')
        print(module)
        method_type = data.get('method_type')
        method_name = data.get('method_name')
        args = data.get('args', [])
        input_data = data.get('input_data', None)
        try:
            if method_type == "module_function":
                module = self.loaded_modules[module_name]
                if hasattr(module, method_name):
                        method = getattr(module, method_name)
                        if input_data is not None:
                            result = method(*args, input_data=input_data)
                        else:
                            result = method(*args)
                        return jsonify({"result": result})
        except Exception as e:
            return jsonify({"error": str(e)})

        try:
            if class_name in self.loaded_classes:
                instance = self.loaded_classes[class_name]
                if hasattr(instance, method_name):
                    method = getattr(instance, method_name)
                    if input_data is not None:
                        result = method(*args, input_data=input_data)
                    else:
                        result = method(*args)
                    return jsonify({"result": result})
                else:
                    return jsonify({"error": f"Method '{method_name}' not found in class '{class_name}'."})
            else:
                return jsonify({"error": f"Class '{class_name}' not found."})
        except Exception as e:
            return jsonify({"error": str(e)})


    def post(self):
        data = request.json
        class_name = data.get('class_name')
        module_name = data.get('module_name')
        method_type = data.get('method_type')
        method_name = data.get('method_name')
        args = data.get('args', [])
        input_data = data.get('input_data', None)
        self.load_module()
        print(self.loaded_modules)
        try:
            if method_type == "module_function":
                    module = self.loaded_modules[module_name]
                    print(module)
                    if hasattr(module, method_name):
                            method = getattr(module, method_name)
                            print(method)
                            if input_data is not None:
                                result = method(*args, input_data=input_data)
                            else:
                                result = method(*args)
                            return jsonify({"result": result})
            if class_name in self.loaded_classes:
                instance = self.loaded_classes[class_name]
                if hasattr(instance, method_name):
                    method = getattr(instance, method_name)
                    if input_data is not None:
                        result = method(*args, input_data=input_data)
                    else:
                        result = method(*args)
                    return jsonify({"result": result})
                else:
                    return jsonify({"error": f"Method '{method_name}' not found in class '{class_name}'."})
            else:
                return jsonify({"error": f"Class '{class_name}' not found."})
        except Exception as e:
            return jsonify({"error": str(e)})
