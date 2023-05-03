import copy,os
from flask import Flask
from flask_restful import Resource, Api
from backend.server.core.views import Default, Models
from backend.config import TestingConfig,ProductionConfig,DevelopmentConfig
from backend.server.utils.helpers import get_list_objects
from backend.server.routes import routes
from flasgger import Swagger

def run_app_server(app, port=3000, ip='0.0.0.0'):

    print("PID:", os.getpid())
    print("Werkzeug subprocess:", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("Inherited FD:", os.environ.get("WERKZEUG_SERVER_FD"))
    app.run(debug=False, host=ip, port=port)

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

    - 'data' : {'DATA_PATH', 'DATA_SETS', 'DEFAULT', 'FILES_PATH'} <-- rework this! 
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


def create_app(server_config,config_class=TestingConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app)
    swagger = Swagger(app)

    # Initialize Flask extensions here

    tasks_list = server_config['function']['task'].split('/')
    server_config['model_objs'] = {}
    if 'profiling' in server_config['function']:
        os.environ['ASKI_PROFILING'] = str(
            server_config['function']['profiling'])
    else:
        # Default
        os.environ['ASKI_PROFILING'] = "false"

    for task in tasks_list:
        server_config['model_objs'][task] = get_list_objects(
            server_config['models_' + task], task, 'models')

    server_config['dataset_objs'] = get_list_objects(
        server_config['datasets'], server_config['function']['task'], 'datasets')
    server_config['processes'] = {}

    initial_server_config = copy.deepcopy(server_config)
    print("(create_app) > Server config is ", server_config)

    
    app.config.update(
        server_config=server_config  
    )

    for route in routes:
        api.add_resource(route["resource"],*route["endpoint"])
    
    # api.add_resource(Default, '/',resource_class_kwargs={'server_config':server_config})


    return app

