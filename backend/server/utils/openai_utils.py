import multiprocessing as mp 
import time 
import openai 
import os 
from datetime import datetime 
from pytz import timezone
import pytz
from flask import current_app

def process_transcript(transcripts): 

    # Summary 
    rsp = gpt_analysis("summary",transcripts)
    summary = rsp['choices'][0]['text']
    print("Boutta put into extractions")

    # Actionables
    rsp = gpt_analysis("actionables",transcripts)
    actionables = rsp['choices'][0]['text']

    # Discussed Agenda
    rsp = gpt_analysis("agenda",transcripts)
    agenda = rsp['choices'][0]['text']

    return {"agenda":agenda,"actionables":actionables,"summary":summary}

def gpt_analysis(category, clean_info): 
    print("Reached GPT analysis")
    #return {'choices' : [{'text': "DUMMY RESPONSE"}]}
    
    if category == "summary": 
        prompt = "Analyze the following meeting transcript and generate a summary."
        message = f"{prompt}\n{clean_info}"
    elif category == "actionables": 
        prompt = "Analyze the following meeting transcript and identify actionable items (such as todo's) and return them in a list, separated by the pipeline '|' character" 
        message = f"{prompt}\n{clean_info}"
        print(message)
    elif category == "agenda": 
        prompt = "Analyze the following meeting transcript and idetnify discussed topics as well as the duration they were discussed and return them in a list, separated by the '-' between time and label, and separated by the pipeline '|' character between each item. For example, 'XX:XX - Introductions' may be a valid entry in the returned list, if the meeting contained an introduction." 
        message = f"{prompt}\n{clean_info}"
    else: 
        return None  

   
    openai.api_key = current_app.config.get('OPENAPI_KEY')

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message,
        temperature=0.7,
        max_tokens=892,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    
    return response 