
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

import requests
import json
import os.path as path
from backend.config import TestingConfig


class WebEx:
    
    functions_supported = ["search","summarization"]

    def __init__(self):
        self._class_name = 'WebEx'
        self._dataset_name = 'WebEx'
        self.webex_api_endpoint = "https://webexapis.com/v1"
        self.headers = {"Authorization": f"Bearer " + TestingConfig.WEBEX_ACCESS_TOKEN, "Content-Type": "application/json", "Scope" : "meeting:recordings_read"}
        self.meetings = {}
        self.transcripts = {}
        self.names = {}
        self.merged_text = ""
        self.file_name = "webex_transcripts.json"
        self.load_meetings_list()
        self.download_webex_meetings()
    ''' Internal helper function to parse through dataset '''

    def _create_topic_content(self):
        """Returns list of all available topics (442 total)

        :return: List of all the topics
        :rtype: list
        """
        self.transcripts

    

    def _get_topic_titles(self):
        """Returns entirety of info_dict for a given title

        :return: list of titles
        :rtype: list
        """
        return list(self.transcripts.keys())

    

    def _get_title_info(self, title):
        """Returns text of a topic for a given title as list 

        :param title: the name of the title
        :type title: str
        :return: list of topic for given title
        :rtype: list
        """
        return self.transcripts[title]

    def _get_class_name(self):
        return self._class_name

    def _get_dataset_name(self):
        return self._dataset_name
   

    def _get_title_story(self, title):
        return self.transcripts[title]
    
    def load_meetings_list(self):

        meetings_url = f"{self.webex_api_endpoint}/meetingTranscripts"
        response = requests.get(meetings_url, headers=self.headers)

        print("Loaded in all transcripts...", json.loads(response.text))
        self.meetings = json.loads(response.text).get("items",[])
       
    
    def list_meetings(self):
        return self.meetings
    
    def download_webex_meetings(self):
        for meeting in self.meetings: 
            id = meeting['id']
            timestamped_text = {}

            transcript_url = f"{self.webex_api_endpoint}/meetingTranscripts/{id}/download"
            response = requests.get(transcript_url, headers=self.headers)
            lines = response.text.split("\n\n")

            lines = lines[1:]

            for line in lines: 
                split_again = line.split("\n")
                timestamped_text[split_again[2]] = split_again[1]
                self.merged_text = self.merged_text + split_again[2]
                
            
            self.transcripts[id] = self.merged_text
            self.merged_text = ""
            self.names[id] = meeting['meetingId']
        json_object = json.dumps(self.transcripts, indent=4)
        print(json_object)
        filepath = path.join(TestingConfig.FILES_DIR, self.file_name)
        with open(filepath,"w") as f:
            f.write(json_object)

        return self.file_name

