from dash import Dash, html, dcc, Input, Output, State

import multiprocessing 
from multiprocessing import Queue 
import requests 

from aski.dash_files.app_constants import *
from aski.dash_files.app_helpers import gen_filePreview 
from aski.models.interfaces.model_search import ModelSearch, squad_benchmark 

from aski.flask_servers.flask_constants import PORT_REST_API, PREF_REST_API


def get_search_callbacks(app, page, params): 

    # === Callback for Custom Question/Answering page === #

    @app.callback(Output("custom-content", "children"),
                 [Input("search-custom-choose-file", "value"),
                  Input("search-custom-begin-index", "n_clicks"), 
                  Input("search-custom-ask-q-button", "n_clicks")],
                 [State("search-custom-enter-q-box", "value")])

    def render_custom_content(file_chosen, index_button, ask_button, query_text):

        ### Component 01 - Selecting User File ###

        if file_chosen:
            split_file = file_chosen.split("|")  # Format of file value: <classname>|<filename>

            params._data_dict['states']['chosen_data'] = ''.join(w for w in split_file[1:])
            params._data_dict['states']['chosen_path'] = split_file[0]
            params._data_dict['states']['has_input_file'] = True 



        ### Component 02 - Indexing (Init) ###

        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            print(f"(callback_search) > Begun indexing {params._data_dict['states']['model_active'][0]}")

            preview, content = gen_filePreview(params._data_dict['states']['chosen_data'], params._data_dict['states']['chosen_path'])

            request = f"{PREF_REST_API}{PORT_REST_API}/models/initialize"
            response = requests.post(request, json={'model': params._data_dict['states']['model_active'][0], 
                                                   'filename': params._data_dict['states']['chosen_data'], 
                                                   'filecontent': content}
                                   )

            params._data_dict['states']['has_indexed'] = True 

            print(f"(callback_search) > Completed indexing...")
        


        ### Component 03 - Clicking "Ask Q" ###

        if ask_button == 1 and params._data_dict['states']['has_indexed']:

            print(f"(callback_search) > About to ask: {query_text}")

            request = f"{PREF_REST_API}{PORT_REST_API}/models/search"
            response = requests.get(request, json={'model': params._data_dict['states']['model_active'][0], 
                                                   'query': query_text}
                                   )

            res, time = response.json()['result'], response.json()['latency']

            ans = ModelSearch._parse_raw_ans(res, time)
            print(f"(callback_search) > Received answer: {ans}")

            params._data_dict['states']['query'] = query_text
            params._data_dict['states']['result'] = ans


        return page.get_page_custom(params)




    # === Callback for Solo Benchmarking page === #

    @app.callback(Output("bench-content", "children"),
                  [Input("search-bench-choose-file", "value"),
                   Input("search-bench-begin-index", "n_clicks"),],
                  [])
    
    def render_bench_content(file_chosen, bench_button):

        ### Component 01 - Selecting User File ###

        if file_chosen: 
            split_file = file_chosen.split("|")  # Format of file value: <classname>|<filename>

            params._data_dict['states']['chosen_data'] = ''.join(w for w in split_file[1:])
            params._data_dict['states']['chosen_path'] = split_file[0]
            params._data_dict['states']['has_input_file'] = True 
        

        ### Component 02 - Starting Indexing ###

        if bench_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            request = f"{PREF_REST_API}{PORT_REST_API}/models/benchmark"
            response = requests.get(request, json={'model': params._data_dict['states']['model_active'][0], 
                                                   'filename' : params._data_dict['states']['chosen_data'], 
                                                   'dataset' : params._data_dict['states']['chosen_path'],
                                                   'task' : 'start'}
                                   )

            print(f"(render_bench_content) > Started indexing...")
            params._data_dict['states']['has_indexed'] = True 


        return page.get_page_benchmark(params) 



    # === Callback for Solo Benchmarking page (helper) === #

    @app.callback(Output("search-bench-metrics-content", "children"),
                  [Input('search-bench-interval-component', 'n_intervals')],
                  [State("search-bench-metrics-content", "children")])

    def render_bench_metrics(n_interval, existing_state):

        # If no model selected
        if len(params._data_dict['states']['model_active']) == 0: 
            return existing_state 

        # If we haven't indexed yet
        if not params._data_dict['states']['has_indexed']:
            return page.get_spinnyCircle() 


        return page.get_bench_MetricsCard(params, existing_state)



  # === Callback for Solo benchmarking page (helper) === #

    @app.callback(Output("search-bench-incorrect-content", "children"),
                  [Input('search-bench-interval-component', 'n_intervals')],
                  [State("search-bench-incorrect-content", "children")])

    def render_bench_incorrect(n_interval, existing_state):

        # If no model selected
        if len(params._data_dict['states']['model_active']) == 0: 
            return existing_state 
            
        # If we haven't indexed yet
        if not params._data_dict['states']['has_indexed']:
            return page.get_spinnyCircle() 

        return page.get_bench_IncorrectCard(params)



    # === Callback for Model Comparison page === #

    @app.callback(Output("compare-content", "children"),
                 [Input("search-compare-choose-file", "value"),
                  Input("search-compare-begin-index", "n_clicks")],
                  [])

    def render_compare_content(file_chosen, bench_button):

        results = None
        ### Component 00 - Ensuring 2 Models ###

        if len(params._data_dict['states']['model_active']) != 2: 
            return page.get_page_comparison(params) 

        ### Component 01 - Selecting User File ###

        if file_chosen:
            split_file = file_chosen.split("|")  # Format of file value: <classname>|<filename>

            params._data_dict['states']['chosen_data'] = ''.join(w for w in split_file[1:])
            params._data_dict['states']['chosen_path'] = split_file[0]
            params._data_dict['states']['has_input_file'] = True 
        


        ### Component 02 - Starting Indexing ###

        if bench_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            request = f"{PREF_REST_API}{PORT_REST_API}/models/benchmark"
            response = requests.get(request, json={'model': params._data_dict['states']['model_active'][0], 
                                                'filename' : params._data_dict['states']['chosen_data'], 
                                                'dataset' : params._data_dict['states']['chosen_path'],
                                                'task' : 'start'}
                                )
            
            response = requests.get(request, json={'model': params._data_dict['states']['model_active'][1], 
                                    'filename' : params._data_dict['states']['chosen_data'], 
                                    'dataset' : params._data_dict['states']['chosen_path'],
                                    'task' : 'start'}
                                )

            print(f"(render_compare_content) > Started indexing...")
            params._data_dict['states']['has_indexed'] = True 


        return page.get_page_comparison(params) 



    # === Callback for Model Comparison page (helper) === #


    @app.callback(Output("search-compare-metrics-content-0", "children"),
                  [Input('search-compare-interval-component', 'n_intervals')],
                  [State("search-compare-metrics-content-0", "children")])

    def render_compare_metrics_0(n_interval, existing_state):

        # If no model selected
        if len(params._data_dict['states']['model_active']) != 2: 
            return existing_state 

        # If we haven't indexed yet
        if not params._data_dict['states']['has_indexed']:
            return page.get_spinnyCircle() 

        return page.get_compare_MetricsCard(params, 0)


    @app.callback(Output("search-compare-metrics-content-1", "children"),
                  [Input('search-compare-interval-component', 'n_intervals')],
                  [State("search-compare-metrics-content-1", "children")])

    def render_compare_metrics_1(n_interval, existing_state):

        # If no model selected
        if len(params._data_dict['states']['model_active']) != 2: 
            return existing_state 

        # If we haven't indexed yet
        if not params._data_dict['states']['has_indexed']:
            return page.get_spinnyCircle() 

        return page.get_compare_MetricsCard(params, 1)


    # === Callback for Model Comparison page (helper) === #


    @app.callback(Output("search-compare-incorrect-content-0", "children"),
                 [Input('search-compare-interval-component', 'n_intervals')],
                 [State("search-compare-incorrect-content-0", "children")])

    def render_compare_incorrect_0(n_interval, existing_state):

        # If no model selected
        if len(params._data_dict['states']['model_active']) != 2: 
            return existing_state 
            
        # If we haven't indexed yet
        if not params._data_dict['states']['has_indexed']:
            return page.get_spinnyCircle() 


        return page.get_compare_IncorrectCard(params, 0)
    

    @app.callback(Output("search-compare-incorrect-content-1", "children"),
                 [Input('search-compare-interval-component', 'n_intervals')],
                 [State("search-compare-incorrect-content-0", "children")])

    def render_compare_incorrect_1(n_interval, existing_state):

        # If no model selected
        if len(params._data_dict['states']['model_active']) != 2: 
            return existing_state 
            
        # If we haven't indexed yet
        if not params._data_dict['states']['has_indexed']:
            return page.get_spinnyCircle() 


        return page.get_compare_IncorrectCard(params, 1)
