import dash_bootstrap_components as dbc
from dash import html, dcc

from aski.params.parameters import Parameters
from aski.dash_files.app_constants import *
from aski.dash_files.app_helpers import *

from aski.dash_files.search.elements_search import SearchInterface
from aski.dash_files.summarization.elements_summarization import SummarizationInterface 

# === Returns the sidebar. No customization needed (no inputs) === #

def get_sidebar(params):

    sidebar = html.Div([

        html.Center(html.P(
            params._data_dict['Title'], className="lead", style={'color': CREAM, 'font-size': 23, 'font-weight': "bold", 'font-family': "Quicksand"}
        )),
        html.Br(),

        html.P("""Kindly select a model:
                """, style={'color': WHITE, 'font-family': "Quicksand"}
               ),

        dbc.Card([
            html.Div(
                [
                    get_custom_model_checklist(params._data_dict['states']['model_objs'])
                ]),

        ], color="dark", style={"padding": "1rem", 'font-family': "Quicksand"}),


        html.Br(),
        html.P("""Then, choose from a dataset or upload a file:""", style={'color': WHITE, 'font-family': "Quicksand"}
               ),

        dbc.Card([
            html.Div(
                [
                    html.Center(dcc.Upload(dbc.Button('Upload File (.txt)', color="info", outline=True, style={
                               'font-family': "Quicksand"}), id="sidebar-file-button")),
                ]),

        ], color="dark", style={"padding": "1rem"}),

        html.Br(),

        html.P("""Finally, choose from one of the functions below. 😄""", style={'color': WHITE, 'font-family': "Quicksand"}
               ),

        dbc.Card([
            html.Div(
                [
                    get_custom_functions_checklist(params._data_dict['function'])
                ]
            )
        ], color="dark", style={"padding": "1rem"}),

        html.Br(),

        dbc.Card([
            html.Div(
            [
                html.Center(dbc.Button('Reset Dash', color="info", outline=True, style={'font-family':"Quicksand"}, id='sidebar-reset-button')), 
            ]),
            
        ], color="dark", style={"padding":".8rem"}),

        html.Br(),
        html.Center(dbc.Row(dbc.Col(html.Img(src=CISCO_LOGO,
                    height="90px", style={"margin-bottom": "15px"})))),
        html.Center(html.B(html.A("Join Cisco Research Labs", href=CISCO_LINK,
                    target="_blank", style={'color': TEAL, 'font-family': "Quicksand"}))),

    ],
        style=SIDEBAR_STYLE,
    )
    return sidebar



def get_custom_model_checklist(list_models):

    list_options = []

    for model in list_models:

        model_name       = model._info['name']
        model_class_name = model._info['class_name']
        option = {

        "label": model_name,
        "value": model_class_name

        }

        list_options.append(option)

    check_list = dbc.Checklist(
        options=list_options,
        value=[],
        id="sidebar-models-checklist",
        switch=True,
        style={'color':WHITE, "padding": "0rem",
        'font-family':"Quicksand"},
    )

    return check_list



def get_custom_functions_checklist(functions): 
    list_options = [] 

    for func in functions:
        if func == 'task': continue 
        if func == 'custom' : 
            list_options.append({"label": "Custom Demo", "value": "Custom Demo"})

        if func == 'benchmarking': 
            list_options.append({"label": "Solo Benchmark", "value": "Solo Benchmark"})

        if func == "comparing": 
            list_options.append({"label": "Model Comparison", "value": "Model Comparison"})

    return dbc.RadioItems(
                options=list_options ,
                value=list_options[0]['value'],
                id="sidebar-function-radioitems",
                style={'color':WHITE, "padding": "0rem", 
                        'font-family':"Quicksand"}
            )
                    


# === Returns the content (abstracts, determines which page) === #

def get_content(params):

    task = params._data_dict['function']['task']

    if task == 'search': 
        page = SearchInterface(params)
         
    
    elif task == 'summarization': 
        page = SummarizationInterface(params)
         
    
    elif task == "search/summarization": 
        pass 

    return page.get_page()
