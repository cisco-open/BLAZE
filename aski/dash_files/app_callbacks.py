
# Copyright 2022 Cisco Systems, Inc. and its affiliates
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0



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
import time 

from aski.dash_files.app_constants import *
from aski.params.parameters import Parameters
from aski.dash_files.custom.page_custom import PageCustom
from aski.dash_files.custom.callbacks_custom import get_custom_callbacks
from aski.flask_servers.flask_constants import PREF_REST_API, PORT_REST_API
import copy
# ==============================================================================
# ============================ MODEL CALLBACKS =================================
# ==============================================================================

def run_app(data, port, host):
    time.sleep(5)
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
    app.run_server(host='0.0.0.0',port=port, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_app()
