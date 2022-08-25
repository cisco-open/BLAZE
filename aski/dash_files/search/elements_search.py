import dash_bootstrap_components as dbc
from dash import html, dcc

from aski.dash_files.app_constants import *
from aski.dash_files.app_helpers import *


class SearchInterface(): 

    def __init__(self, params):
        self.params = params 

# ==============================================================================
# ================================== PAGES =====================================
# ==============================================================================

    def get_page(self): 
        return self.get_page_custom(self.params)


    def get_page_custom(self, params): 
        
        model_active = params._data_dict['states']['model_active']
        model_objs = [x for x in params._data_dict['states']['model_objs'] if str(x._info['class_name']) in model_active]


        if len(model_objs) == 1: 
            model_title = f"{model_objs[0]._info['desc']}"
        else:
            model_title = "Please select a model from the left."

        return html.Div(
                    html.Div([
                        self.get_titleCard(model_title),
                        dbc.Row([ 
                            dbc.Col(self.get_inputBox(params)),
                            dbc.Col(self.get_outputBox(params))
                        ])
                    ], 
                    style=CONTENT_STYLE), 
                id="custom-content")

         
    def get_page_benchmark(self, params): 

        return html.Div(html.Div([
            dbc.Row([
                dbc.Col([
                    self.get_bench_TitleCard(params),
                    html.Div(self.get_bench_MetricsCard(params), id="search-bench-metrics-content")
                ], width=4),
                dbc.Col([
                    html.Div(self.get_bench_IncorrectCard(params), id="search-bench-incorrect-content")
                ]),
                dcc.Interval(
                    id='search-bench-interval-component',
                    interval=1*1000,  # in milliseconds
                    n_intervals=0,
                )
            ])
        ], style=CONTENT_STYLE), id="bench-content")


    def get_page_comparison(self, params): 

        return html.Div(html.Div([
            self.get_compare_TitleCard(params),
            dbc.Row([
                dbc.Col([
                    html.Div(self.get_compare_MetricsCard(params, 0), id="search-compare-metrics-content-0"),
                    html.Div(self.get_compare_IncorrectCard(params, 0), id="search-compare-incorrect-content-0")

                ]),
                dbc.Col([
                    html.Div(self.get_compare_MetricsCard(params, 1), id="search-compare-metrics-content-1"),
                    html.Div(self.get_compare_IncorrectCard(params, 1), id="search-compare-incorrect-content-1")

                ]),
                dcc.Interval(
                    id='search-compare-interval-component',
                    interval=1*1000,  # in milliseconds
                    n_intervals=0,
                )
            ])
        ], style=CONTENT_STYLE), id="compare-content") 
    

    """

    The following functions are for Custom Search: 
    
    """

    def get_titleCard(self, modelText):
        titleCard = html.Center(
            dbc.Button(modelText, color="info", outline=True, style={'font-family': "Quicksand", "font-size": "50px", "padding": "1rem", "margin-bottom": "2rem"},
                    ))
        return titleCard


    def get_inputBox(self, params):


        preview = "Kindly choose a file in order to preview it"
        file_txt = None
        placeholder = "Please choose an input file:"

        if params._data_dict['states']['has_input_file']:
            preview, file_txt = gen_filePreview(params._data_dict['states']['chosen_path'])
            placeholder = params._data_dict['states']['chosen_data']

        if len(params._data_dict['states']['model_active']) == 0: 
            begin_text = "Please select a model first."
        else: 
            begin_text = f"Begin {params._data_dict['states']['model_active'][0]} Indexing"

        inputBox = dbc.Card([
            dbc.CardBody([
                            html.Center(html.H5("Input Text(s)", style={
                                        "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),

                            dbc.Row([
                                dbc.Col([
                                    html.H6
                                    (
                                        "Please choose an input file:",
                                        style={"font-family": "Quicksand", "color": WHITE,
                                            'font-size': "22px", "padding": "1rem"}
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dbc.Select(
                                        id="search-custom-choose-file",
                                        options=gen_inputOptions(params),
                                        style={
                                            "background": "#888888", "color": WHITE, "font-family": "Quicksand"},
                                        placeholder=placeholder
                                    ),
                                ])
                            ], align="center"),

                            html.H6
                            (
                                "New options can be added via \"Upload File\" from the sidebar.",
                                style={"font-family": "Quicksand", "font-style": "italic",
                                    "color": WHITE, 'font-size': "22px", "padding": "1rem"}
                            ),

                            html.Br(),

                            dbc.Card([
                                html.H5(preview),
                                html.Br(),
                                html.P(file_txt, style={
                                    "color": WHITE, "overflow": "auto", "height": "12rem"}),

                            ],
                                style={"background": "#88888822", "color": WHITE,
                                    "font-family": "Quicksand", "padding": "1rem"}
                            ),

                            html.Br(),
                            html.Br(),

                            html.Center(dbc.Button(begin_text, color="info", outline=True,
                                        id="search-custom-begin-index", style={'font-size': "26px", 'font-family': "Quicksand"}))
                            ],
                        className="mb-3",
                        style={"width": "100%", "height": "42rem"},
                        ),
        ],
            outline=True,
            color="#049FD911",
            style={"color": "dark"}
        )
        return inputBox


    def get_outputBox(self, params):
        outputBox = dbc.Card([
            dbc.CardBody([
                html.Center(html.H5("Question-Answering", style={
                            "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),

                dbc.Card([
                    html.Div(
                        [
                            dbc.Row([
                                dbc.Col(dbc.Input(
                                    className="mb-3", placeholder=params._data_dict['states']['query'], id="search-custom-enter-q-box", style={"color": WHITE, "background": "#88888822"}
                                ), width=10),
                                dbc.Col(dbc.Button('Ask Q', color="info", outline=True,
                                                id="search-custom-ask-q-button", style={'font-family': "Quicksand"}))
                            ]),
                            dbc.Alert(
                                html.H6(params._data_dict['states']['result'],
                                        style={'text-align': 'right',
                                            "color": WHITE}
                                        ),
                                color="#88888822"
                            )
                        ]),

                ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand"}),

                html.Br(),

                dbc.Row([
                    dbc.Col([
                        self.get_latencyCard(params)
                    ]),
                    dbc.Col([
                        self.get_accuracyCard(params)
                    ])
                ]),

            ],
                className="mb-3",
                style={"width": "100%", "height": "42rem"},
            ),
        ],
            outline=True,
            color="#049FD911",
            style={"color": "dark"}
        )
        return outputBox


    def get_latencyCard(self, params):

        # TODO: REST API - For given model, get latency results 

        metrics =  {
            'latency': [-1, -1, -1],
            'search_avg': -1,
            'num_GPUs': 1,
            'accuracy': [-1, -1]
        }

        table_header = [
            html.Thead(html.Tr([html.Th("Step"), html.Th("Time (s)")]))
        ]

        row1 = html.Tr([html.Td("Load"), html.Td(metrics["latency"][0])])
        row2 = html.Tr([html.Td("Index"), html.Td(metrics["latency"][1])])
        row3 = html.Tr([html.Td("Search"), html.Td(metrics["latency"][2])])

        table_body = [html.Tbody([row1, row2, row3])]

        table = dbc.Table(table_header + table_body,
                        bordered=True, style={"color": WHITE})

        latencyCard = dbc.Card([
            html.Div(
                [
                    html.Center(html.H5("Latency", style={
                                "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),
                    table,
                    html.Br(),
                    html.H5(f"Number of GPUs: {metrics['num_GPUs']}", style={
                            "font-family": "Quicksand", "color": WHITE}),
                    html.H5(f"Search Time Avg: {metrics['search_avg']}", style={
                            "font-family": "Quicksand", "color": WHITE})
                ]),

        ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand", "height": "24rem"}
        )

        return latencyCard


    def get_accuracyCard(self, params):

        # TODO: REST API - For given model, get accuracy results 

        metrics =  {
            'latency': [-1, -1, -1],
            'search_avg': -1,
            'num_GPUs': 1,
            'accuracy': [-1, -1]
        }

        model = params._data_dict['states']['model_active']

        if not model: 
            link = ""
            repo = "" 

            model_text = "<>"
        
        else: 
            model_obj = [x for x in params._data_dict['states']['model_objs'] if str(x._info['class_name']) in model]
            print(model_obj)
            link = model_obj[0]._info['link']
            repo = model_obj[0]._info['repo']

            model_text = model[0]

        row21 = html.Tr(
            [html.Td("% Correct"), html.Td(f"{metrics['accuracy'][0]} %")])
        row22 = html.Tr(
            [html.Td("Avg Time"), html.Td(f"{metrics['accuracy'][1]} s")])

        table2_body = [html.Tbody([row21, row22])]
        table2 = dbc.Table(table2_body, bordered=True, style={"color": WHITE})

        accuracyCard = dbc.Card([
            html.Div(
                [
                    html.Center(html.H5("Accuracy", style={
                                "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),
                    html.Center(html.H5("Tested on SQUAD questions (only for SQUAD datasets)", style={
                                "font-family": "Quicksand", "color": WHITE, "padding": "0rem 0rem 1rem 0rem"})),
                    table2,
                    html.Br(),
                    html.Center(html.H5(html.A(f"Learn more about {model_text}.", href=link, target="_blank", style={
                                "font-family": "Quicksand", "color": WHITE}))),
                    html.Center(html.H5(html.A(f"View {model_text} Github Repo.", href=repo, target="_blank", style={
                                "font-family": "Quicksand", "color": WHITE})))

                ]),

        ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand", "height": "24rem"}
        )
        return accuracyCard




    """

    The following four functions are for the Solo Benchmark page.


    """


    def get_bench_TitleCard(self, params):

        default = params._data_dict['states']['chosen_data']
        if default is None:
            default = "Please select an input file"

        if len(params._data_dict['states']['model_active']) != 1: 
            begin_text = "Please select a model"
        else: 
            begin_text = f"Begin {params._data_dict['states']['model_active'][0]} Benchmarking"


        return dbc.Card([
            html.Div(
                [
                    html.Center(html.H5(default, style={
                                "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),
                    dbc.Row([
                        dbc.Col([
                            html.H6
                            (
                                "Please choose a valid dataset:",
                                style={"font-family": "Quicksand", "color": WHITE,
                                    'font-size': "22px", "padding": "1rem"}
                            ),
                        ], width=6),
                        dbc.Col([
                            dbc.Select(
                                id="search-bench-choose-file",
                                options=gen_inputOptions(params),
                                style={"background": "#888888",
                                    "color": WHITE, "font-family": "Quicksand"},
                                placeholder=default
                            ),
                        ])
                    ], align="center", style={'margin-bottom': "10px"}),
                    html.Center(dbc.Button(begin_text, color="info", outline=True,
                                id="search-bench-begin-index", style={'font-size': "26px", 'font-family': "Quicksand"}))


                ]),

        ],  outline=True,
            color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "margin-bottom": "1rem"}
        )


    def get_bench_MetricsCard(self, params, existing_state=None):

        # If no model selected, say we must select a model to proceed. 

        if len(params._data_dict['states']['model_active']) != 1: 
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Please select a model from the left",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
            )

        m_name = params._data_dict['states']['model_active'][0]
        print(f"(get_bench_MetricsCard) > {params._data_dict['states']['processes']}")


        # If we haven't started our process, say so 

        if m_name not in params._data_dict['states']['processes']: 
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Please begin indexing the model",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
            )



        # If we're starting up, say that we are


        if params._data_dict['states']['has_input_file'] and not params._data_dict['states']['begun_queue'] and params._data_dict['states']['processes'][m_name][1].empty():

            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Starting {params._data_dict['states']['model_active'][-1]} model...",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
            )
        elif params._data_dict['states']['has_input_file'] and not params._data_dict['states']['processes'][m_name][1].empty(): 
             params._data_dict['states']['begun_queue'] = True


        # Try getting results, if not, show old results 

        # TODO: REST API - For given model that is currently being benchmarked, get results OR directly get stats (metrics)

        try:
            results = params._data_dict['states']['processes'][m_name][1].get_nowait()
            params._data_dict['states']['processes'][m_name][2] = results

        except:
            results = params._data_dict['states']['processes'][m_name][2]


        # Compute the necessary metrics to be displayed 

        if results == "DONE": 
            return existing_state 
        else: 
            percent_correct = round(
                100 * np.mean(results["metrics"]["correct_arr"]), 2)
            num_correct = results["metrics"]["correct_arr"].count(1)
            num_total = results["questions"]["num_qs"]
            num_curr = results["questions"]["tot_qs"]
            avg_time = round(np.mean(results["times"]["all_ts"]), 2)
            progress = round(100.0 * num_curr / (num_total+0.001), 2)

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
                            self.get_bench_TimeGraph(results["times"]["all_ts"]),
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


    def get_bench_IncorrectCard(self, params):

        # If no model selected, say we must select a model to proceed. 

        if len(params._data_dict['states']['model_active']) != 1: 
            return dbc.Card([
                html.Div(
                    [
                       self.get_spinnyCircle()
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "50rem", "vertical-align": "middle"}
            )


        m_name = params._data_dict['states']['model_active'][0]

        if m_name not in params._data_dict['states']['processes']: 
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Please begin indexing the model",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "50rem", "vertical-align": "middle"}
            )


        # TODO: REST API - For given model that is currently being benchmarked, get results OR all incorrect questions directly 


        results = params._data_dict['states']['processes'][m_name][2]

        accuracy = round(100 * np.mean(results["metrics"]["correct_arr"]), 2)
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
        ], color="#88888822", style={"padding": "1rem", 'font-family': "Quicksand", "height": "50rem", "overflow": "auto"}
        )


    def get_bench_TimeGraph(self, data_arr):

        try:
            q_num = [(i+1) for i in range(len(data_arr))]
            t_sec = data_arr

            line = px.line(x=q_num, y=t_sec)
            line.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                xaxis_title="Question Number",
                yaxis_title="Time (s)",
            )

        except:
            q_num = [0.0]
            t_sec = [0.0]

            line = px.line(x=q_num, y=t_sec)
            line.update_layout(
                margin=dict(l=0, r=0, b=0, t=0),
                xaxis_title="Question Number",
                yaxis_title="Time (s)",
            )

        return dcc.Graph(id="time-series", figure=line, style={"height": "9rem"})



    """

    The following four functions are for the Comparing Models page.

    """


    def get_compare_TitleCard(self, params):

        default = params._data_dict['states']['chosen_data']
        if default is None:
            default = "Select an input file"

        if len(params._data_dict['states']['model_active']) != 2: 
            begin_text = "Select two models"
            model_title = "Please select two models"
        else: 
            begin_text = f"Begin Benchmarking"
            model_title = f"{params._data_dict['states']['model_active'][0]} vs {params._data_dict['states']['model_active'][1]}"

        dataset_text = "Choose a dataset:"

        return dbc.Card([
            html.Div(
                [
                    dbc.Row([
                        dbc.Col([
                            html.Center(html.H5(model_title, style={
                                        "font-family": "Quicksand", "color": TEAL, 'font-size': "40px", "padding": "0.5rem"})),
                        ], width=5),
                        dbc.Col([

                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.H6
                                        (
                                            dataset_text,
                                            style={"font-family": "Quicksand", "color": WHITE,
                                                'font-size': "22px", "padding": "1rem"}
                                        ),
                                    ], width=4),
                                    dbc.Col([
                                        dbc.Select(
                                            id="search-compare-choose-file",
                                            options=gen_inputOptions(params),
                                            style={"background": "#888888",
                                                "color": WHITE, "font-family": "Quicksand"},
                                            placeholder=default
                                        ),
                                    ], width=3),
                                    dbc.Col([
                                        html.Center(dbc.Button(begin_text, color="info", outline=True,
                                                            id="search-compare-begin-index", style={'font-size': "26px", 'font-family': "Quicksand"}))
                                    ]),
                                ], align="center", style={'margin-bottom': "0px"}),
                            ]),
                        ]),
                    ])
                ]),

        ],  outline=True,
            color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "6rem", "margin-bottom": "1rem"}
        )


    def get_compare_MetricsCard(self, params, m_num):

        # If no model selected, say we must select a model to proceed. 

        if len(params._data_dict['states']['model_active']) != 2: 
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Please select a model from the left",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
            )

        m_name = params._data_dict['states']['model_active'][m_num]
        print(f"(get_compare_MetricsCard) > {params._data_dict['states']['processes']}, processing {m_name}")
        
        
        # If we haven't started our process, say so 

        if m_name not in params._data_dict['states']['processes']: 
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Please begin indexing the model",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
            )


        # If we're starting up, say that we are


        if params._data_dict['states']['has_input_file'] and not params._data_dict['states']['begun_queue'] and params._data_dict['states']['processes'][m_name][1].empty():
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Starting {m_name} model...",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "32rem", "vertical-align": "middle"}
            )
        elif params._data_dict['states']['has_input_file'] and not params._data_dict['states']['processes'][m_name][1].empty(): 
            params._data_dict['states']['begun_queue'] = True


        # TODO: REST API - For given model that is currently being benchmarked, get results OR directly get stats (metrics)


        # Try getting results, if not, show old results 

        try:
            results = params._data_dict['states']['processes'][m_name][1].get_nowait()
            params._data_dict['states']['processes'][m_name][2] = results

        except:
            results = params._data_dict['states']['processes'][m_name][2]


        percent_correct = round(
            100 * np.mean(results["metrics"]["correct_arr"]), 2)
        num_correct = results["metrics"]["correct_arr"].count(1)
        num_total = results["questions"]["num_qs"]
        num_curr = results["questions"]["tot_qs"]
        avg_time = round(np.mean(results["times"]["all_ts"]), 2)
        progress = round(100.0 * num_curr / (num_total+0.001), 2)

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
                                label=f"Accuracy: {percent_correct}%", value=percent_correct, id="animated-progress", animated=False, striped=True, color="success"
                            ),
                            html.Br(),
                            self.get_bench_TimeGraph(results["times"]["all_ts"]),
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


    def get_compare_IncorrectCard(self, params, m_num):

        # If no model selected, say we must select a model to proceed. 

        if len(params._data_dict['states']['model_active']) != 2: 
            return dbc.Card([
                html.Div(
                    [
                       self.get_spinnyCircle()
                    ])
            ], outline=True, color="#049FD911", style={"margin-top": "15px", "color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "vertical-align": "middle", "overflow": "auto"}
            )


        m_name = params._data_dict['states']['model_active'][m_num]

        if m_name not in params._data_dict['states']['processes']: 
            return dbc.Card([
                html.Div(
                    [
                        html.Center(html.H6
                            (
                                f"Please begin indexing the model",
                                    style={"font-family": "Quicksand",
                                        "color": CREAM, 'font-size': "22px"}
                                    ),
                                    style={"margin-top": "50%"})
                    ])
            ], outline=True, color="#049FD911", style={"margin-top": "15px", "color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "vertical-align": "middle", "overflow": "auto"}
            )

        # TODO: REST API - For given model that is currently being benchmarked, get results OR all incorrect questions directly 


        results = params._data_dict['states']['processes'][m_name][2]

        accuracy = round(100 * np.mean(results["metrics"]["correct_arr"]), 2)
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
                                        f"Q's answered incorrectly by {m_name} will appear here.",
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


    """
    
    This final function is miscellanous.
    
    """

    def get_spinnyCircle(self):
        return dbc.Card([
            html.Div(
                [
                    html.Center(dbc.Spinner(color="info", spinner_style={
                                "width": "3rem", "height": "3rem"}), style={"margin-top": "10rem"})
                ])
        ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "24rem", "vertical-align": "middle"}
        )
