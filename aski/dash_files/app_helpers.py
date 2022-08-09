"""

This file stores all other elements utilized by the ASKI Dashboard.
All functions (as well as their descriptions) are listed below:

Comparing Models Page

    get_compareTitleCard(data) - titles of models and option to choose SQUAD dataset
    get_compareMetricsCard(data, pQueue, m_name) - shows progress, accuracy, latency
    get_compareIncorrectCard(data, m_name) - shows all incorrectly-answered Q's
    get_compare_spinnyCircle() - helper function to be shown while model is starting


Solo Benchmark Page

    get_squadTitleCard(data) - titles of chosen model and option to choose SQUAD dataset
    get_squadMetricsCard(data, pQueue) - shows progress, accuracy, and latency
    get_squadIncorrectCard(data) - shows all incorrectly-ansswered Q's
    get_squadTimeGraph(data) - generates graph of time taken vs. question #


Miscellaneous Helpers

    get_inputOptions(files) - merges squad files with user files
    get_filePreview(name, path) - given path, returns text of file
    initialize_data() - intializes the data dictionary used by app
    get_spinnyCircle() - returns a simple spinny circle for loading

"""


import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.express as px
import numpy as np
import os

from aski.dash_files.app_constants import *



"""

The following four functions are miscellaneous helpers.

"""

# === (Misc Help) Merges SQUAD files with user-uploaded files === #


def gen_inputOptions(params):

    n_squad, p_squad = [], []
    datasets = [dir[0] for dir in os.walk(params._data_dict['data']['DATA_PATH'])]

    for dir in datasets[1:]:
        name = dir.split("/")[-1]
        n_squad.append(name.replace("_", " "))
        p_squad.append(dir + "/story.txt")

    n_user, p_user = [], []
    datasets = [dir for dir in os.listdir(params._data_dict['data']['FILES_PATH'])]

    for dir in datasets:
        n_user.append(dir)
        p_user.append(params._data_dict['data']['FILES_PATH']+ "/" + dir)

    files = {
        'n_squad': n_squad,
        'p_squad': p_squad,
        'n_user': n_user,
        'p_user': p_user
    }

    options = []

    for i in range(len(files['n_user'])):
        options.append(
            {"label": files['n_user'][i], "value": files['p_user'][i]})

    for i in range(len(files['n_squad'])):
        options.append(
            {"label": files['n_squad'][i], "value": files['p_squad'][i]})

    return options


# === (Misc Help) Returns text of a file in preview format === #

def gen_filePreview(name, path):

    f = open(path, "r")

    # read the content of file
    data = f.read()

    # "Preview of File: 17825 chars, 2772 words, 17.3 kilobytes"
    preview = f"Preview of File: {len(data)} chars, {len(data.split())} words, {os.path.getsize(path)/1000} kilobytes"
    return preview, data


# === (Misc Help) Initializes the data dictionary used throughout === #

def __get_data():
    return {
        'Function': 'Search',
        'benchmarking': False,
        'comparing': False,
        'model': {
            'name': "ColBERT",
            'title': "ColBERT - Scalable BERT-Based Search",
                    'l_info': "https://arxiv.org/abs/2004.12832",
                    'l_repo': "https://github.com/stanford-futuredata/ColBERT"
        },
        'data': {
            "DATA_PATH": "./data/squad2_data",
            "FILES_PATH": "./data/user_files",
            "DATA_SETS": "1",  # Use * for all Squad Datasets,
            "DEFAULT": "1973_oil_crisis"
        },
        'states': {
            'has_input_file': False,
            'has_indexed': False,
            'chosen_name': None,
            'chosen_path': None,
            'm_in_use': 1,
            'q_placeholder': "Once the input has been indexed, ask away...",
            'a_placeholder': "... and the output will be shown here!"
        },
        'metrics': {
            'latency': [-1, -1, -1],
            'search_avg': -1,
            'num_GPUs': 1,
            'accuracy': [-1, -1]
        },

    }


def initialize_data(data=None):
    if not data:
        data = __get_data()
        
    DATA_PATH = data["data"]["DATA_PATH"]
    FILES_PATH = data["data"]["FILES_PATH"]
    DATA_SETS = data["data"]["DATA_SETS"]
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
        p_user.append(FILES_PATH + "/" + dir)

    dummy_results = {
        "name": None,
        "root": None,
        "questions": {
            "num_qf": len([]),
            "num_qs": 0,
            "all_qs": [],
            "tot_qs": 0,
        },
        "times": {
            "avg_ts": 0,
            "all_ts": [],
        },
        "metrics": {
            "correct_arr": [],
            "incorrect_d": {},
            "accuracy_num": 0,
            "accuracy_prc": 0,
        }
    }
    data['inputs'] = {
        'n_squad': n_squad,
        'p_squad': p_squad,
        'n_user': n_user,
        'p_user': p_user
    }

    data['squad'] = {
        'has_input_file': False,
        'chosen_name': None,
        'chosen_path': None,
        'has_indexed': False,
        'metrics_window': {

        },
        'incorrect_window': {

        },
        'begun_queue': False,
        'old_results': {
            "ColBERT": dummy_results,
            "Elastic": dummy_results,
        }
    }
    return data


# === (Misc Help) Returns a spinny circle for loading screens === #

def get_spinnyCircle():
    return dbc.Card([
        html.Div(
            [
                html.Center(dbc.Spinner(color="info", spinner_style={
                            "width": "3rem", "height": "3rem"}), style={"margin-top": "50%"})
            ])
    ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
    )
