from flask import Flask, request
import json
import os
import subprocess
from aski.flask_servers import requests_files

 #######
 # Create Server with different endpoints:
 # It takes in fields from the yaml file and creates server with those properties.
 # Endpoints are :
 # GET directory
 # POST default_file
 # GET model1 name
 # GET model2 name
 # GET running_model_name
 # GET default_model1 name
 # GET most_recent_metrics
 # POST summary  (with file)
 # POST search
 # POST selected_file
 # POST index_files / pre-process it
 # POST upload_user_file
 # GET/POST state
 # GET/POST function (either benchmarking/comparing)
 #######

 #server_config = {}

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


def create_app(server_config):
    app = Flask(__name__)

    @app.route('/', methods=['GET'])
    def default():
        nonlocal server_config
        return "Working API server"

    @app.route('/data', methods=['GET'])
    def get_data():
        nonlocal server_config
        return json.dumps({'data': server_config['data']})

    @app.route('/set_dataset_file', methods=['POST'])
    def set_filename():
        nonlocal server_config
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
            status = json_input_validators(data, ['filename'])
            if 'Error' in status.keys():
                print('Error! Ignoring wrong request')
                return {'Status': status['Error']}
            try:
                f = open(server_config['data']
                          ['DATA_PATH']+'/'+data['filename'], 'r')
                f.read()
            except:
                print('Selected file does not exist in dataset')
                return {'Status': 'Error! Incorrect filename in dataset!'}
            server_config['data']['DEFAULT'] = data['filename']
            return {'Status': 'OK'}
        else:
            return {'Status': 'Error! Content-Type not supported!'}

    @app.route('/upload_user_file', methods=['POST'])
    def upload_userfile():
        nonlocal server_config
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            data = request.json
            status = json_input_validators(data, ['filename', 'filecontents'])
            if 'Error' in status.keys():
                return {'Status': status['Error']}
            try:
                content_string = data['filecontents']
                decoded = content_string
                #decoded = base64.b64decode(content_string).decode("utf-8")

                FILES_DATA_PATH = server_config['data']['FILES_PATH']

                f_path = FILES_DATA_PATH + "/" + data['filename']

                f = open(f_path, "w")
                f.write(decoded)
                f.close()
                server_config['states']['has_input_file'] = True
                server_config['states']['has_indexed'] = False
            except:
                print('Selected file does not exist in dataset')
                return {'Status': 'Error! Incorrect filename in dataset!'}
            server_config['data']['DEFAULT'] = data['filename']
            return {'Status': 'OK'}
        else:
            return {'Status': 'Error! Content-Type not supported!'}

    @app.route('/feedback', methods=['POST'])
    def feedback():
        # request.json['feedback']
        return {}, 200
    
    """
    dataset-related
    
    """


    @app.route('/files/all_datasets', methods=['GET'])
    def all_datasets(): 
        nonlocal server_config
        return requests_files.all_datasets(request, server_config)

    @app.route('/files/file', methods=['GET'])
    def file(): 
        nonlocal server_config
        return requests_files.file(request, server_config)

    @app.route('/files/initialize', methods=['POST'])
    def change_my_name(): 
        pass # Add imported function here!

    @app.route('/files/upload', methods=['POST', 'DELETE'])
    def upload():
        nonlocal server_config
        return requests_files.upload(request, server_config)



    """
    model-related
    
    """


    @app.route('/models/all_models', methods=['GET'])
    def change_my_name(): 
        pass # Add imported function here!
    
    @app.route('/models/model', methods=['GET'])
    def change_my_name(): 
        pass # Add imported function here!    

    @app.route('/models/initialize', methods=['POST'])
    def change_my_name(): 
        pass # Add imported function here!


    @app.route('/models/kill', methods=['POST'])
    def change_my_name(): 
        pass # Add imported function here!

    @app.route('/models/summary', methods=['GET'])
    def change_my_name(): 
        pass # Add imported function here!

    @app.route('/models/search', methods=['GET'])
    def change_my_name(): 
        pass # Add imported function here!

    @app.route('/models/search/file', methods=['GET'])
    def change_my_name(): 
        pass # Add imported function here!

    @app.route('/models/benchmark', methods=['GET'])
    def change_my_name(): 
        pass # Add imported function here!
    
    
    
    return app

