import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table

from aski.dash_files.app_constants import *
from aski.dash_files.app_helpers import *
from aski.utils.helpers import get_object_from_name, get_metrics_tables

class SummarizationInterface(): 

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

        model_active = params._data_dict['states']['model_active']
        model_objs = [x for x in params._data_dict['states']['model_objs'] if str(x._info['class_name']) in model_active]

        if len(model_objs) == 1: 
            model_title = f"{model_objs[0]._info['desc']}"
        else:
            model_title = "Please select a model from the left."

        return html.Div(html.Div([
            self.get_titleCard(model_title),
            dbc.Row([
                dbc.Col([
                    self.get_bench_dataset_card(params),
                    html.Div(self.get_begin_summarization_button(params)),
                ], width=4),
                dbc.Col(
                    self.get_bench_metric_card(params)
                    )
            ])
        ], style=CONTENT_STYLE), id="bench-content")

    def get_page_comparison(self, params): 
        pass 

# ==============================================================================
# ========================== CUSTOM SUMMARIZATION ==============================
# ==============================================================================

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
                                        id="summarization-custom-choose-file",
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
                                        id="summarization-custom-begin-index", style={'font-size': "26px", 'font-family': "Quicksand"}))
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
                html.Center(html.H5("Summarization", style={
                            "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),

                dbc.Card([
                    html.Div(
                        [
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

# ==============================================================================
# ======================= BENCHMARKING SUMMARIZATION ===========================
# ==============================================================================

    def get_bench_dataset_card(self, params):

        default = None

        # If no dataset has been selected
        if len(params._data_dict['states']['dataset_active']) == 0:
            default = "Please select a dataset."
        else:
            dataset = params._data_dict['states']['dataset_active'][0]
            default = get_object_from_name(dataset, params, 'dataset')._get_class_name()

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
                        ], width=10),
                        dbc.Col([
                            dbc.Select(
                                id="summarization-bench-choose-dataset",
                                required=True,
                                options=get_object_options(params, 'dataset'),
                                style={"background": "#888888",
                                    "color": WHITE, "font-family": "Quicksand"},
                                placeholder=default
                            ),
                        ]),
                    ], align="center", style={'margin-bottom': "10px"})
                ]),

        ],  outline=True,
            color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "margin-bottom": "1rem"})

    def get_bench_metric_card(self, params):

        default = "Please select a metric."

        # If no metric has been selected
        if len(params._data_dict['states']['metrics_results']) != len(params._data_dict['states']['metric_objs']):
            return

        return get_metrics_tables(params)

    def get_begin_summarization_button(self, params):

        default    = "Press the button below to start benchmarking."
        begin_text = 'Run the model'

        return dbc.Card([
            html.Div(
                [
                    html.Center(html.H5(default, style={
                                "font-family": "Quicksand", "color": CREAM, 'font-size': "30px", "padding": "1rem"})),
                    dbc.Row([
                        dbc.Col([
                        ], width=10)
                    ], align="center", style={'margin-bottom': "10px"}), html.Center(dbc.Button(begin_text, color="info", outline=True,
                     id="summarization-bench-begin-summarization", style={'font-size': "26px", 'font-family': "Quicksand"}))
                ]),
        ],  outline=True,
            color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "18rem", "margin-bottom": "1rem"}
        )

    def get_spinnyCircle(self):
        return dbc.Card([
            html.Div(
                [
                    html.Center(dbc.Spinner(color="info", spinner_style={
                                "width": "3rem", "height": "3rem"}), style={"margin-top": "10rem"})
                ])
        ], outline=True, color="#049FD911", style={"color": "dark", "padding": "1rem", 'font-family': "Quicksand", "height": "24rem", "vertical-align": "middle"}
        )
