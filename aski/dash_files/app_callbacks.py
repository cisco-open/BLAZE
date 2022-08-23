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
from aski.dash_files.app_elements import *
from aski.dash_files.app_helpers import *
from aski.dash_files.search.callback_search import get_search_callbacks
from aski.dash_files.summarization.callbacks_summarization import get_summarization_callbacks
from aski.models.summarization import * 
from aski.models.search import * 
from aski.params.parameters import Parameters

# ==============================================================================
# ============================ MODEL CALLBACKS =================================
# ==============================================================================


def run_app(data, port):

    params = Parameters(data)

    models = params._data_dict['models']
    

    # Using the parameters class object ONLY! 
    content = html.Div([get_content(params)], id="l0-page-content")

    app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_QUICKSAND])
    app.layout = html.Div([dcc.Location(id="url"), get_sidebar(params), content])
    app.css.config.serve_locally = True


    # Determining which callbacks are needed
    task = params._data_dict['function']['task']

    if task == 'search': 
        page = SearchInterface(params)
        get_search_callbacks(app, page, params)
         
    
    elif task == 'summarization': 
        page = SummarizationInterface(params) 
        get_summarization_callbacks(app, page, params)
    
    elif task == "search/summarization": 
        pass  
    
    # We define one main callback for sidebar functions (universal)
    @app.callback(Output("l0-page-content", "children"), 
                  [Input("sidebar-models-checklist", "value"), 
                   Input("sidebar-function-radioitems", "value"), 
                   Input("sidebar-file-button", "contents"),
                   Input("sidebar-reset-button", "n_clicks")], 
                  [State("sidebar-file-button", "filename")])

    def sidebar_functionality(model_choice, page_choice, file_content, reset_button, file_name): 

        # If the user chooses to reset 
        if reset_button == params._data_dict['states']['reset_presses'] + 1: 
            print(f"(sidebar_functionality) > Resetting dashboard...")

            params._reset_data_dict_states()
            params._data_dict['states']['model_active'] = [] 
            params._data_dict['states']['reset_presses'] = reset_button 

            # TODO: REST API - Stop Currently Active Models (kill processes, if active)
            return page.get_page_custom(params) 

        # If the user picks a different model than the one(s) in use
        if params._data_dict['states']['model_active'] != sorted(model_choice): 

            l_m = len(model_choice)

            combo_1 = page_choice == "Custom Demo" and l_m == 1
            combo_2 = page_choice == "Solo Benchmark" and l_m == 1
            combo_3 = page_choice == "Model Comparison" and l_m == 2 

            if combo_1 or combo_2 or combo_3: 
                params._data_dict['states']['model_active'] = model_choice 
            else: 
                params._data_dict['states']['model_active'] = [] 
            
            params._reset_data_dict_states()

        # If the user chooses to upload a new file 

        if file_name is not None:

            content_type, content_string = file_content.split(',')
            decoded = base64.b64decode(content_string).decode("utf-8")

            # TODO: REST API - fix url
            requests.post("localhost:3000/files/upload", data={"file": file_name, "content": decoded})

            print(f"> Added file {file_name}.")

        #params.dump_params() <-- write to txt 
            
        # If the user switches to a new page
        if page_choice == "Solo Benchmark": 
            return page.get_page_benchmark(params)
        
        elif page_choice == "Model Comparison": 
            return page.get_page_comparison(params) 
            
        else: 
            return page.get_page_custom(params) 


    # Next, we ensure that the REST API Server is up and running 

    PORT_REST_API = 3000 # TODO: Make this a global constant! 
    print(f"(run_app) > Checking if REST API Server at port {PORT_REST_API} is ready...")

    address = f"http://127.0.0.1:{PORT_REST_API}/"

    response = requests.get(address)
    print(f"(run_app) > Received response: {response}, {response.json()}")

    # Finally, after defining all our callbacks, we can run our app

    app.config['suppress_callback_exceptions'] = True
    app.run_server(port=port, debug=True, use_reloader=False)

if __name__ == "__main__":
    run_app()
