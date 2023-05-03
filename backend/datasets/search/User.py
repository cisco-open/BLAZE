
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
User
====================================================
This module is used to load custom text files uploaded by user(s).
"""

import os


from backend.config import DevelopmentConfig


class User():

    def __init__(self):
        self._class_name = 'User'
        self._dataset_name = 'User'
        self._dataset_type = 'search'

        self._topic_content = {}
        self._get_files()

    def _get_files(self):
        """Get files from the directory
        """        
        for path in os.listdir(DevelopmentConfig.FILES_DIR):
            if os.path.isfile(os.path.join(DevelopmentConfig.FILES_DIR, path)) and path.endswith('.txt'):

                f = open(os.path.join(DevelopmentConfig.FILES_DIR, path), 'r', encoding='utf-8')
                lines = f.readlines()
                f.close()

                self._topic_content[path] = lines

    def _update_file(self, file_path):
        if file_path not in self._topic_content:
            if os.path.isfile(os.path.join(DevelopmentConfig.FILES_DIR, file_path)) and file_path.endswith('.txt'):
                f = open(os.path.join(DevelopmentConfig.FILES_DIR, file_path),
                         'r', encoding='utf-8')
                lines = f.readlines()
                f.close()
                self._topic_content[file_path] = lines

    def _get_class_name(self):
        return self._class_name

    def _get_dataset_name(self):
        return self._dataset_name



    def _get_topic_titles(self):
        """Returns list of all available topics

        :return: list of topics
        :rtype: list
        """        
        return list(self._topic_content.keys())

   

    def _get_title_info(self, title):
        """Returns entirety of info_dict for a given title 

        :param title: specify the title 
        :type title: str
        :return: returns contents of title
        :rtype: dict
        """        
        return self._topic_content[title]

    

    def _get_title_story(self, title):
        """Returns text of a topic for a given title as list

        :param title: Specify the title
        :type title: str
        :return: returns the list of text of topic for given title
        :rtype: list
        """        
        story = []
        for entry in self._topic_content[title]:
            story.append(entry)
        return story
