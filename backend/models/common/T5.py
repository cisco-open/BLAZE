
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
T5 
====================================================
This module loads a T5 model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/t5

"""

from backend.models.interfaces.hugging_face_model_summarization import HuggingFaceModelSummarization


def get_t5_info():
    """ 
    Function to return a dictionnary containing the name, class name, 
    description, paper link and GitHub repo link of the T5 model. It is used 
    throughout the code to get various information about the model.

    Returns
    -------
    model_info : a dictionnary
        A dictionnary containing the name, class name, 
        description, paper link and GitHub repo link of the T5 model
    """
    model_info = {
        'name': "T5",
        'class_name': 'T5',
        'desc': "T5 - Exploring the Limits of Transfer Learning",
        'link': "https://arxiv.org/pdf/1910.10683.pdf",
        'repo': "https://github.com/google-research/text-to-text-transfer-transformer"}

    return model_info


class T5(HuggingFaceModelSummarization):
    """T5 model from 'Exploring the Limits of Transfer Learning with a Unified
     Text-to-Text Transformer' paper"""
    tasks_supported = ["summarization"]
    def __init__(self):

        super().__init__(
            model_name='t5-base',
            model_info=get_t5_info(),
            max_length=2000,
            model_max_length=2000,
            truncation=True)
