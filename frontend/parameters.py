
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


"""
====================================================
Params
====================================================
This module stores a class to initialize, access and modify the parameters
of the dashboard used throughout the code.

"""

import requests

from frontend.custom_resources import SEARCH_BOX_PLACEHOLDER, ANSWER_BOX_PLACEHOLDER
from frontend.pages.single_interaction import BLAZE_API


class Parameters:

    def __init__(self, data_dict=None):

        self._data_dict = data_dict

        self._data_dict['states'] = {}

        self._data_dict['states']['chosen_data'] = None
        self._data_dict['states']['chosen_path'] = None
        self._data_dict['states']['has_input_file'] = False
        self._data_dict['states']['has_indexed'] = False
        self._data_dict['states']['has_summarized'] = False

        self._data_dict['states']['has_dataset'] = False
        self._data_dict['states']['has_metric'] = False

        print(f"\n==== Loading Models ===\n")

        self._data_dict['states']['model_dict'] = {}
        self._data_dict['states']['model_active'] = {}
        request = f"{BLAZE_API}/get_model_checklist"
        response = requests.get(request)
        self._data_dict['states']['model_checklist'] = response.json()['data']

        tasks_list = self._data_dict['function']['task'].split('/')

        for task in tasks_list:
            self._data_dict['states']['model_active'][task] = None

        self._data_dict['states']['query'] = SEARCH_BOX_PLACEHOLDER
        self._data_dict['states']['result_search'] = ANSWER_BOX_PLACEHOLDER
        self._data_dict['states']['result_summarization'] = ANSWER_BOX_PLACEHOLDER
        self._data_dict['states']['reset_presses'] = 0

        # Dictionary with: {model_name: [process, queue, old_results]}
        self._data_dict['states']['processes'] = {}
        self._data_dict['states']['begun_queue'] = False

    def _update_data_dict_model_used(self, model_used):

        self._data_dict['states']['model_active'] = model_used

    def _reset_data_dict_states(self):

        self._data_dict['states']['has_input_file'] = False
        self._data_dict['states']['has_indexed'] = False
        self._data_dict['states']['has_summarized'] = False
        self._data_dict['states']['chosen_name'] = None
        self._data_dict['states']['chosen_path'] = None
        self._data_dict['states']['result_search'] = ANSWER_BOX_PLACEHOLDER
        self._data_dict['states']['result_summarization'] = ANSWER_BOX_PLACEHOLDER

        self._data_dict['states']['query'] = SEARCH_BOX_PLACEHOLDER
        self._data_dict['states']['result'] = ANSWER_BOX_PLACEHOLDER

        # Killing/resetting all multi-processing related things

        for model_name in self._data_dict['states']['processes']:
            p = self._data_dict['states']['processes'][model_name][0]
            p.kill()

        self._data_dict['states']['processes'] = {}
        self._data_dict['states']['begun_queue'] = False

    def _update_params(self, params):

        self._data_dict = params

    def _get_params(self):

        return(self._data_dict)

    def get_function_task(self):
        return self._data_dict['function']['task']

    def get_title(self):
        return self._data_dict['Title']
