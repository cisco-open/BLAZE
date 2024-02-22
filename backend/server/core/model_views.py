import json
from glob import glob
import os
import os.path as path
import string
from flask_restful import Resource, request
from flask import current_app
from backend.params.specifications import Specifications
from backend.server.utils.helpers import get_model_object_from_name,get_object_from_name
from backend.utils import make_request
from backend.config import TestingConfig

class ModelsList(Resource):
    
    def get(self):
        """
        List all available models
        ---
        tags:
          - Model Endpoints
        responses:
          200:
            description: Lists all the available models 
            schema:
              properties:
                models_summarization:
                  type: array
                  items:
                    string: string
                
                models_search:
                    type: array
                    items:
                      string: string
        """
        specs = Specifications(current_app.config.get("MODELS_DIR"), current_app.config.get("DATASETS_DIR"))
        return {'models_summarization': specs._list_models_summarization, 'models_search': specs._list_models_search}      
        



class ModelDetail(Resource):

    def get(self):
        """
        Model Details
        ---
        tags:
          - Model Endpoints
        parameters:
          - name: model
            in: query
            description: Enter the name of the model
            required: true
            schema:
              type: string
        responses:
          200:
            description: successful operation
            schema:
              properties:
                model_info:
                  type: object
                  properties:
                    type: string
                    description: model info.
        """

        query_params = request.args

        if any(param not in query_params for param in ['model']):
            return "Malformed request", 400

        model_name = str(query_params['model'])
        app_config = current_app.config.get("server_config")
        for task in app_config["function"]["task"]:
          for model in app_config['model_objs'][task]:
            if model._info['class_name'] == model_name:
                return {'model_info': model._info}, 200

        return "That model doesn't exist", 404


class ModelInitilize(Resource):
    
    def post(self):
        """
        Model Initilize
        ---
        tags:
          - Model Endpoints
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                model:
                  type: string
                  example: ElasticBERT
                filename:
                  type: string
                  example: red-riding-hood.txt
                filecontent:
                  type: string
                  example: There was once a sweet little maid who lived with her father and mother in a pretty little cottage at the edge of the village. At the further end of the wood was another pretty cottage and in it lived her grandmother.
        responses:
          200:
            description: successful operation
            schema:
              properties:
                response:
                  type: string
                  
        """
        request_json = request.json
        print(request_json)
        if any(param not in request_json for param in ['model']):
            return "Malformed request", 400

        model_name = str(request_json['model'])
        model = get_model_object_from_name(model_name, 'search', current_app.config.get("server_config"))

        if not model:
            return "That model doesn't exist", 404

        if callable(getattr(model, "load_model", None)):

            if 'from_file' in request.json:
              filepaths = glob(
                  path.join(current_app.config.get("FILES_DIR"), '**', request_json['from_file']), recursive=True)

              if len(filepaths) > 0:
                  filepath = filepaths[0]
                  with open(filepath, 'r') as f:
                      content = f.read()
                      size = os.path.getsize(filepath) / 1000
              model.load_model(str(request_json['from_file']), content)
            else:             

              model.load_model(str(request_json['filename']), str(request_json['filecontent']))
            print("INITIALIZEED THE FOLLOWING MODEL", model)

        return {"response": "success"}, 200

class ModelSummary(Resource):

    def post(self):
        """
        Model Summarization
        ---
        tags:
          - Model Endpoints
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                model:
                  type: string
                  example: Bart
                content:
                  type: string
                  example: There was once a sweet little maid who lived with her father and mother in a pretty little cottage at the edge of the village. At the further end of the wood was another pretty cottage and in it lived her grandmother.
        responses:
          200:
            description: successful operation
            schema:
              properties:
                response:
                  type: string
                  
        """

        request_json = request.json
      

        model_name = request_json['model']
        
        if 'from_file' in request.json:
            filepaths = glob(
                path.join(current_app.config.get("FILES_DIR"), '**', request_json['from_file']), recursive=True)

            if len(filepaths) > 0:
                filepath = filepaths[0]
                with open(filepath, 'r') as f:
                    content = f.read()
                    size = os.path.getsize(filepath) / 1000
                text_to_summarize = content
        else:
            text_to_summarize = request_json['content']
            
        model = get_model_object_from_name(
            model_name, 'summarization', current_app.config.get("server_config"))
        print(model)
        summarized_text = model._summarize_text(text_to_summarize)

        return {'result': summarized_text}, 200
    
class ModelActionables(Resource):

    def post(self):
        """
        Model Actionables
        ---
        tags:
          - Model Endpoints
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                model:
                  type: string
                  example: OpenAI
                content:
                  type: string
                  example: There was once a sweet little maid who lived with her father and mother in a pretty little cottage at the edge of the village. At the further end of the wood was another pretty cottage and in it lived her grandmother.
        responses:
          200:
            description: successful operation
            schema:
              properties:
                response:
                  type: string
                  
        """

        request_json = request.json
      

        model_name = request_json['model']
        
        if 'from_file' in request.json:
            filepaths = glob(
                path.join(current_app.config.get("FILES_DIR"), '**', request_json['from_file']), recursive=True)

            if len(filepaths) > 0:
                filepath = filepaths[0]
                with open(filepath, 'r') as f:
                    content = f.read()
                    size = os.path.getsize(filepath) / 1000
                processed_text = content
        else:
            processed_text = request_json['content']
            
        model = get_model_object_from_name(
            model_name, 'actionables', current_app.config.get("server_config"))
        print(model)
        actionables = model.get_actionables(processed_text)

        return {'result': actionables}, 200

class ModelSearch(Resource):

    def post(self):
        """
        Model Search
        ---
        tags:
          - Model Endpoints
        parameters:
          - in: body
            name: body
            schema:
              type: object
              properties:
                model:
                  type: string
                  example: ElasticBERT
                query:
                  type: string
                  example: With whome did sweet little maid lived with?
        responses:
          200:
            description: successful operation
            schema:
              properties:
                result:
                  type: string
                latency:
                  type: string
                  
        """
        print(current_app.config.get("server_config"))

        request_json = request.json
        if any(param not in request_json for param in ['model', 'query']):
            return "Malformed request", 400

        model_name = request_json['model']
        query = request_json['query']

        query = query.translate(string.punctuation)

        model = get_model_object_from_name(model_name, 'search', current_app.config.get("server_config"))
        print("SEARCHING THE FOLLOWING MODEL", model)

        res, latency = model.file_search(query)

        return {'result': res, 'latency': latency}, 200
    

class GetFunctionsFromSwaggerData(Resource):

    def post(self):
        request_json = request.json
        if any(param not in request_json for param in ['model', 'dataset', "description_text"]):
            return "Malformed request", 400
        
        model_name = request_json['model']
        model = get_model_object_from_name(model_name, 'functions', current_app.config.get("server_config"))
        dataset_name = request_json['dataset'] 
        dataset_obj = get_object_from_name(dataset_name, current_app.config.get("server_config"), 'dataset')
        description_text = request_json['description_text']
        """Get by data"""
        functions, swagger_data, tag_dict, classifier_tag = model.translate_swagger_data(dataset_obj,description_text)

        response = {
            "functions": functions,
            "swagger_data": swagger_data,
            "tag_dict": tag_dict,
            "classifier_tag":classifier_tag
        }

        filepath = path.join(current_app.config.get("FILES_DIR"), "functions.json")
        print(filepath)
        with open(filepath, "w") as outfile:
          json.dump(response, outfile)

        return response
    
class RunWithFunctions(Resource):
    
    def post(self):
        request_json = request.json
        if any(param not in request_json for param in ['model']):
            return "Malformed request", 400
        filepath = open(path.join(current_app.config.get("FILES_DIR"), "functions.json"))
        data = json.load(filepath)
        model_name = request_json['model']
        model = get_model_object_from_name(model_name, 'functions', current_app.config.get("server_config"))
        messages = request_json['messages']
        response = model.run_with_functions(messages,data["tag_dict"]['dashboard-controller'])
        return response
    
class CallFunction(Resource):
    
    def post(self):
        request_json = request.json
        yaml_config = TestingConfig.db.get(TestingConfig.DBConfig.type == 'yaml_config')
        auth_type = yaml_config["config"]["Swagger"]["auth_type"]
        request_type = request_json["request_type"]
        url = request_json["url"]
        config = yaml_config["config"]["Swagger"]
        data = request_json.get("data",None)
        params = request_json.get('params',None)

        response = make_request(auth_type, request_type, url,config,params,data)
        print(response.text)
        return response.json()
    
       
    
        