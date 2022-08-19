from re import A
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from dash import dcc, html

from dash.dependencies import Input 

from drag.constants import *
import subprocess 
import socket 



"""

Layout is defined as: 

title
design_layout (cytoscape), warning_messages
design_buttons, node_info, schema_display 

"""

""" Title Card contains the title (fixed) """

def get_title(): 
    title_card = dbc.Row([
                    dbc.Col([
                        html.Center(dbc.Button("Flexible Natural Language Pipeline - Builder", color="info", outline=True, style={'font-family': "Quicksand", "font-size": "50px", "padding": "1rem", "margin-top": "1rem", "margin-bottom":"1rem"}))

                    ], width=8), 
                    dbc.Col([
                        html.Div(
                                [
                                    dbc.Button('Learn More', id=str(DesignID.BTN_ADD_DATA), n_clicks=0, color="info", outline=True, style={"padding": "1rem", "margin-top": "1rem"}),
                                    dbc.Button('Info - Models',
                                            id=str(DesignID.BTN_REMOVE_ELMT),
                                            n_clicks=0, color="info", outline=True, style={"padding": "1rem", "margin-top": "1rem"}),
                                    dbc.Button(
                                        'Info - Data', id=str(DesignID.BTN_CONNECT_NODES), n_clicks=0, color="info", outline=True, style={"padding": "1rem", "margin-top": "1rem"}),
                                    dbc.Button('Contribute', id=str(DesignID.BTN_BUILD_SCHEMA), n_clicks=0, color="info", outline=True, style={"padding": "1rem", "margin-top": "1rem"})
                                ],
                                className="d-grid gap-1 d-md-flex"
                                )
                    ], width=4)
                ])

    return title_card 


""" Design layout rendering contains the CYTOSCAPE """

def get_cytoscape(): 

    design_layout_rendering = dbc.Card([
        cyto.Cytoscape(
        id=str(DesignID.DESIGN_INTERFACE),
        # Possible layouts are (though not all seem to work):
        #     "random", "preset", "circle", "concentric",
        #     "grid", "breadthfirst", "cose", "close-bilkent"
        #     "cola", "euler", "spread", "dagre", "klay"
        layout={'name': 'grid'},
        stylesheet=[
            {
                'selector': 'node',
                'style': {
                    'background-color': '#CA8EB0',
                    'label': 'data(label)',
                }
            }, 
            {
                'selector': '[id *= "Model"]',
                'style': {
                    'background-color': 'black',
                    'shape' : 'triangle',
                    'label': 'data(label)',
                }
            }, 
            {
                'selector': 'edge',
                'style': {
                    'background-color': '#5EB5C9',
                    'label': 'data(label)',
                }
            },
            {
                'selector': 'label',
                'style': {
                    'label': 'data(label)',
                    'color':'white',
                }
            }, 
            {
                'selector': ':selected',
                'style': {
                    'background-color': 'red',
                    'label': 'data(label)',
                    'color':'white',
                }
            }
        ],
        style={
            'width': '100%',
            'height': '450px'
        },
        elements=[])
    ], 
    outline=True, 
    color="#049FD911",
    style={"color": "dark"})

    return design_layout_rendering


""" Contains any warning/error messages... """

def get_warning(): 

    important_info = dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "7rem"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'margin-top': '1rem', 'font-family': "Quicksand", "height":"15rem","vertical-align": "middle"}
            ) 
    return important_info 


""" Contains all buttons for cytoscape functionality """

def get_buttons(): 
    design_layout_buttons = dbc.Card([html.Div(
        [
            dbc.Button('Insert - Model', id=str(DesignID.BTN_ADD_MODEL), n_clicks=0),
            dbc.Button('Insert - Data', id=str(DesignID.BTN_ADD_DATA), n_clicks=0),

            dbc.Button('Connect', id=str(DesignID.BTN_CONNECT_NODES), n_clicks=0, style={'margin-left':'33px'}),
            dbc.Button('Delete', id=str(DesignID.BTN_REMOVE_ELMT), n_clicks=0),

            dbc.Button(dcc.Upload(id=str(DesignID.BTN_UPLOAD_SCHEMA), children=html.Div([html.A('Upload')]), style={'color':CREAM}), style={'margin-left':'33px'}),
            dbc.Button('Build', id=str(DesignID.BTN_BUILD_SCHEMA), n_clicks=0, style={'color':CREAM})
        ],
        className="d-grid gap-1 d-md-flex justify-content-md-end")
    ], outline=True, color="#049FD911", style={"color": "dark"})

    return design_layout_buttons


""" Contains schema display (outputted YAML) """

def get_schema(path=None): 

    placeholder = html.Center(html.H6
            (
                f"Generated YAML will be shown here",
                    style={"font-family": "Quicksand",
                        "color": CREAM, 'font-size': "22px"}
                    ),
                    style={"margin-top": "7rem"})

    if path: 
        # Means that we have a yaml file at path: path
        
        cmd = f"python run.py {path}"
        print(f"Running command: {cmd}")
        subprocess.run(cmd)


        # Now that the server's running, we need to get the link at which it's running... 

        host = socket.gethostbyname(socket.gethostname())

        link = "http://127.0.0.1:" + "/5001"
        print(f"Opening link at {link}")

        placeholder = html.Center(dbc.Button("Open Dash", href=link, color="success", outline=True, style={'font-family': "Quicksand", "font-size": "30px", "padding": "1rem", "margin-top": "8rem", "margin-bottom":"1rem"}))



    design_layout_schema_display = dbc.Card([
        placeholder
    ], outline=True, 
    color="#049FD911",
    style={"color": "dark", 'height':'15rem', 'overflow': 'auto', 'margin-top':'1rem'})

    return design_layout_schema_display 


""" Contains the info display (upon clicking smth) """

def get_cyto_card(): 

    node_info_card = html.Div(
            children=[
                html.Br(),
                dbc.InputGroup(
                    [
                        dbc.InputGroupText('Title'),
                        dbc.Input(placeholder="Please enter pipeline title here...", id=str(DesignID.INPUT_DESIGN_TITLE),
                                  debounce=True)
                    ],
                    className="mb-3",
                ),
                 dbc.InputGroup(
                    [
                        dbc.InputGroupText('YAML'),
                        dbc.Input(placeholder="Please enter yaml file title here...", id=str(DesignID.INPUT_YAML_TITLE),
                                  debounce=True)
                    ],
                    className="mb-3",
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Tabs(
                            id=str(DesignID.TABS_DESIGN),
                            children=[
                                dbc.Tab(label="Element(s)",
                                        tab_id=str(DesignID.TAB_NODE_PROPERTY_VALUE), tabClassName="flex-grow-1 text-center"),
                                dbc.Tab(label="Connection(s)",
                                        tab_id=str(DesignID.TAB_EDGE_PROPERTY_VALUE), tabClassName="flex-grow-1 text-center")
                            ],
                        )),
                    dbc.CardBody(children=[get_node_model_card(), get_node_data_card(), get_edge_card()])
                ]),
            ]
        )

    return node_info_card 


def get_node_model_card(): 

    dropdown_items = dropdown_models_items
    label = "Models"
    placeholder = "Please select a model from the dropdown..."

    node_tab_content = html.Div(
    id=str(DesignID.TAB_NODE_MODEL_CONTENT),
    children=[
        dbc.InputGroup(
            [
                dbc.DropdownMenu(children=dropdown_items, label=label),
                dbc.Input(id=str(DesignID.INPUT_MODEL_DISPLAY_ELEMENT), placeholder=placeholder),

            ],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.InputGroupText('Description'),
                dbc.Textarea(id=str(DesignID.TEXTAREA_MODEL_NODE_DESCRIPTION)),
            ],
            className="mb-3",
        ),
    ],
    style={'display': 'none'})

    return node_tab_content  

def get_node_data_card(): 

    dropdown_items = dropdown_data_items
    label = "Data"
    placeholder = "Please select a dataset from the dropdown..."

    node_tab_content = html.Div(
        id=str(DesignID.TAB_NODE_DATA_CONTENT),
        children=[
            dbc.InputGroup(
                [
                    dbc.DropdownMenu(children=dropdown_items, label=label),
                    dbc.Input(id=str(DesignID.INPUT_DATA_DISPLAY_ELEMENT), placeholder=placeholder),

                ],
                className="mb-3",
            ),
            dbc.InputGroup(
                [
                    dbc.InputGroupText('Description'),
                    dbc.Textarea(id=str(DesignID.TEXTAREA_DATA_NODE_DESCRIPTION)),
                ],
                className="mb-3",
            ),
        ],
        style={'display': 'none'})

    return node_tab_content 




def get_edge_card(): 
    edge_tab_content = html.Div(
    id=str(DesignID.TAB_EDGE_CONTENT),
    children=[
        dbc.InputGroup([
            dbc.InputGroupText('Name'),
            dbc.Input(id=str(DesignID.INPUT_EDIT_EDGE_LABEL), debounce=True)
        ],
                       className="mb-3"),
        dbc.Row([
            dbc.Col(dbc.Switch(id=str(DesignID.TOGGLE_CUSTOM),
                label='Custom',
                value=False)),
            dbc.Col(dbc.Switch(id=str(DesignID.TOGGLE_BENCHMARK),
                    label='Benchmark',
                    value=False)),
            dbc.Col(dbc.Switch(id=str(DesignID.TOGGLE_COMPARISON),
                label='Comparison',
                value=False)),
        ])
    ],
    style={'display': 'none'})

    return edge_tab_content 


"""This implements layouts for design pane."""


"""
Design_layout is the element that stitches all the components together 
"""

design_layout = html.Div([
    
    dbc.Row([
        get_title(), 
        dbc.Col([
            get_cytoscape(), 
            get_warning(), 
        ], width=8), 
        dbc.Col([
            get_buttons(), 
            get_cyto_card(), 
            html.Div(id=str(DesignID.SCHEMA_PANE), children=[get_schema()]), 
        ], width=4),
        dcc.Download(id=str(DesignID.DOWNLOAD_FILE)),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0,
        )
    ])
], 
style={'background-color': '#222222', 'height': '60rem', 'width': '100%', 'padding':'1rem'})
