"""This app creates the drag-and-drop builder."""

import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from drag.callbacks import get_callbacks
from drag.constants import * 
from drag.global_obj import init_design
from drag.layouts import design_layout

import dash_bootstrap_components as dbc
from dash_extensions.enrich import DashProxy, NoOutputTransform

def run_app(): 
        
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
    get_callbacks(app)


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
