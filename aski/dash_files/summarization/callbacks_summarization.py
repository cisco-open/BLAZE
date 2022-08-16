from dash import Dash, html, dcc, Input, Output, State

from aski.dash_files.app_constants import * 
from aski.utils.helpers import get_current_model, get_object_from_name

# ==============================================================================
# ========================== CUSTOM SUMMARIZATION ==============================
# ==============================================================================

def get_summarization_callbacks(app, page, params): 
   
    # === Callback for Custom Summarization page === #
    @app.callback(Output("custom-content", "children"),
                  [Input("summarization-custom-choose-file", "value"),
                   Input("summarization-custom-begin-index", "n_clicks")],
                  [])

    def render_custom_content(file_chosen, index_button):

        ### Component 01 - Selecting User File
        if file_chosen is not None:

            # Update the params object to signify that the user chose a file
            params._data_dict['states']['has_input_file'] = True 

            # If the user reads from squad
            if (file_chosen.split("/")[-1] == "story.txt"):
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-2]).replace("_", " ")

            # If the user uses a custom file
            else:
                params._data_dict['states']['chosen_data'] = (
                    file_chosen.split("/")[-1]).replace("_", " ")

            params._data_dict['states']['chosen_path'] = file_chosen

        ### Component 02 - Summarizing the file  
        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            f_name = params._data_dict['states']['chosen_data']

            f = open(params._data_dict['states']['chosen_path'], "r")
            lines = f.readlines()[1:]
            f.close()
            f_content = "".join(lines)

            model_active = params._data_dict['states']['model_active'][0]
            print(f" > Begun summarizing with {model_active}...")
            
            current_model = get_current_model(params) 

            result = current_model._summarize_text(f_content)

            params._data_dict['states']['has_indexed'] = True 

            print(f" > Completed summarization...")
        
            params._data_dict['states']['result'] = result

        return page.get_page_custom(params)

# ==============================================================================
# ======================= BENCHMARKING SUMMARIZATION ===========================
# ==============================================================================

    @app.callback(Output("bench-content", "children"),
                  [Input("search-bench-choose-file", "value"),
                   Input("search-bench-begin-index", "n_clicks"),],
                  [])
    
    def render_bench_content(dataset_chosen, bench_button):

        print(f"(render_bench_content) > Entered bench callback.")

        ### Component 01 - Selecting User File ###
        print(dataset_chosen)

        dataset = get_object_from_name(dataset_chosen, params, 'dataset')

        if dataset_chosen:
            params._data_dict['states']['has_dataset'] = True 
            params._data_dict['states']['dataset_active'] = [dataset] 
        
        print(params._data_dict['states']['dataset_active'])
        print('Here')
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
