from dash import Dash, html, dcc, Input, Output, State

from aski.dash_files.app_constants import * 
from aski.utils.helpers import get_current_model, get_object_from_name

# ==============================================================================
# ========================== CUSTOM SUMMARIZATION ==============================
# ==============================================================================

def get_summarization_callbacks(app, page, params): 
   
    # === Callback for Custom Summarization page === #
    @app.callback(Output("custom-content", "children"),[
                  Input("summarization-custom-choose-file", "value"),
                  Input("summarization-custom-begin-index", "n_clicks")],
                  [])
    def render_custom_content(file_chosen, index_button):

        ### SELECTING FILE FOR SUMMARIZATION
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

        ### RUNNING SUMMARIZATION
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

    @app.callback(Output("bench-content", "children"),[
                  Input("summarization-bench-choose-dataset", "value"),
                  Input("summarization-bench-choose-metric",  "value"),
                  Input("summarization-bench-begin-summarization",   "n_clicks"),],[])
    def render_bench_content(dataset_chosen, metric_chosen, bench_button):

        print("> Entered bench callback.")

        ### CHOOSING A DATASET ###
        if dataset_chosen is not None:
            params._data_dict['states']['has_dataset']    = True 
            params._data_dict['states']['dataset_active'] = [dataset_chosen] 
        
        ### CHOOSING A METRIC
        if metric_chosen is not None:
            params._data_dict['states']['has_metric'] = True 
            params._data_dict['states']['metric_active'] = [metric_chosen] 
        
        ### RUNNING SUMMARIZATION ON AN ENTIRE DATASET
        if (bench_button == 1 and \
            len(params._data_dict['states']['model_active'])   == 1 and 
            len(params._data_dict['states']['metric_active'])  == 1  and \
            len(params._data_dict['states']['dataset_active']) == 1):


            print(params._data_dict['states']['dataset_active'][0])
            print(params._data_dict['states']['metric_active'][0])
            print(params._data_dict['states']['model_active'][0])

            dataset_active  = get_object_from_name(params._data_dict['states']['dataset_active'][0], params, 'dataset')
            metric_active   = get_object_from_name(params._data_dict['states']['metric_active'][0], params, 'metric')
            model_active    = get_object_from_name(params._data_dict['states']['model_active'][0], params, 'model')

            print('summarizing')

            updated_dataset = model_active._summarize_dataset(
                dataset_active,
                dataset_active._document_column,
                dataset_active._split)

            print('Updating dataset')
            dataset_index = params._data_dict['states']['dataset_objs'].index(dataset_active)
            params._data_dict['states']['dataset_objs'][dataset_index] = updated_dataset

            print(params._data_dict['states']['dataset_objs'][dataset_index])
            print(params._data_dict['states']['dataset_objs'][dataset_index]['validation'])

        return page.get_page_benchmark(params) 










