import base64 
from dash import Dash, html, dcc, Input, Output, State
import requests 

from aski.dash_files.app_constants import *
from aski.flask_servers.flask_constants import PREF_REST_API, PORT_REST_API
from aski.utils.helpers import get_model_object_from_name, get_object_from_name
from aski.dash_files.custom.page_custom import gen_file_preview
from aski.models.interfaces.model_search import ModelSearch 


def get_custom_callbacks(app, page, params): 

    # Search takes the following: search-custom-ask-q-button, 
    #                             search-custom-enter-q-box, 
    #                             

    callback_inputs = [
            Input("custom-choose-file", "value"),
            Input("custom-begin-index", "n_clicks")
    ] 

    if 'summarization' in params._data_dict['function']['task']: 
        callback_inputs.append(
            Input("custom-begin-summarization", "n_clicks"),
        ) 

    if 'search' in params._data_dict['function']['task']: 
        callback_inputs.append(
            Input("search-custom-ask-q-button", "n_clicks"),
        )
        callback_inputs.append(
            State("search-custom-enter-q-box", "value")
        )


    if 'summarization' in params._data_dict['function']['task']: 
        callback_inputs.append(
            Input("sidebar-models-checklist-summarization", "value"), 
        ) 

    if 'search' in params._data_dict['function']['task']: 
        callback_inputs.append(
            Input("sidebar-models-checklist-search", "value"), 
        )
    

    @app.callback(
        Output("custom-content", "children"),
        Input("sidebar-function-radioitems", "value"), 
        Input("sidebar-file-button", "contents"),
        Input("sidebar-reset-button", "n_clicks"),
        State("sidebar-file-button", "filename"),
        callback_inputs)

    def render_custom_content(*args):

        page_choice = args[0]
        file_content = args[1]
        reset_button = args[2]
        file_name = args[3]


        file_chosen = args[4]
        index_button = args[5]

        task = params._data_dict['function']['task']

        if 'summarization' in task: 
            summarization_button = args[6]
            if 'search' in task:  
                ask_button = args[7]
                query_text = args[8]
            else: 
                ask_button = 0 
                query_text = "" 
        else: 
            summarization_button = 0 
            ask_button = args[6]
            query_text = args[7]
        
        if 'summarization' in task and 'search' in task: 
            model_choice_search = args[-1]
            model_choice_summarization = args[-2]
        elif 'summarization' in task: 
            model_choice_search = 0 
            model_choice_summarization = args[-1]
        else: 
            model_choice_search = args[-1]
            model_choice_summarization = 0 

        print(args)

        # UPDATE MODEL SEARCH
        if 'search' in task and params._data_dict['states']['model_active']['search'] != model_choice_search:
            params._data_dict['states']['model_active']['search'] = model_choice_search

        # UPDATE MODEL SUMMARIZATION
        if 'summarization' in task and params._data_dict['states']['model_active']['summarization'] != model_choice_summarization: 
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

            content_type, content_string = file_content.split(',')
            decoded = base64.b64decode(content_string).decode("utf-8")

            requests.post(f"{PREF_REST_API}{PORT_REST_API}/files/upload", data={"file": file_name, "content": decoded})

            print(f"> Added file {file_name}.")

        ### SELECTING FILE
        if file_chosen is not None:

            split_file = file_chosen.split("|")  # Format of file value: <classname>|<filename>

            params._data_dict['states']['chosen_data'] = ''.join(w for w in split_file[1:])
            params._data_dict['states']['chosen_path'] = split_file[0] # TODO SWAP AND FIS 
            params._data_dict['states']['has_input_file'] = True 


        ### RUNNING SUMMARIZATION
        if summarization_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_summarized']:

            preview, content = gen_file_preview(params._data_dict['states']['chosen_data'], params._data_dict['states']['chosen_path'])
            
            # Get the name of the model currently active as a string
            model_active_name = params._data_dict['states']['model_active']['summarization']
            print(f" > Begun summarizing with {model_active_name}...")
            
            current_model = get_model_object_from_name(
                model_active_name, 
                'summarization', 
                params._data_dict) 

            result = current_model._summarize_text(content)

            print(result)

            params._data_dict['states']['has_summarized'] = True 

            print(f" > Completed summarization...")
        
            params._data_dict['states']['result_summarization'] = result

        ### RUNNING SEARCH - INDEXING
        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            print(f"(callback_search) > Begun indexing {params._data_dict['states']['model_active']['search']}")

            preview, content = gen_file_preview(params._data_dict['states']['chosen_data'], params._data_dict['states']['chosen_path'])

            request = f"{PREF_REST_API}{PORT_REST_API}/models/initialize"
            response = requests.post(request, json={'model': params._data_dict['states']['model_active']['search'], 
                                                   'filename': params._data_dict['states']['chosen_data'], 
                                                   'filecontent': content}
                                   )

            params._data_dict['states']['has_indexed'] = True 

            print(f"(callback_search) > Completed indexing...")


        ### RUNNING SEARCH - ASK QUESTION
        if ask_button == 1 and params._data_dict['states']['has_indexed']:

            print(f"(callback_search) > About to ask: {query_text}")

            request = f"{PREF_REST_API}{PORT_REST_API}/models/search"
            response = requests.get(request, json={'model': params._data_dict['states']['model_active']['search'], 
                                                   'query': query_text}
                                   )

            res, time = response.json()['result'], response.json()['latency']

            ans = ModelSearch._parse_raw_ans(res, time)
            print(f"(callback_search) > Received answer: {ans}")

            params._data_dict['states']['query'] = query_text
            params._data_dict['states']['result_search'] = ans

        return page.get_page()