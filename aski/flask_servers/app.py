from flask import Flask, request
import json

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
            json = request.json
            data = json.loads(json)
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
            json = request.json
            data = json.loads(json)
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

    return app
