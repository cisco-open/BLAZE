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

The following four functions are for the Comparing Models page.

"""

# === (Compare Ms) Returns the top models/data choosing card === #


def get_compareTitleCard(data):

    default = data['squad']['chosen_name']
    if default is None:
        default = data['data']['DEFAULT']

    return dbc.Card([
        html.Div(
            [
                dbc.Row([
                    dbc.Col([
                        html.Center(html.H5("ColBERT vs Elastic", style={
                                    "font-family": "Quicksand", "color": TEAL, 'font-size': "40px", "padding": "0.5rem"})),
                    ], width=5),
                    dbc.Col([

                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.H6
                                    (
                                        "Please choose a SQUAD dataset (same for both):",
                                        style={"font-family": "Quicksand", "color": WHITE,
                                               'font-size': "22px", "padding": "0rem"}
                                    ),
                                ], width=4),
                                dbc.Col([
                                    dbc.Select(
                                        id="compare-squad-file",
                                        options=gen_inputOptions(
                                            data['inputs']),
                                        style={"background": "#888888",
                                               "color": WHITE, "font-family": "Quicksand"},
                                        placeholder=default
                                    ),
                                ], width=3),
                                dbc.Col([
                                    html.Center(dbc.Button(f'Begin Benchmark', color="info", outline=True,
                                                           id="compare-begin-index", style={'font-size': "26px", 'font-family': "Quicksand"}))
                                ]),
                            ], align="center", style={'margin-bottom': "0px"}),
                        ]),
                    ]),

                ])



            ]),

    ],  outline=True,
        color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "6rem", "margin-bottom": "1rem"}
    )


# === (Compare Ms) Returns the progress, accuracy, latency, graph(s) === #

def get_compareMetricsCard(data, pQueue, m_name):

    if not data['squad']['begun_queue'] and pQueue.empty():
        return dbc.Card([
            html.Div(
                [
                    html.Center(html.H6
                        (
                            f"Starting {m_name} model...",
                                style={"font-family": "Quicksand",
                                       "color": CREAM, 'font-size': "22px"}
                                ),
                                style={"margin-top": "12rem"})
                ])
        ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "26rem", "vertical-align": "middle"}
        )
    else:
        data['squad']['begun_queue'] = True

    try:
        results = pQueue.get_nowait()
        print("1")
        data['squad']['old_results'][m_name] = results

    except:
        results = data['squad']['old_results'][m_name]

    num_correct = results["metrics"]["correct_arr"].count(1)
    num_total = results["questions"]["num_qs"]
    num_curr = results["questions"]["tot_qs"]
    avg_time = round(np.mean(results["times"]["all_ts"]), 2)
    progress = round(100.0 * num_curr / (num_total+0.01), 2)

    results = data['squad']['old_results'][m_name]
    accuracy = round(100 * np.mean(results["metrics"]["correct_arr"]), 2)

    return dbc.Card([
        html.Div(
            [
                    html.Br(),
                    dbc.Progress(
                        label=f"Progress: {progress}%", value=progress, id="animated-progress", animated=False, striped=True
                    ),
                    html.Br(),
                    dbc.Col([
                        dbc.Row
                        ([
                            html.Br(),
                            dbc.Col(html.H6
                                    (
                                        "Num. Correct (#):",
                                        style={"font-family": "Quicksand",
                                               "color": WHITE, 'font-size': "22px"}
                                    ), width=4),
                            dbc.Col(dbc.Badge(html.H1(num_correct, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),

                            dbc.Col(html.H6
                                    (
                                        "Num Total (#):",
                                        style={"font-family": "Quicksand",
                                               "color": WHITE, 'font-size': "22px"}
                                    ), width=4),
                            dbc.Col(dbc.Badge(html.H1(num_total, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),


                        ]),
                        html.Br(),
                        dbc.Progress(
                            label=f"Accuracy: {accuracy}%", value=accuracy, id="animated-progress", animated=False, striped=True, color="success"
                        ),
                        html.Br(),
                        get_squadTimeGraph(results["times"]["all_ts"]),
                        html.Br(),
                        dbc.Row
                        ([
                            dbc.Col(html.H6
                                    (
                                        "Average time / Question (s):",
                                        style={"font-family": "Quicksand",
                                               "color": CREAM, 'font-size': "22px"}
                                    ), width=9),
                            dbc.Col(dbc.Badge(html.H1(avg_time, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),
                        ]),
                    ]),
                    ])
    ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "26rem"}
    )


# === (Compare Ms) Returns all incorrectly-answered questions in SQUAD data === #

def get_compareIncorrectCard(data, m_name):

    results = data['squad']['old_results'][m_name]
    accuracy = round(100 * np.mean(results["metrics"]["correct_arr"]), 2)

    results = data['squad']['old_results'][m_name]
    incorrect = results['metrics']['incorrect_d']

    accordion_list = []
    for wrong in incorrect:
        m_ans = incorrect[wrong][0]
        q_ans = incorrect[wrong][1]
        contx = incorrect[wrong][2]

        accordion_list.append(
            dbc.AccordionItem(
                f"Model's answer: {m_ans} | Correct answer: {q_ans} \n | \n Context: {contx}", title=wrong,
                style={'font-family': "Quicksand", 'color': WHITE,
                       'background-color': "#049FD911", 'text-color': WHITE}
            )
        )

    item_list = [f"item-{i}" for i in range(len(accordion_list))]

    return dbc.Card([
        html.Div(
            [
                    html.Center(html.H6
                                (
                                    f"Questions answered incorrectly by {m_name} will appear here.",
                                    style={"font-family": "Quicksand", "color": WHITE,
                                           'font-size': "22px", "padding": "1rem"}
                                )),
                    html.Hr(style={"color": WHITE}),
                    dbc.Accordion(
                        accordion_list,
                        start_collapsed=False, always_open=True, active_item=item_list, style={"padding": "1rem", 'font-family': "Quicksand", 'color': "#049FD911", 'background-color': "#049FD911", 'text-color': "#049FD911"}
                    ),
                    ])
    ], color="#88888822", style={"margin-top": "15px", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "overflow": "auto"}
    )


# === (Compare Ms) Returns a spinning circle to be displayed while loading === #

def get_compare_spinnyCircle():
    return dbc.Card([
        html.Div(
            [
                html.Center(dbc.Spinner(color="info", spinner_style={
                            "width": "3rem", "height": "3rem"}), style={"margin-top": "10rem"})
            ])
    ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "24rem", "vertical-align": "middle"}
    )


"""

The following four functions are for the Solo Benchmark page.


"""


# === (Solo Bench) Returns the top model/data choosing card === #

def get_squadTitleCard(data):

    default = data['squad']['chosen_name']
    if default is None:
        default = data['data']['DEFAULT']

    return dbc.Card([
        html.Div(
            [
                html.Center(html.H5(default, style={
                            "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),
                dbc.Row([
                    dbc.Col([
                        html.H6
                        (
                            "Please choose a SQUAD dataset:",
                            style={"font-family": "Quicksand", "color": WHITE,
                                   'font-size': "22px", "padding": "1rem"}
                        ),
                    ], width=6),
                    dbc.Col([
                        dbc.Select(
                            id="squad-file",
                            options=gen_inputOptions(data['inputs']),
                            style={"background": "#888888",
                                   "color": WHITE, "font-family": "Quicksand"},
                            placeholder=default
                        ),
                    ])
                ], align="center", style={'margin-bottom': "10px"}),
                html.Center(dbc.Button(f'Begin {data["model"]["name"]} Benchmark', color="info", outline=True,
                            id="squad-begin-index", style={'font-size': "26px", 'font-family': "Quicksand"}))


            ]),

    ],  outline=True,
        color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "margin-bottom": "1rem"}
    )


# === (Solo Bench) Returns the progress, accuracy, latency, graph(s) === #

def get_squadMetricsCard(data, pQueue):

    if not data['squad']['begun_queue'] and pQueue.empty():
        return dbc.Card([
            html.Div(
                [
                    html.Center(html.H6
                        (
                            "Starting ColBERT model...",
                                style={"font-family": "Quicksand",
                                       "color": CREAM, 'font-size': "22px"}
                                ),
                                style={"margin-top": "50%"})
                ])
        ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
        )
    else:
        data['squad']['begun_queue'] = True

    try:
        results = pQueue.get_nowait()
        print("1")
        data['squad']['old_results'] = results

    except:
        results = data['squad']['old_results']

    percent_correct = round(
        100 * np.mean(results["metrics"]["correct_arr"]), 2)
    num_correct = results["metrics"]["correct_arr"].count(1)
    num_total = results["questions"]["num_qs"]
    num_curr = results["questions"]["tot_qs"]
    avg_time = round(np.mean(results["times"]["all_ts"]), 2)
    progress = round(100.0 * num_curr / (num_total+0.01), 2)

    return dbc.Card([
        html.Div(
            [
                    html.Br(),
                    dbc.Progress(
                        label=f"Progress: {progress}%", value=progress, id="animated-progress", animated=False, striped=True
                    ),
                    html.Br(),
                    dbc.Col([
                        html.Br(),
                        dbc.Row
                        ([
                            dbc.Col(html.H6
                                    (
                                        "Percent Questions Correct (%):",
                                        style={"font-family": "Quicksand",
                                               "color": CREAM, 'font-size': "22px"}
                                    ), width=9),
                            dbc.Col(dbc.Badge(html.H1(percent_correct, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),
                        ]),
                        html.Br(),
                        dbc.Row
                        ([
                            dbc.Col(html.H6
                                    (
                                        "Number Questions Correct (#):",
                                        style={"font-family": "Quicksand",
                                               "color": WHITE, 'font-size': "22px"}
                                    ), width=9),
                            dbc.Col(dbc.Badge(html.H1(num_correct, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),
                        ]),
                        dbc.Row
                        ([
                            dbc.Col(html.H6
                                    (
                                        "Number Questions Total (#):",
                                        style={"font-family": "Quicksand",
                                               "color": WHITE, 'font-size': "22px"}
                                    ), width=9),
                            dbc.Col(dbc.Badge(html.H1(num_total, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),
                        ]),
                        html.Hr(style={"color": WHITE}),
                        get_squadTimeGraph(results["times"]["all_ts"]),
                        html.Br(),
                        dbc.Row
                        ([
                            dbc.Col(html.H6
                                    (
                                        "Average time / Question (s):",
                                        style={"font-family": "Quicksand",
                                               "color": CREAM, 'font-size': "22px"}
                                    ), width=9),
                            dbc.Col(dbc.Badge(html.H1(avg_time, style={
                                "font-family": "Quicksand", 'font-size': "22px"}), color="dark", text_color="primary")),
                        ]),
                    ]),
                    ])
    ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem"}
    )


# === (Solo Bench) Returns all incorrectly-answered questions in SQUAD data === #

def get_squadIncorrectCard(data):
    m_name = data['model']['name']
    results = data['squad']['old_results'][m_name]
    accuracy = round(100 * np.mean(results["metrics"]["correct_arr"]), 2)

    results = data['squad']['old_results'][m_name]
    incorrect = results['metrics']['incorrect_d']

    accordion_list = []
    for wrong in incorrect:
        m_ans = incorrect[wrong][0]
        q_ans = incorrect[wrong][1]
        contx = incorrect[wrong][2]

        accordion_list.append(
            dbc.AccordionItem(
                f"Model's answer: {m_ans} | Correct answer: {q_ans} \n | \n Context: {contx}", title=wrong,
                style={'font-family': "Quicksand", 'color': WHITE,
                       'background-color': "#049FD911", 'text-color': WHITE}
            )
        )

    item_list = [f"item-{i}" for i in range(len(accordion_list))]

    return dbc.Card([
        html.Div(
            [
                    html.Br(),
                    dbc.Progress(
                        label=f"Accuracy: {accuracy}%", value=accuracy, id="animated-progress", animated=False, striped=True, color="success"
                    ),
                    html.Br(),
                    html.Center(html.H6
                                (
                                    "All questions answered incorrectly will appear in the accordion, found below.",
                                    style={"font-family": "Quicksand", "color": WHITE,
                                           'font-size': "22px", "padding": "1rem"}
                                )),
                    html.Br(),
                    dbc.Accordion(
                        accordion_list,
                        start_collapsed=False, always_open=True, active_item=item_list, style={"padding": "1rem", 'font-family': "Quicksand", 'color': "#049FD911", 'background-color': "#049FD911", 'text-color': "#049FD911"}
                    ),
                    ])
    ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand", "height": "24rem", "overflow": "auto"}
    )


# === (Solo Bench) Returns graph of time taken (s) vs. question number === #

def get_squadTimeGraph(data):

    try:
        year = [(i+1) for i in range(len(data))]
        carbon = data

        line = px.line(x=year, y=carbon)
        line.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            xaxis_title="Question Number",
            yaxis_title="Time (s)",
        )

    except:
        year = [0]
        carbon = [0]

        line = px.line(x=year, y=carbon)
        line.update_layout(
            margin=dict(l=0, r=0, b=0, t=0),
            xaxis_title="Question Number",
            yaxis_title="Time (s)",
        )

    return dcc.Graph(id="time-series", figure=line, style={"height": "9rem"})


"""

The following four functions are miscellaneous helpers.

"""

# === (Misc Help) Merges SQUAD files with user-uploaded files === #


def gen_inputOptions(files):

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
