import copy,os
from flask import Flask
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
import multiprocessing
# from backend.server.app import app,socketio
from flask_restful import Resource, Api
from backend.server.core.views import Default, Models
from backend.config import TestingConfig,ProductionConfig,DevelopmentConfig
from backend.server.utils.helpers import get_list_objects
from backend.models.common.ElasticBERT import ElasticBERT
from backend.models.interfaces.model_search import squad_benchmarkV2
from backend.server.routes import routes
from flasgger import Swagger
from gevent import monkey,sleep
from threading import Event
import time
import multiprocessing as mp

thread_event = Event()
transcripts = mp.Queue()

loaded_classes = {}

# monkey.patch_all()
def run_app_server(app,socketio, port=3000, ip='0.0.0.0'):
    
    print("PID:", os.getpid())
    print("Werkzeug subprocess:", os.environ.get("WERKZEUG_RUN_MAIN"))
    print("Inherited FD:", os.environ.get("WERKZEUG_SERVER_FD"))
    # app.run(debug=False, host=ip, port=port)
    socketio.run(app,host=ip,port=port,debug=False)

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
    CORS(app) # This will enable CORS for all routes
    socketio = SocketIO(app,cors_allowed_origins="*") 
    app.config["transcriptsQueue"] = transcripts
    if "module" in server_config:
        app.config.update(allowed_modules=config_class.yaml_allowed_moduls(server_config.get("module",None)))
    app.config.from_object(config_class)
    api = Api(app)
    swagger = Swagger(app)
    frontend_config = copy.deepcopy(server_config)
    frontend_config.update(config_class.public_config())
    tasks_list = server_config['function']['task']
    server_config['model_objs'] = {}
    if 'profiling' in server_config['function']:
        os.environ['ASKI_PROFILING'] = str(
            server_config['function']['profiling'])
    else:
        # Default
        os.environ['ASKI_PROFILING'] = "false"

    for task in tasks_list:
        server_config['model_objs'][task] = get_list_objects(
            server_config['models_' + task], 'common', 'models')
        
    if 'datasets' in server_config:
        server_config['dataset_objs'] = get_list_objects(
            server_config['datasets'], 'common', 'datasets')
        server_config['processes'] = {}

    initial_server_config = copy.deepcopy(server_config)
    print("(create_app) > Server config is ", server_config)


    app.config.update(
        frontend_config=frontend_config,
        server_config=server_config  
    )

    for route in routes:
        api.add_resource(route["resource"],*route["endpoint"],endpoint=route.get("endpointName",None))
    
    # api.add_resource(Default, '/',resource_class_kwargs={'server_config':server_config})

    @socketio.on('connect')
    def test_connect():
        emit('response', {'data': 'Connected'})
    
    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    @socketio.on('benchmark')
    def benchmark(data):
        print(data)
        emit('benchmark',{"response":"Starting elastic model"})
        socketio.sleep(1)
        file = data["file"]
        model_obj = server_config["model_objs"]["search"][0]        
        squad_benchmarkV2(file_name=file,model_obj=model_obj,sio=socketio,channel="benchmark")
    
    @socketio.on('benchmark2')
    def benchmark2(data):
        print(data)
        emit('benchmark',{"response":"Starting elastic model"})
        socketio.sleep(1)
        file = data["file"]
        model_obj = server_config["model_objs"]["search"][0]        
        squad_benchmarkV2(file_name=file,model_obj=model_obj,sio=socketio,channel="benchmark2")
        

    return app,socketio

