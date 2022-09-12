from dash import Dash, html, dcc, Input, Output, State

import multiprocessing 
from multiprocessing import Queue 

from aski.dash_files.app_constants import * 
from aski.models.interfaces.model_search import squad_benchmark 


def get_search_callbacks(app, page, params): 

    # === Callback for Custom Question/Answering page === #

    @app.callback(Output("custom-content", "children"),
                  [Input("search-custom-choose-file", "value"),
                   Input("search-custom-begin-index", "n_clicks"), 
                   Input("search-custom-ask-q-button", "n_clicks")],
                  [ State("search-custom-enter-q-box", "value")])

    def render_custom_content(file_chosen, index_button, ask_button, query_text):

        ### Component 01 - Selecting User File ###

        if file_chosen:

            params._data_dict['states']['has_input_file'] = True 

            if (file_chosen.split("/")[-1] == "story.txt"):
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-2]).replace("_", " ")
            else:
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-1]).replace("_", " ")

            params._data_dict['states']['chosen_path'] = file_chosen



        ### Component 02 - Indexing (Init) ###

        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            # TODO: REST API - Start indexing selected file with model 

            f_name = params._data_dict['states']['chosen_data']

            f = open(params._data_dict['states']['chosen_path'], "r")
            lines = f.readlines()[1:]
            f.close()
            f_content = "".join(lines)

            print(f"(callback_search) > Begun indexing {params._data_dict['states']['model_active']}")
            
            params._data_dict['states']['model_objs'][0].load_model(f_name, f_content)
            params._data_dict['states']['has_indexed'] = True 

            print(f"(callback_search) > Completed indexing...")
        


        ### Component 03 - Clicking "Ask Q" ###

        if ask_button == 1 and params._data_dict['states']['has_indexed']:

            # TODO: REST API - Get answer, latency from model with given query 

            print(f"(callback_search) > About to ask: {query_text}")

            res, time = params._data_dict['states']['model_objs'][0].file_search(query_text)
            ans = "Unable to find an answer."

            try:
                ans = res[0]['res'] + f" ({round(time, 2)}s)"
                print(res[0])
            except:
                pass

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

        print(f"(render_bench_content) > Entered bench callback.")

        ### Component 01 - Selecting User File ###

        if file_chosen:
            params._data_dict['states']['has_input_file'] = True 

            if (file_chosen.split("/")[-1] == "story.txt"):
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-2]).replace("_", " ")
            else:
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-1]).replace("_", " ")

            params._data_dict['states']['chosen_path'] = file_chosen

        
        ### Component 02 - Starting Indexing ###

        if bench_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            # TODO: REST API - Start indexing selected dataset with model 
            # TODO: REST API - Have some way to read/dump information into a Queue/write last few results 


            # Spawn new process, dump to shared pipe every question --> read to generate figures!
            
            m_name = params._data_dict['states']['model_active'][0]

            params._data_dict['states']['processes'][m_name] = [None, Queue(), CONST_RESULTS]
            params._data_dict['states']['processes'][m_name][0] = multiprocessing.Process(target=squad_benchmark, args=(
                                                                                    params._data_dict['states']['processes'][m_name][1], 
                                                                                    params._data_dict['states']['chosen_data'] , 
                                                                                    params._data_dict['states']['chosen_path'], 
                                                                                    params._data_dict['states']['model_objs'][0]))

            params._data_dict['states']['processes'][m_name][0].start() 

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

        # If we're done benchmarking 
        m_name = params._data_dict['states']['model_active'][0]
        if params._data_dict['states']['processes'][m_name][2] == "DONE":
            return existing_state

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

        # If we're done benchmarking 
        m_name = params._data_dict['states']['model_active'][0]
        if params._data_dict['states']['processes'][m_name][2] == "DONE":
            return existing_state

        return page.get_bench_IncorrectCard(params)



    # === Callback for Model Comparison page === #

    @app.callback(Output("compare-content", "children"),
                 [Input("search-compare-choose-file", "value"),
                  Input("search-compare-begin-index", "n_clicks")],
                  [])

    def render_compare_content(file_chosen, bench_button):

        results = None

        print(f"(render_compare_content) > Entered compare callback.")

        ### Component 00 - Ensuring 2 Models ###

        if len(params._data_dict['states']['model_active']) != 2: 
            return page.get_page_comparison(params) 

        ### Component 01 - Selecting User File ###

        if file_chosen:
            params._data_dict['states']['has_input_file'] = True 

            if (file_chosen.split("/")[-1] == "story.txt"):
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-2]).replace("_", " ")
            else:
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-1]).replace("_", " ")

            params._data_dict['states']['chosen_path'] = file_chosen


        ### Component 02 - Starting Indexing ###

        if bench_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            # TODO: REST API - Start indexing selected dataset with model 
            # TODO: REST API - Have some way to read/dump information into a Queue/write last few results 

            # Spawn new process, dump to shared pipe every question --> read to generate figures!
            
            m_name_1 = params._data_dict['states']['model_active'][0]
            m_name_2 = params._data_dict['states']['model_active'][1]

            params._data_dict['states']['processes'][m_name_1] = [None, Queue(), CONST_RESULTS]
            params._data_dict['states']['processes'][m_name_1][0] = multiprocessing.Process(target=squad_benchmark, args=(
                                                                                    params._data_dict['states']['processes'][m_name_1][1], 
                                                                                    params._data_dict['states']['chosen_data'] , 
                                                                                    params._data_dict['states']['chosen_path'], 
                                                                                    params._data_dict['states']['model_objs'][0]))

            params._data_dict['states']['processes'][m_name_2] = [None, Queue(), CONST_RESULTS]
            params._data_dict['states']['processes'][m_name_2][0] = multiprocessing.Process(target=squad_benchmark, args=(
                                                                                    params._data_dict['states']['processes'][m_name_2][1], 
                                                                                    params._data_dict['states']['chosen_data'] , 
                                                                                    params._data_dict['states']['chosen_path'], 
                                                                                    params._data_dict['states']['model_objs'][1]))


            params._data_dict['states']['processes'][m_name_1][0].start() 
            params._data_dict['states']['processes'][m_name_2][0].start() 

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

        # If we're done benchmarking 
        m_name = params._data_dict['states']['model_active'][0]
        if params._data_dict['states']['processes'][m_name][2] == "DONE":
            return existing_state

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

        # If we're done benchmarking 
        m_name = params._data_dict['states']['model_active'][1]
        if params._data_dict['states']['processes'][m_name][2] == "DONE":
            return existing_state

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

        # If we're done benchmarking 
        m_name = params._data_dict['states']['model_active'][0]
        if params._data_dict['states']['processes'][m_name][2] == "DONE":
            return existing_state

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

        # If we're done benchmarking 
        m_name = params._data_dict['states']['model_active'][1]
        if params._data_dict['states']['processes'][m_name][2] == "DONE":
            return existing_state

        return page.get_compare_IncorrectCard(params, 1)
