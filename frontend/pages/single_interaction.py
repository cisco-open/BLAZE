
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


import base64
from dash import Input, Output, State
import requests

from backend.config import DevelopmentConfig
from backend.models.interfaces.model_search import ModelSearch

BLAZE_API = f"{DevelopmentConfig.PREF_REST_API}{DevelopmentConfig.PORT_REST_API}"


def gen_file_preview(filename, fileclass):
    request = f"{BLAZE_API}/datasets/files/detail"
    print(f"filename: {filename}, fileclass: {fileclass}")

    # Fileclass is simply the dataset class (ex. Squad, user)
    response = requests.get(
        request, params={'filename': filename, 'fileclass': fileclass})

    file_content = response.json()['content']
    # <-- only for user files, if not then "N/A" (in KB)
    file_size = response.json()['size']

    preview = f"Preview of File: {len(file_content)} chars, {len(file_content.split())} words, {file_size} kilobytes"
    return preview, file_content


def get_custom_callbacks(app, page, params):
    # Search takes the following: search-custom-ask-q-button,
    #                             search-custom-enter-q-box,


    callback_inputs = [
        Input("custom-choose-file", "value"),
        Input("custom-begin-index", "n_clicks")
    ]

    if 'summarization' in params._data_dict['function']['task']:
        callback_inputs.append(
            Input("custom-begin-summarization", "n_clicks"),
        )
        callback_inputs.append(
            Input("sidebar-models-checklist-summarization", "value"),
        )

    if 'search' in params._data_dict['function']['task']:
        callback_inputs.append(
            Input("search-custom-ask-q-button", "n_clicks"),
        )
        callback_inputs.append(
            State("search-custom-enter-q-box", "value")
        )
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
        params._data_dict['states']['model_active']['summarization'] = args[-1]
        if 'summarization' in task and 'search' in task:
            model_choice_search = args[-1]
            model_choice_summarization = args[-2]
        elif 'summarization' in task:
            model_choice_search = 0
            model_choice_summarization = args[-1]
        else:
            model_choice_search = args[-1]
            model_choice_summarization = 0

        # UPDATE MODEL SEARCH
        if 'search' in task and params._data_dict['states']['model_active']['search'] != model_choice_search:
            params._data_dict['states']['model_active']['search'] = model_choice_search

        # # UPDATE MODEL SUMMARIZATION
        if 'summarization' in task and params._data_dict['states']['model_active']['summarization'] != model_choice_summarization:
            params._data_dict['states']['model_active']['summarization'] = model_choice_summarization

        # RESET
        if reset_button == params._data_dict['states']['reset_presses'] + 1:
            print(f"(sidebar_functionality) > Resetting dashboard...")

            params._reset_data_dict_states()
            response = requests.get(f"{BLAZE_API}/reset")

            params._data_dict['states']['reset_presses'] = reset_button

            return page.get_page()

        print(params._data_dict)

        # FILE CONTENT

        if file_name is not None:

            content_type, content_string = file_content.split(',')
            decoded = base64.b64decode(content_string).decode("utf-8")

            requests.post(f"{BLAZE_API}/datasets/files/upload",
                          json={"file": file_name, "content": decoded})

            print(f"> Added file {file_name}.")
            params._data_dict['states']['chosen_data'] = file_name
            # TODO SWAP AND FIS
            params._data_dict['states']['chosen_path'] = "User"
            params._data_dict['states']['has_input_file'] = True

        # SELECTING FILE
        if file_chosen is not None:

            # Format of file value: <classname>|<filename>
            split_file = file_chosen.split("|")

            params._data_dict['states']['chosen_data'] = ''.join(
                w for w in split_file[1:])
            # TODO SWAP AND FIS
            params._data_dict['states']['chosen_path'] = split_file[0]
            params._data_dict['states']['has_input_file'] = True
            print(params._data_dict)

        # RUNNING SUMMARIZATION
        if summarization_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_summarized']:

            preview, content = gen_file_preview(
                params._data_dict['states']['chosen_data'], params._data_dict['states']['chosen_path'])

            # Get the name of the model currently active as a string
            model_active_name = params._data_dict['states']['model_active']['summarization']

            print(f" > Begun summarizing with {model_active_name}...")

            request = f"{BLAZE_API}/summary"
            response = requests.post(request, json={'model': params._data_dict['states']['model_active']['summarization'],
                                                   'content': content}
                                    )
            result = response.json()['result']

            print(result)

            params._data_dict['states']['has_summarized'] = True

            print(f" > Completed summarization...")

            params._data_dict['states']['result_summarization'] = result

        # RUNNING SEARCH - INDEXING
        if index_button == 1 and params._data_dict['states']['has_input_file'] and not params._data_dict['states']['has_indexed']:

            print(
                f"(callback_search) > Begun indexing {params._data_dict['states']['model_active']['search']}")

            preview, content = gen_file_preview(
                params._data_dict['states']['chosen_data'], params._data_dict['states']['chosen_path'])

            request = f"{BLAZE_API}/models/model/initialize"
            response = requests.post(request, json={'model': params._data_dict['states']['model_active']['search'],
                                                    'filename': params._data_dict['states']['chosen_data'],
                                                    'filecontent': content}
                                     )

            params._data_dict['states']['has_indexed'] = True

            print(f"(callback_search) > Completed indexing...")

        # RUNNING SEARCH - ASK QUESTION
        if ask_button == 1 and params._data_dict['states']['has_indexed']:

            print(f"(callback_search) > About to ask: {query_text}")

            request = f"{BLAZE_API}/search"
            response = requests.post(request, json={'model': params._data_dict['states']['model_active']['search'],
                                                   'query': query_text}
                                    )

            res, time = response.json()['result'], response.json()['latency']

            ans = ModelSearch._parse_raw_ans(res, time)
            print(f"(callback_search) > Received answer: {ans}")

            params._data_dict['states']['query'] = query_text
            params._data_dict['states']['result_search'] = ans

        return page.get_page()
