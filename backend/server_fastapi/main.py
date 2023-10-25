import json
import os
import copy
import yaml
import backend.server_fastapi.state as state
from fastapi import FastAPI
import argparse
from backend.server_fastapi.config import TestingConfig,ProductionConfig,DevelopmentConfig
from backend.server.utils.helpers import get_list_objects
from backend.server_fastapi.routers import dataset_views, model_views
from werkzeug.utils import import_string

def from_object(state, obj):
        if isinstance(obj, str):
            obj = import_string(obj)
        for key in dir(obj):
            if key.isupper():
                state[key] = getattr(obj, key)

yaml_file = os.getenv("yaml")

with open(yaml_file, mode="rt", encoding="utf-8") as file:
    server_config = yaml.safe_load(file)

config_class = TestingConfig

if "module" in server_config:
        state.state.update(allowed_modules=config_class.yaml_allowed_moduls(server_config.get("module",None)))

from_object(state.state,config_class)

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

state.state.update(
        frontend_config=frontend_config,
        server_config=server_config  
    )
app = FastAPI()
app.include_router(dataset_views.router)