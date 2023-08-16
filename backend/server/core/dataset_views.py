import json
from glob import glob
import os
import os.path as path
from flask_restful import Resource, Api, fields, marshal_with, request
from flask import current_app
from backend.params.specifications import Specifications
from backend.server.utils.helpers import get_object_from_name
import requests

class DatasetsList(Resource):
    
    def get(self):
        """
        Get all available datasets
        ---
        tags:
          - Dataset Endpoints
        responses:
          200:
            description: successful operation
            schema:
              properties:
                datasets_summarization:
                  type: object
                  properties:
                    type: string
                datasets_search:
                  type: object
                  properties:
                    type: string
                    
        """
        specs = Specifications(current_app.config.get("MODELS_DIR"), current_app.config.get("DATASETS_DIR"))
        return {'datasets_summarization': specs._list_datasets_summarization, 'datasets_search': specs._list_datasets_search}, 200

class DatasetFilesList(Resource):

    def get(self):
        '''
        GET /dataset/files/ - all available files from a given dataset 
        - Input->Query Params: {"file": str, "content": str}
        - Output: {}
        - Use Case: when the user uploads a file
        - Who's Doing: Jason
        
        '''

        query_params = request.args
        if any(param not in query_params for param in ['dataset']):
            return "Malformed request", 400

        dataset_name = str(query_params['dataset'])
        
        dataset_obj = get_object_from_name(dataset_name, current_app.config.get("server_config"), 'dataset')

        if not dataset_obj:
            return "That dataset doesn't exist", 404

        titles = dataset_obj._get_topic_titles()
        return {"files": titles}, 200

    def post(self):
        '''
        POST /dataset/files/ - user uploads file 
        - Input: {"file": str, "content": str}
        - Output: {}
        - Use Case: when the user uploads a file
        - Who's Doing: Jason
        
        '''
        request_data = request.json
        if any(param not in request_data for param in ['file', 'content']):
            return "Malformed request", 400

        if not any(request_data['file'].endswith(ext) for ext in ['.txt', '.pdf']):
            return "Bad file extension", 400

        filepath = path.join(current_app.config.get("FILES_DIR"), request_data['file'])
        isBytes = "" if request_data['file'].endswith('.txt') else 'b'
        with open(filepath, f'w{isBytes}') as f:
            f.write(request_data['content'])

        for dataset_obj in current_app.config.get("server_config")['dataset_objs']:
            if dataset_obj._dataset_name == "User":
                dataset_obj._update_file(request_data['file'])
                break

        return {}, 201

    def delete(self):

        '''5) DELETE  /dataset/files/ - user deletes file
        - Input: {"file": str}
        - Output: {}
        - Use Case: when the user deletes a **CUSTOM** file
        - Who's Doing: Jason
        '''
        request_data = request.json
        if any(param not in request_data for param in ['file']):
            return "Malformed request", 400

        filepath = path.join(current_app.config.get("FILES_DIR"), request_data['file'])
        if os.path.exists(filepath):
            os.remove(filepath)
            return {}, 204
        else:
            return {}, 404

class DatasetFilesDetails(Resource):

    def get(self):
        """
        3) GET dataset/files/file - specific file text (details) 
            - Input: {"filename": str, "fileclass": str}
            - Output: {"content": str, "size": int}
            - Use Case: Show preview for files
            - Who's Doing: Jason
        """
        query_params = request.args
        if any(param not in query_params for param in ['filename', 'fileclass']):
            return "Malformed request", 400

        dataset_name = str(query_params['fileclass'])

        if dataset_name == 'User':
            filepaths = glob(
                path.join(current_app.config.get("FILES_DIR"), '**', query_params['filename']), recursive=True)

            if len(filepaths) > 0:
                filepath = filepaths[0]
               
                with open(filepath, 'r') as f:
                    if filepath.endswith(".json"):
                        content = json.loads(f.read())
                    else:
                        content = f.read()
                    size = os.path.getsize(filepath) / 1000
            else:
                return "That file doesn't exist", 404
        else:
            print(f"{dataset_name} | {str(query_params['filename'])}")
            dataset_obj = get_object_from_name(
                dataset_name, current_app.config.get("server_config"), 'dataset')
            print(dataset_obj)
            if dataset_obj._dataset_type == 'search':
                content = dataset_obj._get_title_story(str(query_params['filename']))
                content = ' '.join(sentence for sentence in content)
                size = "N/A"
            elif dataset_obj._dataset_type == 'summarization':
                content = None
                size = None
            else:
                return "That file doesn't exist", 404

        response_data = {}
        response_data['content'] = content
        response_data['size'] = size

        return response_data, 200


class DownloadWebExMeetingTranscripts(Resource):

    def get(self):
        
        webex_api_endpoint = "https://webexapis.com/v1"
        headers = {"Authorization": f"Bearer " + current_app.config.get('WEBEX_ACCESS_TOKEN'), "Content-Type": "application/json", "Scope" : "meeting:recordings_read"}

        meetings_url = f"{webex_api_endpoint}/meetingTranscripts"
        response = requests.get(meetings_url, headers=headers)

        print("Loaded in all transcripts...", json.loads(response.text))
        self.meetings = json.loads(response.text)["items"]

        self.transcripts = {}
        self.names = {}
        self.merged_text = ""
        self.file_name = "webex_transcripts.json"

        for meeting in self.meetings: 
            id = meeting['id']
            timestamped_text = {}

            transcript_url = f"{webex_api_endpoint}/meetingTranscripts/{id}/download"
            response = requests.get(transcript_url, headers=headers)
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

        filepath = path.join(current_app.config.get("FILES_DIR"), self.file_name)
        with open(filepath,"w") as f:
            f.write(json_object)

        return {"response": "success","fileName":self.file_name}, 200


class ListMeetingTranscripts(Resource):

    def get(self):
        webex_api_endpoint = "https://webexapis.com/v1"
        headers = {"Authorization": f"Bearer " + current_app.config.get('WEBEX_ACCESS_TOKEN'), "Content-Type": "application/json", "Scope" : "meeting:recordings_read"}

        meetings_url = f"{webex_api_endpoint}/meetingTranscripts"
        response = requests.get(meetings_url, headers=headers)

        print("Loaded in all transcripts...", json.loads(response.text))
        self.meetings = json.loads(response.text)["items"]
        return {"response": self.meetings}, 200


