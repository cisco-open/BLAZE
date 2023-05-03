
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
BART 
====================================================
This module loads a BART model and makes it available for the 
dashboard to use.

https://huggingface.co/docs/transformers/model_doc/bart

"""

from backend.models.interfaces.hugging_face_model_summarization import HuggingFaceModelSummarization


def get_bart_info():
    """ 
    Function to return a dictionnary containing the name, class name, 
    description, paper link and GitHub repo link of the BART model. It is used 
    throughout the code to get various information about the model.

    Returns
    -------
    model_info : a dictionnary
        A dictionnary containing the name, class name, 
        description, paper link and GitHub repo link of the T5 model
    """
    model_info = {
        'name': "BART",
        'class_name': 'Bart',
        'desc': "BART - Denoising Sequence-to-Sequence Pre-training",
        'link': "https://arxiv.org/pdf/1910.13461.pdf",
        'repo': "https://github.com/facebookresearch/fairseq/blob/main/examples/bart"}

    return model_info


class Bart(HuggingFaceModelSummarization):
    """BART model from 'Denoising Sequence-to-Sequence Pre-training for Natural 
    Language Generation, Translation, and Comprehension' paper"""

    def __init__(self):

        super().__init__(
            model_name='facebook/bart-large',
            model_info=get_bart_info(),
            max_length=1020,
            model_max_length=1020,
            truncation=True)
