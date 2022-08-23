import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import numpy as np
import os

import requests

from aski.dash_files.app_constants import DATA_PATH, FILES_PATH

def get_object_options(params, object_type):

    object_names = []
    objects = params._data_dict['states'][object_type + '_objs']
    
    for object_iter in objects:
        object_name = object_iter._get_class_name()
        object_names.append(object_name)

    options = []

    for i in range(len(object_names)):
        options.append(
            {"label": object_names[i], "value": object_names[i]})

    return options

def get_dataset_options(params):

    dataset_names = []
    datasets = params._data_dict['states']['dataset_objs']
    
    for dataset in datasets:
        dataset_name = dataset._get_class_name()
        dataset_names.append(dataset_name)

    options = []

    for i in range(len(dataset_names)):
        options.append(
            {"label": dataset_names[i], "value": dataset_names[i]})

    return options

def gen_inputOptions(params):

    print(f"(gen_inputOptions) > Entering function, seeing what is available...")

    server_files = {} 

    PORT_REST_API = 3000 # TODO: Make this a global constant! 
    request = f"http://127.0.0.1:{PORT_REST_API}/files/all_datasets"

    response = requests.get(request)
    print(f"(run_app) > Received response: {response}, {response.json()}")

    # TODO: this is only for search datasets at the moment!

    for dataset in response.json()['datasets_search']: 
        print(f"Getting all files from {dataset}...")
        request = f"http://127.0.0.1:{PORT_REST_API}/files/all_files"

        response = requests.get(request, json={'dataset':dataset})
        #print(f"(run_app) > Received response: {response}, {response.json()}")

        server_files[dataset] = response.json()['files']


    # TODO: REST API - Get and Display all File Options (Datasets + Uploaded Files)

    # HARDCODED SINCE WE WILL BE USING SQUAD FOR NOW 

    #     data:
    #   DATA_PATH: ./data/squad2_data
    #   DATA_SETS: '1'
    #   DEFAULT: 1973_oil_crisis
    #   FILES_PATH: ./data/user_files

    DATA_PATH = './data/squad'
    FILES_PATH = './data/user_files'

    n_squad, p_squad = [], []
    datasets = [dir[0] for dir in os.walk(DATA_PATH)]


    for dir in datasets[1:]:
        name = dir.split("/")[-1]
        n_squad.append(name.replace("_", " "))
        p_squad.append(dir + "/story.txt")

    n_user, p_user = [], []

    datasets = [dir for dir in os.listdir(FILES_PATH)]

    for dir in datasets:
        n_user.append(dir)
        p_user.append(FILES_PATH+ "/" + dir)


    files = {
        'n_squad': n_squad,
        'p_squad': p_squad,
        'n_user': n_user,
        'p_user': p_user
    }

    options = []

    # Add an unclickable option for it to look nicer
    options.append({"label": "-- User files --", "disabled": True})

    # Add the user files
    for i in range(len(files['n_user'])):
        options.append(
            {"label": files['n_user'][i], "value": files['p_user'][i]})

    # Add an unclickable option for it to look nicer
    options.append({"label": "-- Squad files (Local) --", "disabled": True})

    # Add the Squad files
    for i in range(len(files['n_squad'])):
        options.append(
            {"label": files['n_squad'][i], "value": files['p_squad'][i]})
    
    # TODO: Consolidate/fix these (hacky solution for now, will fix in next commit)

    #get_file_request_prefix = f"http://127.0.0.1:{PORT_REST_API}/files/file"

    for entry in server_files: 

        # Add an unclickable option for it to look nicer
        options.append({"label": f"-- {entry} files (Server) --", "disabled": True})

        files_list = server_files[entry]
        # Add the Squad files
        for i in range(len(files_list)):
            options.append(
                {"label": files_list[i], "value": files_list[i]})


    return options


# === (Misc Help) Returns text of a file in preview format === #
def gen_filePreview(name, path):

    # TODO: REST API - Given a file choice, return text, size, and length information 

    f = open(path, "r")

    # read the content of file
    data = f.read()

    # "Preview of File: 17825 chars, 2772 words, 17.3 kilobytes"
    preview = f"Preview of File: {len(data)} chars, {len(data.split())} words, {os.path.getsize(path)/1000} kilobytes"
    return preview, data
    