
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
    app.run_server(host='0.0.0.0',port='5010', debug=True, use_reloader=False)


if __name__ == "__main__":
    run_app()
