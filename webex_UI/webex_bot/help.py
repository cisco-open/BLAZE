"""

This file implements the commands of the webex bot, via the underlying class `PrevMeetings`.

"""

from constants import CONSTANTS
import requests
import json


def LoadTranscripts():
    
    transcriptFileName = "webex_transcripts.json"
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


def ListMeetingTranscripts():
        response_string = ""
        webex_api_endpoint = CONSTANTS.get("webex_api_endpoint")
        headers = {"Content-Type": "application/json"}
        meetings_url = f"{webex_api_endpoint}/list_webex_meeting_transcripts"
        response = requests.get(meetings_url, headers=headers)
        print("Loaded in all transcripts...", json.loads(response.text))
        meetings = json.loads(response.text)['response']
        for meeting in meetings:
              id = meeting['id']
              response_string = response_string+ "".join(["ID:",meeting["id"],"\n","start_time:",meeting["startTime"],"\n","topic:",meeting["meetingTopic"],"\n\n\n"])
              
        return response_string

def SummarizeTranscripts(transcriptFileName,message): 
        transcripts_content = ""
        webex_api_endpoint = CONSTANTS.get("webex_api_endpoint")
        headers = {
            'Content-Type': 'application/json'
        }

        url = f"{webex_api_endpoint}/datasets/files/detail?filename={webex_transcripts.json}&fileclass=User"
        response = requests.request("GET", url, headers=headers)
        file_content = json.loads(response.text)["content"]
        print(file_content)

        if message.strip() == "all":
              transcripts_content = "\n".join(file_content.values())
        else:
            meeting_ids = message.split(",")
            for id in meeting_ids:
                transcripts_content = transcripts_content + file_content[id.strip()]

        payload = json.dumps({
                "model": "Bart",
                "content": transcripts_content
            })
            
        response = requests.request("POST", CONSTANTS.get("webex_api_endpoint")+"/summary", headers=headers, data=payload)
        transcript_response = json.loads(response.text)['result']
        
        return json.loads(response.text)['result']

 

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
     
