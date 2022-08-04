from dash import Dash, html, dcc, Input, Output, State

from aski.dash_files.app_constants import * 


def get_summarization_callbacks(app, page, params): 
   
   
    # === Callback for Custom Question/Answering page === #

    @app.callback(Output("custom-content", "children"),
                  [Input("summarization-custom-choose-file", "value"),
                   Input("summarization-custom-begin-index", "n_clicks")],
                  [])

    def render_custom_content(file_chosen, index_button):

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

            f_name = params._data_dict['states']['chosen_data']

            f = open(params._data_dict['states']['chosen_path'], "r")
            lines = f.readlines()[1:]
            f.close()
            f_content = "".join(lines)

            print(f"(callback_search) > Begun indexing {params._data_dict['states']['model_active']}")
            
            params._data_dict['states']['model_objs'][0]._summarize_text(f_content)
            params._data_dict['states']['has_indexed'] = True 

            print(f"(callback_search) > Completed indexing...")
        
            params._data_dict['states']['result'] = params._data_dict['states']['model_objs'][0]._get_summary()


        return page.get_page_custom(params)
