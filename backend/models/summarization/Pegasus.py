
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
Pegasus 
====================================================
This module loads a Pegasus model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/main/model_doc/pegasus
"""

from backend.models.interfaces.hugging_face_model_summarization import HuggingFaceModelSummarization


def get_pegasus_info():
    """ 
    Function to return a dictionnary containing the name, class name, 
    description, paper link and GitHub repo link of the Pegasus model. It is 
    used throughout the code to get various information about the model.

    Returns
    -------
    model_info : a dictionnary
        A dictionnary containing the name, class name, 
        description, paper link and GitHub repo link of the T5 model
    """
    model_info = {
        'name': "Pegasus",
        'class_name': 'Pegasus',
        'desc': "Pegasus - Pre-training with Extracted Gap-sentences",
        'link': "https://arxiv.org/pdf/1912.08777.pdf",
        'repo': "https://github.com/google-research/pegasus"}

    return model_info


class Pegasus(HuggingFaceModelSummarization):
    """Pegasus model from 'Pre-training with Extracted Gap-sentences for 
    Abstractive Summarization' paper"""

    def __init__(self):

        super().__init__(
            model_name='google/pegasus-xsum',
            model_info=get_pegasus_info(),
            max_length=512,
            model_max_length=512,
            truncation=True)
