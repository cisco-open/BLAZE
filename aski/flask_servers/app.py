from flask import Flask, request
import json
import os
import subprocess

from aski.flask_servers import requests_files
from aski.flask_servers import requests_models 
from aski.utils.helpers import get_list_objects


"""

500 - internal server error
400 - bad request
404 - not found
200 - successful

states to retain: 
- yaml file (nonlocal server_config)
    o add models (indexed or not) to this 
    o for each model process, have pid and other related info

"""


def run_app_server(app, port=3000, ip='localhost'):

    print("PID:", os.getpid())
    print("Werkzeug subprocess:", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("Inherited FD:", os.environ.get("WERKZEUG_SERVER_FD"))
    app.run(host=ip, port=port)

def json_input_validators(input_data, fields_to_be_present):
    for f in fields_to_be_present:
        if f not in input_data.keys():
            return {'Error': f'Error!! {f} key missing in input data'}
    return {'Success': '0'}


def create_server_config(data): 
    # Input: data dictionary (yaml file) 
    # TODO: Implement this function! 

  
    """
    
    Things we can cut out of server_config: 

    - 'Title'
    - 'function'

    Things that are currently in server_config: 

    - 'datasets' " [d1_name]
    - 'models' : ['m1_name']
    - 'model_objs' : [m1_obj]

    What server_config should eventually look like: 

    - 'data_names' : ['Squad', 'CNN Dailymail', 'User Files']
    - 'data_objs' : [Squad.py obj, CNNDailyMail.py obj, UserFiles.obj]
    - 'model_names' : [ElasticBERT, T5]
    - 'model_objs' : [ElasticBERT.py obj, T5.py obj]
    - 'processes' : {'ElasticBERT' : [Process, Queue, Res]}
    
    """

    return data

def create_app(server_config):

    app = Flask(__name__)

    # Initialize models by storing the models in a list in server config
    server_config['model_objs'] = get_list_objects(server_config['models'], server_config['function']['task'], 'models') 
    server_config['dataset_objs'] = get_list_objects(server_config['datasets'], server_config['function']['task'], 'datasets') 
    server_config['processes'] = {}

    print("(create_app) > Server config is ", server_config)
  

    # 01) General methods. 
    
    @app.route('/', methods=['GET'])
    def default():
        nonlocal server_config
        return {'response' : "Working API server"}, 200 

    @app.route('/data', methods=['GET'])
    def get_data():
        nonlocal server_config
        return json.dumps({'data': server_config['data']})
    

    # 02) Dataset methods.

    @app.route('/files/all_datasets', methods=['GET'])
    def all_datasets(): 
        nonlocal server_config
        return requests_files.all_datasets(request, server_config)


    @app.route('/files/all_files', methods=['GET'])
    def all_files(): 
        nonlocal server_config
        return requests_files.all_files(request, server_config)

    @app.route('/files/file', methods=['GET'])
    def file(): 
        nonlocal server_config
        return requests_files.file(request, server_config)

    @app.route('/files/load', methods=['POST'])
    def load(): 
        nonlocal server_config
        return requests_files.load(request, server_config)

    @app.route('/files/upload', methods=['POST', 'DELETE'])
    def upload():
        nonlocal server_config
        return requests_files.upload(request, server_config)

    @app.route('/files/yaml', methods=['POST'])
    def generate_dash():
        nonlocal server_config
        return requests_files.generate_dash(request, server_config)



    # 03) Model methods.

    @app.route('/models/all_models', methods=['GET'])
    def all_models(): 
        nonlocal server_config
        return requests_models.all_models(request, server_config)

    @app.route('/models/model', methods=['GET'])
    def model(): 
        nonlocal server_config
        return requests_models.model(request, server_config)

    @app.route('/models/initialize', methods=['POST'])
    def initialize(): 
        nonlocal server_config
        return requests_models.initialize(request, server_config)

    @app.route('/models/summary', methods=['GET'])
    def summary(): 
        nonlocal server_config
        return requests_models.summary(request, server_config)

    @app.route('/models/search', methods=['GET'])
    def search(): 
        nonlocal server_config
        return requests_models.search(request, server_config)

    @app.route('/models/search/file', methods=['GET'])
    def search_file(): 
        nonlocal server_config
        return requests_models.search_file(request, server_config)

    @app.route('/models/benchmark', methods=['GET'])
    def benchmark(): 
        nonlocal server_config
        return requests_models.benchmark(request, server_config)
    
    @app.route('/models/kill', methods=['POST'])
    def kill(): 
        nonlocal server_config
        return requests_models.kill(request, server_config)
    
    return app

