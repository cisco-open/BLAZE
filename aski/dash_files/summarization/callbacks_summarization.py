from dash import Dash, html, dcc, Input, Output, State

from aski.dash_files.app_constants import * 
from aski.utils.helpers import get_current_model

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
