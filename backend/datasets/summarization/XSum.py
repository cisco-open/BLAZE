
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
XSumDataset
====================================================
This module extends the Dataset Class and is used to load specifically from the 
XSum Dataset.

https://huggingface.co/datasets/xsum
"""

from backend.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset


class XSum(HuggingFaceDataset):

    def __init__(self):
        super().__init__(
            dataset_name='xsum',
            config='3.0.0',
            class_name='XSum',
            document_column='document',
            summary_column='summary',
            split='validation')
        self._dataset_type = 'summarization'
