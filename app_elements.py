"""

This file stores most of the elements utilized by the ASKI Dashboard. 
All functions (as well as their descriptions) are listed below: 

High-Level Functions: 

    get_sidebar() - generates the sidebar for the dashboard 
    get_content() - highest function, returns page layout
    get_benchmark_content() - returns page layout for solo benchmarking
    get_comparison_content() - returns page layout for model comparison 

Custom Q/A Functions: 

    get_titleCard() - returns title (ex. ColBERT or Elasticsearch)
    get_inputBox() - returns left panel (choose file, preview, start)
    get_outputBox() - returns right panel (enter Q, print A, display stats)
    get_latencyCard() - child of get_outputBox, shows time taken by model 
    get_accuracyCard() - child of get_outputBox, shows overall accuracy 


"""

import dash_bootstrap_components as dbc
from dash import html, dcc

from app_constants import * 
from app_helpers import * 


"""

The following four functions are high-level functions. 

Dependency hirearchy is: 
- ASKI Dashboard --> [get_sidebar, get_content]
- get_content --> [get_benchmark_content, get_comparison_content]

"""

# === Returns the sidebar. No customization needed (no inputs) === #

def get_sidebar(): 

    sidebar = html.Div([

        html.Center(html.P(
            SIDEBAR_TEXT, className="lead", style={'color':CREAM, 'font-size':23,'font-weight':"bold",'font-family':"Quicksand"}
        )),
        html.Br(), 
        
        html.P("""Kindly select a method below. 
                """, style={'color':WHITE, 'font-family':"Quicksand"}
            ),

            dbc.Card([
                html.Div(
                [
                    dbc.RadioItems(
                        options=[
                            {"label": "ColBERT", "value": 1, "disabled": True}, # Currently transferring 
                            {"label": "Elastic", "value": 2},
                            {"label": "K-Graph", "value": 3, "disabled": True}, # Currently implementing 
                        ],
                        value=2,
                        id="input-radioitems-model",
                        style={'color':WHITE, "padding": "0rem",},
                    ),
                ]),
                
            ], color="dark", style={"padding":"1rem", 'font-family':"Quicksand"}),
           
            
            html.Br(), 
            html.P("""Then, choose from a SQUAD dataset or upload your file.""", style={'color':WHITE, 'font-family':"Quicksand"}
            ),

            dbc.Card([
                html.Div(
                [
                    dcc.Upload(dbc.Button('Upload File (.txt, .pdf)', color="info", outline=True, style={'font-family':"Quicksand"}), id="input-button-file"),
                ]),
                
            ], color="dark", style={"padding":"1rem"}),

            html.Br(),

            html.P("""Finally, ask questions or run the provided benchmark. 😄""", style={'color':WHITE, 'font-family':"Quicksand"}
            ),
            
            dbc.Card([
                html.Div(
                    [
                        dbc.Checklist(
                            options=[
                                {"label": "Custom Questions", "value": 1},
                                {"label": "Solo Benchmark", "value": 2},
                                {"label": "Model Comparison", "value": 3},
                            ],
                            value=[1],
                            id="input-switches-data",
                            switch=True,
                            style={'color':WHITE, "padding": "0rem", 'font-family':"Quicksand"}
                        ),
                    ]
                )
            ], color="dark", style={"padding":"1rem"}),    
        
            html.Br(),
            html.Br(),
            html.Center(dbc.Row(dbc.Col(html.Img(src=CISCO_LOGO, height="90px", style={"margin-bottom": "15px"})))),
            html.Center(html.B(html.A("Join Cisco Research Labs", href=CISCO_LINK, target="_blank", style={'color':TEAL, 'font-family':"Quicksand"}))),

        ],
        style=SIDEBAR_STYLE,
    )
    return sidebar; 



# === Returns the content (abstracts, determines which page) === #

def get_content(data, pQueue=None, pQueue1=None): 

    # Return model comparison page 
    if data["comparing"]: 
        return get_comparison_content(data, pQueue, pQueue1)

    # Return solo benchmark page 
    elif data["benchmarking"]: 
        return get_benchmark_content(data, pQueue)

    # Return custom Q/A page (default) 
    else: 
        return html.Div(
                    html.Div([
                        get_titleCard(data['model']['title']),
                        dbc.Row([ 
                            dbc.Col(get_inputBox(data)),
                            dbc.Col(get_outputBox(data))
                        ])
                    ], 
                    style=CONTENT_STYLE), 
                id="custom-content")



# === Returns the content of the solo benchmarking page === #

def get_benchmark_content(data, pQueue): 

    return html.Div(html.Div([
        dbc.Row([
            dbc.Col([
                get_squadTitleCard(data), 
                html.Div(get_squadMetricsCard(data, pQueue), id="progress-content")
            ], width=4), 
            dbc.Col([
                html.Div(get_squadIncorrectCard(data), id="incorrect-content")
            ]), 
            dcc.Interval(
                id='interval-component',
                interval=1*1000, # in milliseconds 
                n_intervals=0,
            )
        ])
    ], style=CONTENT_STYLE), id="squad-content")



# === Returns the content of the multi-pane comparison page === #

def get_comparison_content(data, pQueue0, pQueue1): 
        return html.Div(html.Div([
        get_compareTitleCard(data), 
        dbc.Row([
            dbc.Col([
                html.Div(get_compareMetricsCard(data, pQueue0, "ColBERT"), id="progress-content0"),
                html.Div(get_compareIncorrectCard(data, "ColBERT"), id="incorrect-content0")

            ]), 
            dbc.Col([
                html.Div(get_compareMetricsCard(data, pQueue1, "Elastic"), id="progress-content1"),
                html.Div(get_compareIncorrectCard(data, "Elastic"), id="incorrect-content1")

            ]),
            dcc.Interval(
                id='compare-interval-component',
                interval=1*1000, # in milliseconds 
                n_intervals=0,
            )
        ])
    ], style=CONTENT_STYLE), id="compare-content")



"""

The following five functions are used for the custom Q/A page. 

Dependency hirearchy is:
- Custom Q/A Page --> [get_titleCard, get_inputBox, get_outputBox]
- get_outputBox --> [get_latencyCard, get_accuracyCard]

"""

# === (Custom Q/A) Returns the titlecard. Text changes based on model === #

def get_titleCard(modelText): 
    titleCard = html.Center(
        dbc.Button(modelText, color="info", outline=True, style={'font-family':"Quicksand", "font-size":"50px", "padding":"1rem", "margin-bottom":"2rem"},
    ))
    return titleCard 



# === (Custom Q/A) Returns the inputbox card === #

def get_inputBox(data): 

    preview = "Kindly choose a file in order to preview it"
    file_txt = None 
    placeholder = "Please choose an input file:"

    if data['states']['has_input_file']: 
        preview, file_txt = gen_filePreview(data['states']['chosen_name'], data['states']['chosen_path'])
        placeholder = data['states']['chosen_name']


    inputBox = dbc.Card([
                dbc.CardBody([
                        html.Center(html.H5("Input Text(s)", style={"font-family":"Quicksand", "color":CREAM,'font-size':"30px", "padding":"1rem"})),

                        dbc.Row([
                            dbc.Col([
                                html.H6
                                (
                                        "Please choose an input file:", 
                                        style={"font-family":"Quicksand", "color":WHITE, 'font-size':"22px","padding":"1rem"}
                                ),
                            ], width=6), 
                            dbc.Col([
                                dbc.Select(
                                    id="input-file",
                                    options=gen_inputOptions(data['inputs']),
                                    style={"background":"#888888", "color":WHITE, "font-family":"Quicksand"},
                                    placeholder=placeholder 
                                ),
                            ])
                        ], align="center"),

                        html.H6
                        (
                                "New options can be added via \"Upload File\" from the sidebar.", 
                                style={"font-family":"Quicksand", "font-style":"italic","color":WHITE, 'font-size':"22px","padding":"1rem"}
                        ),

                        html.Br(), 

                        dbc.Card([
                                html.H5(preview),
                                html.Br(),
                                html.P(file_txt, style={"color":WHITE, "overflow":"auto", "height":"12rem"}),
                                
                            ],
                            style={"background":"#88888822", "color":WHITE, "font-family":"Quicksand", "padding":"1rem"} 
                        ),
                    
                        html.Br(), 
                        html.Br(),

                        html.Center(dbc.Button(f'Begin {data["model"]["name"]} Indexing', color="info", outline=True, id="input-indexing", style={'font-size':"26px",'font-family':"Quicksand"}))          
                ],
                className="mb-3",
                style={"width": "100%", "height" : "42rem"},
            ),
        ],
        outline=True, 
        color="#049FD911",
        style={"color":"dark"}
    )
    return inputBox 



# === (Custom Q/A) Returns the model's output === #

def get_outputBox(data): 
    outputBox = dbc.Card([
            dbc.CardBody([
                    html.Center(html.H5("Question-Answering", style={"font-family":"Quicksand", "color":CREAM,'font-size':"30px", "padding":"1rem"})),

                    dbc.Card([
                        html.Div(
                        [
                            dbc.Row([
                                dbc.Col(dbc.Input(
                                    className="mb-3", placeholder=data['states']['q_placeholder'], id="input-qbox", style={"color":WHITE, "background":"#88888822"}
                                ), width=10),
                                dbc.Col(dbc.Button('Ask Q', color="info", outline=True, id="input-qbutton", style={'font-family':"Quicksand"}))
                            ]),
                            dbc.Alert(
                                html.H6(data['states']['a_placeholder'], 
                                        style={'text-align':'right', "color":WHITE}
                                ), 
                                color="#88888822"
                            )
                        ]),
                        
                    ], color="#88888822", style={"padding":"1rem", 'font-family':"Quicksand"}),

                    html.Br(), 

                    dbc.Row([
                        dbc.Col([
                            get_latencyCard(data['metrics'])
                        ]), 
                        dbc.Col([
                            get_accuracyCard(data['metrics'], data['model'])
                        ])
                    ]),

                ],
                className="mb-3",
                style={"width": "100%", "height" : "42rem"},
            ),
        ],
        outline=True, 
        color="#049FD911",
        style={"color":"dark"}
    )
    return outputBox 



# === (Custom Q/A) Returns the latency card === #

def get_latencyCard(metrics): 

    table_header = [
        html.Thead(html.Tr([html.Th("Step"), html.Th("Time (s)")]))
    ]

    row1 = html.Tr([html.Td("Load"), html.Td(metrics["latency"][0])])
    row2 = html.Tr([html.Td("Index"), html.Td(metrics["latency"][1])])
    row3 = html.Tr([html.Td("Search"), html.Td(metrics["latency"][2])])
    

    table_body = [html.Tbody([row1, row2, row3])]

    table = dbc.Table(table_header + table_body, bordered=True, style={"color":WHITE})

    latencyCard = dbc.Card([
        html.Div(
        [
            html.Center(html.H5("Latency", style={"font-family":"Quicksand", "color":CREAM,'font-size':"30px", "padding":"1rem"})),
            table,
            html.Br(),
            html.H5(f"Number of GPUs: {metrics['num_GPUs']}", style={"font-family":"Quicksand", "color":WHITE}),
            html.H5(f"Search Time Avg: {metrics['search_avg']}", style={"font-family":"Quicksand", "color":WHITE})
        ]),
        
    ], color="#88888822", style={"padding":"1rem", 'font-family':"Quicksand", "height":"24rem"}
    )

    return latencyCard



# === (Custom Q/A) Returns the accuracy card === #

def get_accuracyCard(metrics, model): 
    
    row21 = html.Tr([html.Td("% Correct"), html.Td(f"{metrics['accuracy'][0]} %")])
    row22 = html.Tr([html.Td("Avg Time"), html.Td(f"{metrics['accuracy'][1]} s")])
    
    table2_body = [html.Tbody([row21, row22])]
    table2 = dbc.Table(table2_body, bordered=True, style={"color":WHITE})


    accuracyCard = dbc.Card([
        html.Div(
        [
            html.Center(html.H5("Accuracy", style={"font-family":"Quicksand", "color":CREAM,'font-size':"30px", "padding":"1rem"})),
            html.Center(html.H5("Tested on SQUAD questions (only for SQUAD datasets)", style={"font-family":"Quicksand", "color":WHITE, "padding":"0rem 0rem 1rem 0rem"})),
            table2,
            html.Br(), 
            html.Center(html.H5(html.A(f"Learn more about {model['name']}.", href=model['l_info'], target="_blank", style={"font-family":"Quicksand", "color":WHITE}))),
            html.Center(html.H5(html.A(f"View {model['name']} Github Repo.", href=model['l_repo'], target="_blank", style={"font-family":"Quicksand", "color":WHITE})))

        ]),
        
    ], color="#88888822", style={"padding":"1rem", 'font-family':"Quicksand", "height":"24rem"}
    ) 
    return accuracyCard 
