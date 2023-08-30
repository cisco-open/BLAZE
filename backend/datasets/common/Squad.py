
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
Squad
====================================================
This module extends the HuggingFaceDataset Class and is used to load 
specifically from the Squad Dataset
"""

from backend.datasets.interfaces.hugging_face_dataset import HuggingFaceDataset


class Squad(HuggingFaceDataset):
    
    functions_supported = ["search","summarization","search_benchmark","search_comparison"]

    def __init__(self):
        super().__init__(
            dataset_name='squad_v2',
            config='squad_v2',
            class_name='Squad',
            document_column='text',
            summary_column=None,
            split=None)
        self._dataset_type = 'search'
        self._topic_content = self._create_topic_content()

    ''' Internal helper function to parse through dataset '''

    def _create_topic_content(self):
        """Returns list of all available topics (442 total)

        :return: List of all the topics
        :rtype: list
        """
        topic_content = {}

        # topic_content: title --> {context : [q/a pairs]}

        for entry in self._dataset['train']:

            title = entry['title']  # is a string
            context = entry['context']  # is a string
            question = entry['question']  # is a string
            answers = entry['answers']['text']  # can be a list

            if title not in topic_content:
                topic_content[title] = {context: [(question, answers)]}

            elif context not in topic_content[title]:
                topic_content[title][context] = [(question, answers)]

            else:
                topic_content[title][context].append((question, answers))

        return topic_content

    

    def _get_topic_titles(self):
        """Returns entirety of info_dict for a given title

        :return: list of titles
        :rtype: list
        """
        return list(self._topic_content.keys())

    

    def _get_title_info(self, title):
        """Returns text of a topic for a given title as list 

        :param title: the name of the title
        :type title: str
        :return: list of topic for given title
        :rtype: list
        """
        return self._topic_content[title]

   

    def _get_title_story(self, title):
        story = []
        for entry in self._topic_content[title]:
            story.append(entry)
        return story
    
    
