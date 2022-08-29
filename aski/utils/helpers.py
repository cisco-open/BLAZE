from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc
from importlib import import_module
import yaml

from aski.dash_files.app_constants import CREAM, WHITE

def get_list_objects(list_objects_str, task, object_type):
    """ 
    Function that takes as input a list of strings of the models we want to use
    for the dashboard and that returns a list of the different models as 
    objects.
    Parameters
    ----------
    list_models_str : list of Strings
      List of the models we want to use for the dashboard as Strings
    Returns
    -------
    list_models_obj : list of Model objects
        List of the models we want to use for the dashboard as Objects
    """

    list_objects = []

    for object_name in list_objects_str:
      object_var = call_object_class_from_name(object_name, task, object_type)
      
      list_objects.append(object_var)

    return list_objects

def call_object_class_from_name(object_name, task, object_type):

    # Get the class as a variable
    object_class = import_module(
        "aski." + object_type + '.' + task + '.' + object_name).__getattribute__(object_name) 

    # Call the class
    object_var = object_class()
    return object_var

def get_object_from_name(object_name, params, object_type):

    object_active = object_name
    current_object = None 

    for object_iter in params._data_dict['states'][object_type + '_objs']:
        object_name = object_iter._get_class_name()

        if object_name == object_active:
            current_object = object_iter

    return current_object

def dump_yaml(data, path):

    with open(path, mode="wt", encoding="utf-8") as file:
        yaml.dump(data, file)

def get_current_model(params):

    model_active = params._data_dict['states']['model_active'][0]
    current_model = None 

    for model in params._data_dict['states']['model_objs']:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model

def get_dataset_object_from_name(dataset_name, data_dict): 

    # TODO: Consolidate this and "get_model_object_from_name"

    model_active = dataset_name
    current_model = None 

    for model in data_dict['dataset_objs']:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model


def get_model_object_from_name(model_name, data_dict):

    model_active = model_name
    current_model = None 

    for model in data_dict['model_objs']:
        model_name = model._get_class_name()

        if model_name == model_active:
            current_model = model

    return current_model

def get_metrics_tables(params):

    metrics_results = params._data_dict['states']['metrics_results']
    metrics_used    = params._data_dict['states']['metric_objs']

    dash_elements = []

    for i in range(len(metrics_used)):

        # Get the metric name and the associated dictionnary
        metric_name   = metrics_used[i]._class_name
        pre_dict      = metrics_results[i]

        # Keep only the keys specified in the class
        metric_keep   = metrics_used[i]._metric_keys
        metric_result = {k: pre_dict[k] for k in metric_keep if k in pre_dict}

        # Round the metrics
        metric_result = {k : round(metric_result[k], 3) for k in metric_result}
        metric_name   = metrics_used[i]._class_name


        table = dash_table.DataTable(
            data=[metric_result], 
            id='tbl' + str(i),
            cell_selectable=False,
            column_selectable=False,
            style_header = {'background-color': '#049FD911', 'color': CREAM, 
            'textAlign': 'center', 'font-size': 20, 'font-weight': "bold", 'font-family': "Quicksand"},
            style_cell   = {'background-color': '#049FD911', 'color': WHITE, 
            'textAlign': 'left',   'font-size': 20, 'font-weight': "bold", 'font-family': "Quicksand"}
            )

        dash_element = dbc.Col([
                            html.H6(metric_name, style={"font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem", 'text-align': 'center'}),
                            table,
                            html.Br(),
                        ], width=15, style={"background": "#049FD911", "color": WHITE, "font-family": "Quicksand", "padding": "1rem"}, align="center")

        dash_elements.append(dash_element)

    return dash_elements

