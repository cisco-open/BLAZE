import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import numpy as np
import os
from os.path import splitext


import requests

from aski.dash_files.app_constants import DATA_PATH, FILES_PATH
from aski.flask_servers.flask_constants import PORT_REST_API, PREF_REST_API
from aski.utils.helpers import read_file

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

    server_files = {} 
    for dataset in params._data_dict['datasets']: 
        request = f"{PREF_REST_API}{PORT_REST_API}/files/all_files"
        response = requests.get(request, json={'dataset':dataset})

        server_files[dataset] = response.json()['files']

    options = [] 
    for entry in server_files: 

        # Add an unclickable option for it to look nicer
        options.append({"label": f"-- {entry} Files --", "disabled": True})

        files_list = server_files[entry]
        for i in range(len(files_list)):
            options.append(
                {"label": files_list[i], "value": f"{entry}|{files_list[i]}"})

    return options

# === (Misc Help) Returns text of a file in preview format === #

# TODO: consolidate the two (REST API and PDF reader ones) 

def gen_filePreview(filename, fileclass):

    request = f"{PREF_REST_API}{PORT_REST_API}/files/file"
    print(f"filename: {filename}, fileclass: {fileclass}")

    # Fileclass is simply the dataset class (ex. Squad, user)
    response = requests.get(request, json={'filename':filename, 'fileclass':fileclass})

    file_content = response.json()['content']
    file_size = response.json()['size'] # <-- only for user files, if not then "N/A" (in KB)

    preview = f"Preview of File: {len(file_content)} chars, {len(file_content.split())} words, {file_size} kilobytes"
    return preview, file_content
    

def gen_filePreview_Path(path):

    file_name = os.path.basename(path)

    # TODO: REST API - Given a file choice, return text, size, and length information 
    file_name, file_extension = splitext(file_name)

    if file_extension == '.txt':

        f = open(path, "r")

        # read the content of file
        data = f.read()

        # "Preview of File: 17825 chars, 2772 words, 17.3 kilobytes"
        preview = f"Preview of File: {len(data)} chars, {len(data.split())} words, {os.path.getsize(path)/1000} kilobytes"

        return preview, data

    elif file_extension == '.pdf':

        data = read_file(path)

        preview = f"Preview of File: {len(data)} chars, {len(data.split())} words, {os.path.getsize(path)/1000} kilobytes"

        return preview, data

