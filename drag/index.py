"""This app creates a dashboard for flame."""

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

import callbacks_design
from constants import (ID_CONTENT, RESOURCE_COMPUTES, RESOURCE_DATA,
                       RESOURCE_DESIGN, RESOURCE_JOBS, RESOURCE_MODELS)
from global_objects import init_design
from layouts_design import design_layout

import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, NoOutputTransform

def run_app(): 
        
    FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
    FONT_QUICKSAND = "https://fonts.googleapis.com/css?family=Quicksand&display=swap"

    app = DashProxy(
        external_stylesheets=[dbc.themes.FLATLY, FA, FONT_QUICKSAND],
        suppress_callback_exceptions=True,
        title="Builder-Flexible NLP Pipeline",
        transforms=[
            NoOutputTransform(),  # enable callbacks without output
        ]
    )

    content = html.Div(id=ID_CONTENT)

    app.layout = html.Div([dcc.Location(id="url"), content])
    app.config['suppress_callback_exceptions'] = True 
    callbacks_design.get_design_callbacks(app)


    ### Sidebar Callback ###

    @app.callback(Output(ID_CONTENT, "children"), 
                Input("url", "pathname"))

    def display_page_content(pathname):
        """Return a page for content pane."""

        init_design()
        return design_layout

    # Can't use 5001
    app.run_server(port='5010', debug=True, use_reloader=False)

if __name__ == "__main__":
    run_app()

