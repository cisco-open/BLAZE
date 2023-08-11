"""

This file implements the commands of the webex bot, via the underlying class `PrevMeetings`.

"""

from constants import CONSTANTS
import requests
import json


def LoadTranscripts():
    webex_api_endpoint = CONSTANTS.get("webex_api_endpoint")
    headers = {"Content-Type": "application/json"}
    meetings_url = f"{webex_api_endpoint}/download_webex_meeting_transcripts"
    response = requests.get(meetings_url, headers=headers)

    print("Loaded in all transcripts...", json.loads(response.text))
    transcriptFileName = json.loads(response.text)["fileName"]
    return transcriptFileName
        
"""

HELPER FUNCTIONS LISTED BELOW 

"""
def InitilizeTranscripts(transcriptFileName):

    url = CONSTANTS.get("webex_api_endpoint")+"/models/model/initialize"

    payload = json.dumps({
        "model": "ElasticBERT",
        "from_file": transcriptFileName
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

def SummarizeTranscripts(transcriptFileName): 
        print(transcriptFileName)
        payload = json.dumps({
            "model": "Bart",
            "from_file": transcriptFileName
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", CONSTANTS.get("webex_api_endpoint")+"/summary", headers=headers, data=payload)

        print(response.text)
        return json.loads(response.text)["result"]


def SearchTranscripts(query):
     
        payload = json.dumps({
            "model": "ElasticBERT",
            "query": query
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", CONSTANTS.get("webex_api_endpoint")+"/search", headers=headers, data=payload)

        print(response.text)
        return json.loads(response.text)["result"][0]["res"]
     
