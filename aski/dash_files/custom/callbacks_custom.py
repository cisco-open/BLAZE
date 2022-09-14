from dash import Dash, html, dcc, Input, Output, State

from aski.dash_files.app_constants import * 
from aski.utils.helpers import get_model_object_from_name, get_object_from_name, read_file, save_file

def get_custom_callbacks(app, page, params): 

    @app.callback(
        Output("custom-content", "children"),[
        Input("sidebar-models-checklist-search", "value"), 
        Input("sidebar-models-checklist-summarization", "value"), 
        Input("sidebar-function-radioitems", "value"), 
        Input("sidebar-file-button", "contents"),
        Input("sidebar-reset-button", "n_clicks"),
        Input("custom-choose-file", "value"),
        Input("custom-begin-index", "n_clicks"),
        Input("custom-begin-summarization", "n_clicks"),
        Input("search-custom-ask-q-button", "n_clicks")],[
        State("sidebar-file-button", "filename"),
        State("search-custom-enter-q-box", "value")])

    def render_custom_content(
        model_choice_search,
        model_choice_summarization,
        page_choice, 
        file_content, 
        reset_button, 
        file_chosen, 
        index_button, 
        summarization_button,
        ask_button,
        file_name,
        query_text):

        # UPDATE MODEL SEARCH
        if params._data_dict['states']['model_active']['search'] != model_choice_search:
            params._data_dict['states']['model_active']['search'] = model_choice_search

        # UPDATE MODEL SUMMARIZATION
        if params._data_dict['states']['model_active']['summarization'] != model_choice_summarization: 
            params._data_dict['states']['model_active']['summarization'] = model_choice_summarization

        # RESET
        if reset_button == params._data_dict['states']['reset_presses'] + 1: 
            print(f"(sidebar_functionality) > Resetting dashboard...")

            params._reset_data_dict_states()
            params._data_dict['states']['model_active'] = [] 
            params._data_dict['states']['reset_presses'] = reset_button 
            return page.get_page() 

        # FILE CONTENT
        if file_name is not None:

            save_file(file_content, file_name)
            print(f"> Added file {file_name}.")

        ### SELECTING FILE
        if file_chosen is not None:

            # Update the params object to signify that the user chose a file
            params._data_dict['states']['has_input_file'] = True 

            # If the user reads from squad
            if (file_chosen.split("/")[-1] == "story.txt"): 
                params._data_dict['states']['chosen_data'] = file_chosen.split("/")[-2]

            # If the user uses a custom file
            else:
                params._data_dict['states']['chosen_data'] = (file_chosen.split("/")[-1]).replace("_", " ")

            params._data_dict['states']['chosen_path'] = file_chosen

        ### RUNNING SUMMARIZATION
        if summarization_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_summarized']:

            f_content = read_file(params._data_dict['states']['chosen_path'])

            # Get the name of the model currently active as a string
            model_active_name = params._data_dict['states']['model_active']['summarization']
            print(f" > Begun summarizing with {model_active_name}...")
            
            current_model = get_model_object_from_name(
                model_active_name, 
                'summarization', 
                params._data_dict) 

            result = current_model._summarize_text(f_content)

            print(result)

            params._data_dict['states']['has_summarized'] = True 

            print(f" > Completed summarization...")
        
            params._data_dict['states']['result_summarization'] = result

        ### RUNNING SEARCH - INDEXING
        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            file_content = read_file(params._data_dict['states']['chosen_path'])

            print(f"> Begun indexing {params._data_dict['states']['model_active']['search']}")

            model_active_name = params._data_dict['states']['model_active']['search']

            current_model = get_model_object_from_name(
                model_active_name, 
                'search', 
                params._data_dict) 

            current_model.load_model(file_name, file_content)
            params._data_dict['states']['has_indexed'] = True 

            print(f"(callback_search) > Completed indexing...")

        ### RUNNING SEARCH - ASK QUESTION
        if ask_button == 1 and params._data_dict['states']['has_indexed']:

            print(f"> About to ask: {query_text}")

            model_active_name = params._data_dict['states']['model_active']['search']

            current_model = get_model_object_from_name(
                model_active_name, 
                'search', 
                params._data_dict) 

            res, time = current_model.file_search(query_text)
            ans = "Unable to find an answer."

            try:
                ans = res[0]['res'] + f" ({round(time, 2)}s)"
                print(res[0])
            except:
                pass

            print(f"(callback_search) > Received answer: {ans}")

            params._data_dict['states']['query'] = query_text
            params._data_dict['states']['result_search'] = ans

        return page.get_page()