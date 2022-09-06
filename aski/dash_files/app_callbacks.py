"""
====================================================
App callbacks
====================================================
This module define the app callbacks, which allow the dashboard to be 
interactive. 

"""

import base64 
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import requests

from aski.dash_files.app_constants import *
from aski.params.parameters import Parameters
from aski.utils.helpers import save_file, read_file
from aski.dash_files.custom.page_custom import PageCustom
from aski.dash_files.custom.callbacks_custom import get_custom_callbacks

# ==============================================================================
# ============================ MODEL CALLBACKS =================================
# ==============================================================================

def run_app(data, port):

    # Initialize the parameters and the page
    params = Parameters(data)
    page = PageCustom(params)

    # Using the parameters class object ONLY! 
    content = html.Div([page.get_page()], id="l0-page-content")

    app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_QUICKSAND])
    app.layout = html.Div([dcc.Location(id="url"), page.get_sidebar(), content])
    app.css.config.serve_locally = True

    get_custom_callbacks(app, page, params)

    # Finally, after defining all our callbacks, we can run our app
    app.config['suppress_callback_exceptions'] = True
    app.run_server(port=port, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_app()
